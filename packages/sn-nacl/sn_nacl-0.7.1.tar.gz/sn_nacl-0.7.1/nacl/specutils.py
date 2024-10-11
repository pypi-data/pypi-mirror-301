"""
"""

import sys
import logging

import numpy as np
from scipy.interpolate import interp1d
from scipy import sparse
import matplotlib.pyplot as plt

from sksparse import cholmod

from saltworks.plottools import binplot
from saltworks.robuststat import mad
from bbf.bspline import integ


class Spec:

    class FitResults:
        pass

    def __init__(self, tds, spec, basis,
                 error_eval_bin_width=50.,
                 beta=1.E-8):
        self.tds = tds
        self.spec = spec
        self.basis = basis
        self.error_eval_bin_width = error_eval_bin_width
        self.beta = beta
        if tds.spec_data != None:
            tds_spec_data = tds.spec_data
        else:
            tds_spec_data = tds.spectrophotometric_data
        self.tds_spec_data = tds_spec_data
        idx = self.idx = tds_spec_data.spec == spec

        for field in ['sn', 'mjd', 'valid', 'spec', 'exptime', 'z']:
            setattr(self, field, self._check_field(field))
        sn = tds_spec_data.sn[idx]
        assert np.all(np.equal(sn, sn[0]))

        self.wl = tds_spec_data.wavelength[idx]
        self.restframe_wl = self.wl / (1. + self.z)
        self.flux = tds_spec_data.flux[idx]
        self.fluxerr = tds_spec_data.fluxerr[idx]

        # # cut the NaN's
        # self.cut = np.isnan(self.flux) | (self.fluxerr < 0) | np.isnan(self.fluxerr)
        # if self.cut.sum() > 0:
        #     logging.warning(f'{self.cut.sum()} measurement detected with negative of nan uncertainties')

        # # cut the NaN's
        # self.cut = np.isnan(self.flux) | (self.fluxerr < 0) | np.isnan(self.fluxerr)
        # if self.cut.sum() > 0:
        #     logging.warning(f'{self.cut.sum()} measurement detected with negative of nan uncertainties')

        # wl_min, wl_max = basis.grid.min(), basis.grid.max()
        # # print(wl_min, wl_max, self.restframe_wl.min(), self.restframe_wl.max())
        # cut = (self.restframe_wl<wl_min) | (self.restframe_wl>wl_max)
        # if cut.sum() > 0:
        #     logging.info(f'{self.cut.sum()} outside basis range')
        # self.cut &= cut

        self.cut = self._select_data()

        self.fitres = []

    def _select_data(self):
        """the spectral data generally needs to be cleaned.
        """
        # remove the NaN's
        nan_idx = np.isnan(self.flux) | np.isnan(self.fluxerr)

        # some errors are negative
        # we don't cut the data - we resset them temporarily to 1.
        negflxerr_idx = self.fluxerr < 0.
        self.fluxerr[negflxerr_idx] = 1.

        # some data points are zeros
        zero_idx = (self.flux == 0.) | (self.fluxerr == 0.)

        # finally, get rid of all the data that is outside
        # the (restframe) basis wavelength rage
        wl_min, wl_max = self.basis.grid.min(), self.basis.grid.max()
        out_of_range_idx = (self.restframe_wl < wl_min) | (self.restframe_wl > wl_max)

        self.select_stats = {'nan': nan_idx.sum(),
                             'negative_errs': negflxerr_idx.sum(),
                             'zero_flux_or_err': zero_idx.sum(),
                             'out_of_range': out_of_range_idx.sum()}

        cut = nan_idx | zero_idx | out_of_range_idx
        logging.info(f'{self.sn}: {cut.sum()} measurement removed.')
        if cut.sum() > 0:
            logging.info(f'nan:{nan_idx.sum()} zflx:{zero_idx.sum()} oorng: {out_of_range_idx.sum()}')

        return cut

    def _check_field(self, name):
        """
        """
        try:
            s = np.unique(self.tds_spec_data.nt[self.idx][name])
        except:
            s = np.unique(self.tds_spec_data.__dict__[name][self.idx])
        assert len(s) == 1
        return s[0]

    def fit(self, x, y, yerr, beta=None):
        """
        """
        N = len(x)
        assert (len(y) == N) and (len(yerr) == N)
        if beta is None:
            beta = self.beta

        J = self.basis.eval(x)
        w = 1. / yerr
        W = sparse.dia_matrix((w**2, 0), shape=(N,N))
        H = J.T @ W @ J
        fact = cholmod.cholesky(H.tocsc(), beta=beta)

        r = Spec.FitResults()
        r.coeffs = fact(J.T @ W @ y)
        r.res = (y - J @ r.coeffs)
        r.wres = (y - J @ r.coeffs) * w
        r.chi2 = (r.wres**2).sum()
        r.ndof = (len(y) - len(r.coeffs))
        r.rchi2 = r.chi2 / r.ndof
        r.basis = self.basis
        #try:
        HH = H.todense() + np.diag(np.full(len(r.coeffs), 1.E-20))
        r.coeffs_cov = np.linalg.inv(HH)
        r.coeffs_err = np.sqrt(np.array(r.coeffs_cov.diagonal()).squeeze())
        r.i = np.arange(len(r.coeffs))
        r.selection = r.coeffs_err < 0.5/beta

            # r.coeffs_err = np.sqrt(scipy.sparse.linalg.inv(H).diagonal())
        #except:
        #    r.coeffs_err = np.zeros_like(r.coeffs)

        return r

    def recompute_error_model(self, wl, res, nbins=10):
        """
        """
        #       nbins = int((wl.max() - wl.min()) / bin_width)
        x, y, yerr = binplot(wl, res, nbins=nbins, scale=False, noplot=True)
        self.error_model = interp1d(x, yerr, kind='linear', fill_value=(yerr[0], yerr[-1]), bounds_error=False)
        self.x_err, self.y_err = x, yerr
        return self.error_model

    def flag_residuals(self):
        """
        """
        pass

    def process(self):
        """
        """
        rwl = self.restframe_wl[~self.cut]
        flx = self.flux[~self.cut]
        flxerr = self.fluxerr[~self.cut]

        if len(rwl) == 0:
            logging.error(f'{self.sn} no data')
            return None

        # re-eval errors
        r = self.fit(rwl, flx, flxerr)
        error_model = self.recompute_error_model(rwl, r.res, nbins=10)
        self.fitres.append(r)

        # re-fit with recomputed errors
        model_flxerr = error_model(self.restframe_wl)
        if np.any(model_flxerr <= 0.):
            logging.error(f'{self.sn}: unable to recompute an error model')
            self.estimated_fluxerr = model_flxerr
            return None

        r = self.fit(rwl, flx, model_flxerr[~self.cut])
        self.fitres.append(r)

        # # bin spectrum
        # r = self.fit(self.wl, self.flux, fluxerr, order=1, bin_width=self.bin_width)
        # self.fitres.append(r)

        self.estimated_fluxerr = model_flxerr

    def get_projected_spectrum(self):
        """
        """
        if len(self.fitres) != 2:
            return None

        r = self.fitres[1]
        idx = r.selection
        wl = integ(r.basis, n=1) / integ(r.basis, n=0)
        # wl = wl[r.selection]
        N = idx.sum()

        d = np.zeros(N, self.tds_spec_data.nt.dtype)
        d['sn'] = self.sn
        d['spec'] = self.spec
        d['mjd'] = self.mjd
        d['valid'] = self.valid
        d['exptime'] = self.exptime
        d['wavelength'] = wl[idx]
        d['i_basis'] = r.i[idx]
        d['flux'] = r.coeffs[idx]
        d['fluxerr'] = r.coeffs_err[idx]
        return d

    def plot(self):
        """
        """
        try:
            r = self.fitres[1]
        except:
            logging.warning('problem with the fit: showing initial fit')
            try:
                r = self.fitres[0]
            except:
                r = None
                logging.warning('problem with the fit: no fit available')

        fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(8,8), sharex=False)

        fig.suptitle(f'SN{self.sn} z={self.z} mjd={self.mjd}')

        # the original spectrum (with re-estimated errors and the fit)
        axes[0].errorbar(self.restframe_wl[~self.cut], self.flux[~self.cut], yerr=self.estimated_fluxerr[~self.cut],
                         ls='', marker='.', label='orig')
        wl_min, wl_max = self.restframe_wl.min(), self.restframe_wl.max()

        if r is not None:
            wl = np.linspace(wl_min, wl_max, 1000)
            J = self.basis.eval(wl)
            axes[0].plot(wl, J @ r.coeffs, 'r-', zorder=1000)
            axes[0].set_ylabel('spectrum')

        # the residuals
        if r is not None:
            axes[1].errorbar(self.restframe_wl[~self.cut], r.res, yerr=self.estimated_fluxerr[~self.cut],
                             ls='', marker='.', color='b')
            axes[1].set_ylabel('residuals')

            axes[2].plot(self.x_err, self.y_err, 'bo')
            xx = np.linspace(self.restframe_wl.min(), self.restframe_wl.max(), 100)
            axes[2].plot(xx, self.error_model(xx), 'r-')
            axes[2].set_ylabel('error model')

        # axes[3].shared_x_axes.remove(axes[3])
        if r is not None:
            axes[3].plot(r.i, r.coeffs,
                         color='gray', marker='.', alpha=0.5, ls='')
            axes[3].errorbar(r.i[r.selection], r.coeffs[r.selection], yerr=r.coeffs_err[r.selection],
                             ls='', marker='.')
            y = r.coeffs[r.selection]
            ym, ys = np.median(y), mad(y)
            axes[3].set_ylim((ym-3*ys, ym+3*ys))
            axes[3].set_ylabel('projection')


def clean_and_project_spectra(tds, basis):
    """
    """
    #spec_data = tds.spec_data
    if tds.spec_data is not None:
        spec_data = tds.spec_data
    else:
        spec_data = tds.spectrophotometric_data
    l = []
    with_errors = []
    z = spec_data.z
    for spec in spec_data.spec_set:
        s = Spec(tds, spec, basis)
        logging.info(f'processing {s.sn} {spec}')
        try:
            s.process()
            p = s.get_projected_spectrum()
        except:
            logging.error(f'unable to process: {s.sn}')
            logging.error(f'{sys.exc_info()}')
            p = None
        if p is None:
            with_errors.append(s)
            continue
        l.append(p)
    return l, with_errors
