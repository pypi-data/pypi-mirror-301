"""
This module is a rewrite of the minimizers.py module.
"""

import time
import logging

import numpy as np
import scipy
import scipy.optimize
import pandas
import matplotlib.pyplot as plt

from sksparse import cholmod

try:
    from sparse_dot_mkl import gram_matrix_mkl, dot_product_mkl
except ModuleNotFoundError:
    logging.warning('module: `sparse_dot_mkl` not available')
else:
    logging.info('sparse_dot_mkl found. Building hessian should be faster.')


class Minimizer:
    """Find the minimum of a function using a Newton-Raphson method"""
    def __init__(self, log_likelihood, max_iter=100,
                 dchi2_stop=0.001, log=[]):
        """
        """
        self.log_likelihood = log_likelihood
        # self.model = self.log_likelihood.model
        self.max_iter = max_iter
        self.dchi2_stop = dchi2_stop
        self._log = log

    def ndof(self):
        # return self.model.training_dataset.nb_meas() - len(self.model.pars.free)
        return self.log_likelihood.ndof()

    def get_log(self):
        return pandas.DataFrame(self._log)

    def _brent(self, pars, dpars):
        """attempt to save the day with a line search
        """
        def min_1d_func(t):
            return self.log_likelihood(pars.free + t * dpars.free)

        # ret = pars.copy()
        logging.info('linesearch (brent)...')
        t, val, ni, funcalls = \
            scipy.optimize.brent(min_1d_func, brack=(0., 1.),
                                 full_output=True)
        # ret.free = pars.free + t * dpars.free
        logging.info(f'done: t={t}, val={val}')
        # logging.info(f'{val} == {self.log_likelihood(pars.free)}')
        return t

    def minimize(self, p_init, mode='supernodal', ordering_method='metis',
                 beta=0., dchi2_stop=None):
        """Minimize the log-likelihood"""
        # pars = self.model.pars
        pars = self.log_likelihood.pars
        pars.free = p_init
        dchi2_stop = dchi2_stop if dchi2_stop is not None else self.dchi2_stop
        # dpars = self.model.pars.copy()
        dpars = pars.copy()
        old_pars = pars.copy()
        dpars.full[:] = 0.
        self._log = []

        # minimization loop
        old_chi2 = None
        for i in range(self.max_iter+1):
            logging.info(f'nacl.minimizer: {i}')
            chi2, grad, hessian = self.log_likelihood(pars.free,
                                                      deriv=True)
            try:
                logging.info('cholesky...')
                fact = cholmod.cholesky(hessian.tocsc(),
                                        mode=mode,
                                        ordering_method=ordering_method,
                                        beta=beta)
                logging.debug('done.')
            except:
                logging.error(f'cholesky failed: matrix non-posdef')
                # try:
                #         logging.warning('attempting to recover with LDLt')
                #         fact = cholmod.cholesky(hessian.tocsc(),
                #                                 mode='simplicial',
                #                                 ordering_method=ordering_method,
                #                                 beta=beta)
                # except:
                #     logging.error(f'failed also.')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': self.ndof(),
                        'status': 'Cholesky failed',
                        'grad': grad,
                        'hessian': hessian}
            dpars.free = fact(grad)

            # print(dpars.free)

            # store previous parameter values
            old_chi2 = chi2
            old_pars.free = pars.free
            pars.free = pars.free + dpars.free
            # and recompute the chi2
            chi2 = self.log_likelihood(pars.free, deriv=False)
            # chi2 decrement
            dchi2 = old_chi2 - chi2

            if dchi2 < 0 & (np.abs(dchi2) > dchi2_stop):
                logging.warning(f'increasing chi2: dchi2={dchi2:.4e}')
                t = self._brent(old_pars, dpars)
                pars.free = old_pars.free + t * dpars.free
                chi2 = self.log_likelihood(pars.free, deriv=False)
                dchi2 = old_chi2 - chi2
                if dchi2 < 0.:
                    logging.warning(f'increasing chi2: {old_chi2} -> {chi2}')
                    # revert to the previous step
                    pars.free = old_pars.free
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': self.ndof(),
                            'status': 'increasing chi2'}

            # maybe we have converged ?
            if np.abs(dchi2) <= dchi2_stop:
                logging.info(f'converged: dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': self.ndof(),
                        'status': 'converged'}

            # and maybe we have exceeded the number of iterations ?
            if i >= self.max_iter:
                logging.info(f'iter {i:3} dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': self.ndof(),
                        'status': 'too many iterations'}

            logging.info(f'iter {i} dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')


    def minimize_lm(self, p_init, **kwargs):
        """The Levenberg Marquard version of minimize

        Parameters
        ----------
        dchi2_stop: float, default: 1.E-3
          stop criterion.
        mode: {'supernodal', 'simplicial'}, default: 'supernodal'
          cholmod algorithm.
        ordering_method: str, default: 'metis'
          ordering method.
        beta: float, default: 0.
          whether to surcharge the hessian diagonal before factorizing.
        lamb: float, default: 1.E-3
          the initial value of the LM damping parameter.
        accept: float, default: 10.
          factor applied on lambda if the step is accepted
        reject: float, default: 5.
          factor applied on lambda if the step is rejected
        max_iter: int, default:100
          maximum number of iterations before we give up
        geo: bool, default: False
          whether to enable geodesic acceleration
        hstep: float, default: 1.E-4
          numerical derivatives step

        Returns
        -------

        """
        # it has to be a copy !
        # pars = self.model.pars.copy()
        pars = self.log_likelihood.pars.copy()
        pars.free = p_init
        dchi2_stop = kwargs.get('dchi2_stop', self.dchi2_stop)
        # dpars = self.model.pars.copy()
        dpars = self.log_likelihood.pars.copy()
        dpars.full[:] = 0.
        self._log = []
        chi2_t = []
        tt = []

        old_pars = pars.copy()
        trial = pars.copy()
        mode = kwargs.get('mode', 'supernodal')
        ordering_method = kwargs.get('ordering_method', 'metis')
        beta = kwargs.get('beta', 0.)

        accept = kwargs.get('accept', 10.)
        reject = kwargs.get('reject', 10.)

        # number of tries to get a correct LM step
        max_attempts = kwargs.get('max_attempts', 100)
        # maximum number of iterations allowed
        max_iter = kwargs.get('max_iter', self.max_iter)
        lamb = kwargs.get('lamb', 10.)

        # diag_charge
        diag_charge = kwargs.get('diag_charge', 'levenberg')

        # whether to activate geodesic acceleration
        geo = kwargs.get('geo', False)
        h = kwargs.get('hstep', 1.E-4)

        # minimization loop
        for i in range(max_iter+1):
            # logging.info(f'minimize_lm: {i}')
            chi2, grad, hessian = self.log_likelihood(pars.free, deriv=True)
            # r0 = self.log_likelihood.w_res

            if i == 0:
                logging.info(
                    f'init: l={lamb:6.1e} chi2: {chi2:12.4e} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')

            # LM step
            success, attempts = False, 0
            while not success:
                if attempts == max_attempts:
                    logging.error('unable to get a valid LM step')
                    # TODO: define what we should return here.
                    return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': self.ndof(),
                        'status': 'no valid LM step'}

                try:
                    diag = hessian.diagonal()
                    if diag_charge == 'levenberg':
                        hessian.setdiag(diag + lamb)
                    elif diag_charge == 'marquardt':
                        hessian.setdiag((1.+lamb) * diag)
                    elif diag_charge == 'marquardt_max':
                        max_diag = diag.max()
                        hessian.setdiag(diag + lamb * max_diag)
                    else:
                        raise ValueError(f'diag_charge: invalid value {diag_charge}')

                    fact = cholmod.cholesky(hessian.tocsc(),
                                            mode=mode,
                                            ordering_method=ordering_method,
                                            beta=beta)

                    # NOTE: rectifying the algebra.
                    # if the log-likelohood returns its true gradient,
                    # the NR-step is H^-1 @ (-grad)
                    dpars.free = fact(-1. * grad)

                    # if geo:
                    #     _ = self.log_likelihood(pars.free + h * dpars.free)
                    #     r1 = self.log_likelihood.w_res
                    #     print(len(r1), len(r0))
                    #     d_w_res = (r1 - r0) / h
                    #     print(len(d_w_res), len(hessian.dot(dpars.free)))
                    #     dw = 2. * (d_w_res - hessian.dot(dpars.free)) / h
                    #     w_J = self.log_likelihood.w_J
                    #     geo_corr = -0.5 * fact(w_J.dot(dw))
                    #     truncerr = 2 * np.sqrt(geo_corr.dot(geo_corr)) / \
                    #                    np.sqrt(dpars.free.dot(dpars.free))

                    hessian.setdiag(diag)
                except:
                    logging.error(f'cholesky failed: matrix non posdef')
                    lamb *= reject
                    attempts += 1
                    continue

                # print(dpars)

                # old_chi2 = chi2
                # old_pars.free = pars.free
                # pars.free = pars.free + dpars.free
                trial.free = pars.free + dpars.free
                # if geo:
                #     trial.free += geo_corr

                # check_chi2 = self.log_likelihood(pars.free, deriv=False)
                trial_chi2 = self.log_likelihood(trial.free, deriv=False)
                # print(f'CHECK: {chi2} {check_chi2} {trial_chi2}')
                dchi2 = chi2 - trial_chi2

                # if geo and truncerr > 2.:
                #     pass
                if dchi2 > 0.  or (np.abs(dchi2) <= dchi2_stop):
                    success = True
                else:
                    pass

                # if dchi2 > 0. or (np.abs(dchi2) <= dchi2_stop):
                if success:
                    lamb /= accept
                    # logging.info(f'success: dchi2={dchi2}')
                else:
                    lamb *= reject
                    # chi2 = self.log_likelihood(pars.free, deriv=False)
                    logging.warning(f'[{attempts}/{max_attempts}] increasing chi2: dchi2={dchi2:.4e}')
                    logging.warning(f'next attempt with lambda={lamb:.4e}')
                    attempts += 1
                    continue

            # now, we can update the parameter vector
            old_chi2 = chi2
            chi2 = trial_chi2
            old_pars.free = pars.free
            pars.free = trial.free

            # if logging activated, we construct a log structure here
            l = self.log_likelihood.get_log()
            l['step'] = i
            l['time'] = time.perf_counter()
            l['lambda'] = lamb
            l['dchi2'] = dchi2
            l['ldpars'] = np.sqrt(np.dot(dpars.free, dpars.free))
            self._log.append(l)

            chi2_t.append(chi2)
            tt.append(time.perf_counter())

            # maybe we have converged ?
            if np.abs(dchi2) <= dchi2_stop:
                logging.info(f'converged: dchi2={dchi2:12.4e}: {old_chi2:12.4e} -> {chi2:12.4e} ndof={self.ndof()} chi2/ndof={chi2/self.ndof():.6f}')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': self.ndof(),
                        'status': 'converged',
                        'chi2_t':chi2_t,
                        'time':tt}

            # TODO: change this. This check should be after the loop
            # and maybe we have exceeded the number of iterations ?
            if i >= max_iter:
                logging.info(f'iter {i: 3d} l={lamb:6.1e}: {old_chi2:12.4e} -> {chi2:12.4e} | dchi2={dchi2:12.4e} | ndof={self.ndof()} chi2/ndof={chi2/self.ndof():.6f}')
                return {'pars': pars.copy(),
                        'chi2': chi2,
                        'ndof': self.ndof(),
                        'status': 'too many iterations',
                        'chi2_t':chi2_t,
                        'time':tt}

            logging.info(f'iter {i: 3d} l={lamb:6.1e}: {old_chi2:12.4e} -> {chi2:12.4e} | dchi2={dchi2:12.4e} | ndof={self.ndof()} chi2/ndof={chi2/self.ndof():.6f}')


    def get_cov_matrix(self, params_of_interest=None, corr=False, plot=False):
        """
        returns the covariance matrix and correlation matrix and the estimated
        errors on the parameters of interest
        cov : V
        corr : Vij/sqrt(Vii*Vjj)
        and can plot them

        Return:
        V : covariance matrix
        err_of_interest (optional) : errors on the specified parameters
        corr (optional) : correlation matrix
        """
        llk, grad, H = self.log_likelihood(self.log_likelihood.pars.free, deriv=True)
        #f = cholmod.cholesky(H, beta=1e-6)
        f = cholmod.cholesky(H)
        V = 2 * f.inv()
        var = V.diagonal()
        index_of_interest = np.array([])
        if plot:
            plt.figure()
            plt.imshow(V.toarray())
            plt.colorbar()
            plt.title('Covariance matrix')
        if params_of_interest is not None:
            for x in params_of_interest:
                idx = self.log_likelihood.pars.indexof(x)
                index_of_interest = np.append(index_of_interest, idx)
                if plot:
                    plt.figure()
                    plt.imshow(V.toarray()[idx][:,idx])
                    plt.colorbar()
                    plt.title('Covariance matrix of ' + x)
            index_of_interest = index_of_interest.astype(int)
            err_of_interest = np.sqrt(var[index_of_interest])
        else:
            err_of_interest = None
        if not corr:
            return V, err_of_interest
        else:
            N = len(var)
            i = np.arange(N)
            ii = np.vstack([i for k in range(N)])
            v1 = var[ii]
            v2 = v1.T
            vii_jj = v1 * v2
            vii_jj = np.sqrt(vii_jj)
            corr = V/vii_jj
            if plot:
                plt.figure()
                plt.imshow(corr.toarray())
                plt.colorbar()
                plt.title('Correlation matrix')
            return V, err_of_interest, corr


    def plot(self, timesteps=False):
        """
        """
        if not hasattr(self, '_log'):
            return
        d = pandas.DataFrame(self._log)
        fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(6,12), sharex=True)
        xx = d.step if not timesteps else d.time-d.time.min()
        xlabel = 'step' if not timesteps else 'time [s]'
        axes[0].plot(xx, d.llk, 'k.:')
        axes[0].set_ylabel(r'$-2\ln {\cal L}$')
        axes[1].semilogy(xx, d.main_chi2, 'b.:')
        axes[1].set_ylabel(r'$\chi^2$')
        axes[2].plot(xx, d.log_det_v, 'r.:')
        axes[2].set_ylabel(r'$\log\|\mathbf{V}\|$')
        axes[3].semilogy(xx, d.reg, 'g.:')
        axes[3].set_ylabel('reg')
        axes[4].semilogy(xx, d.cons, 'g.:')
        axes[4].set_ylabel('cons')
        axes[5].semilogy(xx, d.dchi2, 'b.:')
        axes[5].set_ylabel(r'$\delta -2\ln {\cal L}$')
        axes[5].set_xlabel(xlabel)
        plt.subplots_adjust(wspace=0.005, hspace=0.005)

    # this version will be deprecated in the future
    def __call__(self, p_init, mode='supernodal', ordering_method='metis',
                 beta=0., linesearch=False):
        """Minimize the log-likelihood
        """
        # pars = self.model.pars
        pars = self.log_likelihood.pars
        pars.free = p_init
        # dpars = self.model.pars.copy()
        dpars = self.log_likelihood.pars.copy()
        pars_before = pars.copy()
        dpars.full[:] = 0.
        self._log = []

        # minimization loop
        old_chi2 = None
        for i in range(self.max_iter):
            logging.info(f'nacl.minimizer: {i}')
            chi2, grad, hessian = self.log_likelihood(pars.free,
                                                      deriv=True)
            # maybe we are close to the minimum already ?
            if old_chi2 is not None:
                dchi2 = old_chi2 - chi2
                if (np.abs(dchi2) < self.dchi2_stop):
                    logging.info(f'converged: dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': self.ndof(),
                            'status': 'converged'}
                if dchi2 < 0.:
                    logging.warning(f'increasing chi2: {old_chi2} -> {chi2}')
                    # revert to the previous step
                    pars.free = pars_before.free
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': self.ndof(),
                            'status': 'increasing chi2'}
                if i >= self.max_iter:
                    return {'pars': pars.copy(),
                            'chi2': chi2,
                            'ndof': self.ndof(),
                            'status': 'too many iterations'}
                logging.info(f'iter {i} dchi2={dchi2:.4e}: {old_chi2:12.9g} -> {chi2:12.9g} ndof={self.ndof()} chi2/ndof={chi2/self.ndof()}')
            # else:
                # logging.info(f'first step - ')
            # if not, let's compute the next Newton-Raphson step...
            try:
                logging.info('cholesky...')
                fact = cholmod.cholesky(hessian.tocsc(),
                                        mode=mode,
                                        ordering_method=ordering_method,
                                        beta=beta)
                logging.info('done.')
            except:
                logging.error(f'cholesky failed: matrix non-posdef')
                return {'pars': pars.copy,
                        'chi2': chi2,
                        'ndof': len(pars.free),
                        'status': 'Cholesky failed',
                        'grad': grad,
                        'hessian': hessian}
            dpars.free = fact(grad)

            if linesearch:

                def min_1d_func(t):
                    return self.log_likelihood(pars_before.free + \
                                               t * dpars.free)

                logging.info('linesearch (brent)...')
                t, val, ni, funcalls = \
                    scipy.optimize.brent(min_1d_func, brack=(0., 1.),
                                         full_output=True)
                pars.free = pars_before.free + t * dpars.free
                logging.info(f'done: t={t}, val={val}')
                logging.info(f'{val} == {self.log_likelihood(pars.free)}')

            else:
                pars.free = pars_before.free + dpars.free

            if old_chi2 and (old_chi2 < chi2):
                # if increasing chi2 detected, then linesearch
                t = self._brent(pars_before, dpars)
                pars.free = pars_before.free + dpars.free

            # and update the old values
            old_chi2 = chi2
            pars_before.free = pars.free


# class LogLikelihood2:
#     """Compute a LogLikelihood and its derivatives from a model.

#     The main purpose of this class, is to assemble the ingredients of the
#     linearized normal equations, from (1) a model (2) a dataset (3) optional
#     add-ons such as contraints, regularization and an error model.

#     It was written to mimimize the typical Likelihood of the NaCl model
#     (see Guy's thesis, equation (1) page XX).
#     """

#     def __init__(self, model, cons=None, reg=None, variance_model=None,
#                  spec_weight_scale=1.,
#                  phot_error_pedestal=None,
#                  force_default_spgemm=False):
#         """
#         """
#         self.model = model
#         self.training_dataset = model.training_dataset
#         self.pars = self.model.pars.copy()
#         self.cons = cons if cons is not None else []
#         self.reg = reg if reg is not None else []
#         self.variance_model = variance_model
#         self.spec_weight_scale = spec_weight_scale
#         self.y = self.training_dataset.get_all_fluxes()
#         self.yerr = self.training_dataset.get_all_fluxerr()
#         self.bads = self.training_dataset.get_valid() == 0
#         self.phot_error_pedestal = phot_error_pedestal
#         self.force_default_spgemm = force_default_spgemm
#         self._log = None

#     def get_log(self):
#         return self._log

#     def ndof(self):
#         """
#         """
#         nphot, nsp, nspp = self.training_dataset.nb_meas(valid_only=True,
#                                                          split_by_type=True)
#         nmeas = nphot + np.sqrt(self.spec_weight_scale) * nsp + nspp
#         n_free_pars = len(self.model.pars.free)
#         return int(nmeas - n_free_pars)

#     def __call__(self, p, deriv=False):
#         """evaluate for the current parameters
#         """
#         self.model.pars.free = p

#         # the ingredients
#         bads = self.bads
#         model_flux, model_jac = None, None
#         model_var, model_var_jac = 0., None
#         chi2, log_det_v = 0., 0.

#         # just for logging purposes
#         main_chi2 = 0.
#         cons_chi2 = []
#         reg_chi2 = []

#         # wscales
#         # WARNING : in this method, the weights correspond to the
#         # inverse of the sigma, and not the inverse of the variance
#         # the weight scales follow this convention. Hence, to
#         # reduce the contribution of the spectra to the global chi2
#         # by a factor 0.1, the wscales need to be equal to np.sqrt(0.1)
#         wscales = np.ones(len(self.y))
#         nlc, nsp, nspp = self.training_dataset.nb_meas(valid_only=False, split_by_type=True)
#         wscales[nlc:nlc+nsp] *= np.sqrt(self.spec_weight_scale)

#         # if no derivatives requested,
#         # just add the penalities and we should be ok
#         if not deriv:
#             # model and variance
#             model_flux = self.model(p, jac=False)
#             var = self.yerr**2 / wscales ** 2
#             # here: add an optional pedestal to fluxerr
#             # warning: this option is dangerous, because
#             # it results in the biased result. Use it only
#             # during the first steps of training, to ease
#             # the first chi2 minimizations
#             if self.phot_error_pedestal is not None:
#                 nlc, _, _ = self.training_dataset.nb_meas(valid_only=False, split_by_type=True)
#                 ped = (self.phot_error_pedestal * self.y) ** 2
#                 var[:nlc] += (ped[:nlc] / wscales**2)
#             if self.variance_model is not None:
#                 model_var = self.variance_model(model_flux=model_flux)
#                 var += (model_var / wscales**2)
#                 log_det_v = np.log(var[~bads]).sum()

#             # weighted residuals
#             res = self.y - model_flux
#             sig = np.sqrt(var)
#             wres = res / sig

#             # if hasattr(self, 'debug'):
#             #     self.chi2_debug = (wres[~bads]**2).sum()
#             #     self.log_det_v_debug = log_det_v
#             #     self.full_chi2_debug = self.chi2_debug + log_det_v

#             # and the chi2
#             main_chi2 = (wres[~bads]**2).sum()
#             chi2 = main_chi2 + log_det_v
#             for cons in self.cons:
#                 c = cons(p, deriv=False)
#                 cons_chi2.append(c)
#                 chi2 += c
#                 # chi2 += cons(p, deriv=False)
#             for reg in self.reg:
#                 r = reg(p, deriv=False)
#                 reg_chi2.append(r)
#                 chi2 += r
#                 # chi2 += reg(p, deriv=False)

#             self._log = {'chi2': main_chi2,
#                          'log_det_v': log_det_v,
#                          'cons': np.sum(cons_chi2),
#                          'reg': np.sum(reg_chi2)}

#             return chi2

#         # that was the easy part. Now, when derivatives requested
#         # things are little more complicated.
#         logging.debug('model (jac=True)')
#         model_flux, model_jac = self.model(p, jac=True)
#         var = self.yerr**2 / wscales**2
#         if self.phot_error_pedestal is not None:
#             nlc, _, _ = self.training_dataset.nb_meas(valid_only=False, split_by_type=True)
#             ped = (self.phot_error_pedestal * self.y) ** 2
#             var[:nlc] += (ped[:nlc] / wscales**2)
#         if self.variance_model is not None:
#             logging.debug('variance model (jac=True)')
#             model_var, model_var_jac = \
#                 self.variance_model(model_flux=model_flux,
#                                     model_jac=model_jac,
#                                     jac=True)
#             var += (model_var / wscales**2)
#             # I assume model_var_jac is a coo_matrix
#             model_var_jac = model_var_jac.tocoo()
#             model_var_jac.data /= wscales[model_var_jac.row]**2
#             log_det_v = np.log(var[~bads]).sum()

#         # weighted residuals
#         res = self.y - model_flux
#         w = 1. / np.sqrt(var)
#         N = len(self.y)
#         W = scipy.sparse.dia_matrix((w, [0]), shape=(N, N))
#         w_res = W @ res
#         w_J = W @ model_jac

#         # cut the bads
#         w_J = w_J[~bads,:]
#         w_res = w_res[~bads]

#         # store the results. May be used later
#         self.w_res = w_res
#         self.w_J = w_J

#         # chi2
#         main_chi2 = chi2 = (w_res**2).sum()
#         chi2 += log_det_v

#         # if hasattr(self, 'debug'):
#         #     self.chi2_debug = main_chi2
#         #     self.log_det_v_debug = log_det_v
#         #     self.full_chi2_debug = chi2

#         # the gradient and hessian have several components
#         # first, the two classical ones: J^TWJ and J^TWR
#         grad = 2. * w_J.T @ w_res
#         w_J = w_J.tocsr()
#         if 'gram_matrix_mkl' in globals() and not self.force_default_spgemm:
#             logging.debug('hessian: H = J.T @ J (gram_matrix_mkl)')
#             if 1 in w_J.shape:
#                 # there seem to be a bug in gram_matrix_mkl when
#                 # one of the matrix dimensions is one. typically refuses
#                 # to contract (N,1) matrix into a scalar
#                 hess = 2. * dot_product_mkl(w_J.T, w_J, reorder_output=True)
#             else:
#                 # `reorder_output=True` seems essential here.
#                 # otherwise, the Newton-Raphson step is wrong, typically
#                 # by a factor 0.5 ... this is scary, I know...
#                 hess = 2. * gram_matrix_mkl(w_J, reorder_output=True)
#                 row, col = hess.nonzero()
#                 hess[col,row] = hess[row,col]
#                 #            hess = 2. * dot_product_mkl(w_J.T, w_J, reorder_output=True)
#         else:
#             logging.debug('hessian: H = J.T @ J (slow version)')
#             hess = 2. * w_J.T @ w_J

#         # model_jac.data *= w[model_jac.row]
#         # main_chi2 = chi2 = (wres[~bads]**2).sum()
#         # chi2 += log_det_v
#         # wres = wres[~bads]

#         # then, the contributions of the (optional) variance model
#         # to the hessian and gradient
#         # TODO:
#         #  - remove outliers from the model jacobian
#         #  - if W @ J faster, do that
#         # TODO:
#         #  -if some variance model parameters are fixed this is apparently
#         # not taken into account ...
#         if self.variance_model is not None:
#             logging.debug('variance model')
#             WW = scipy.sparse.dia_matrix((w**2, [0]), shape=(N, N))
#             # model_var_jac.data /= var[model_var_jac.row]
#             model_var_jac = (WW @ model_var_jac)[~bads, :]

#             # gradient
#             # was +1
#             # rWdVWr = -1. * (w_res**2).sum() * np.array(model_var_jac.T.sum(axis=1)).squeeze()
#             mvJ = model_var_jac.tocoo()
#             wres_mvJ = scipy.sparse.coo_matrix(
#                 (mvJ.data * w_res[mvJ.row],
#                  (mvJ.row, mvJ.col)),
#                  shape=mvJ.shape)
#             rWdVWr = 1. * wres_mvJ.T @ w_res

#             # rWdVWr = -1. * (w_res**2 * np.array(model_var_jac.T)).sum(axis=1).squeeze()
#             grad += rWdVWr
#             # was -1
#             tr_WdV = -1. * np.array(model_var_jac.T.sum(axis=1)).squeeze()
#             grad += tr_WdV

#             # hessian
#             tr_WdVWdV = 1. * model_var_jac.T.dot(model_var_jac)
#             hess += tr_WdVWdV

#         # the quadratic constraints
#         logging.debug('constraints')
#         for penality in self.cons:
#             v_pen, grad_pen, hess_pen = penality(p, deriv=True)
#             chi2 += v_pen
#             grad += grad_pen
#             hess += hess_pen
#             cons_chi2.append(v_pen)

#         # the regularization
#         logging.debug('regularization')
#         for penality in self.reg:
#             v_pen, grad_pen, hess_pen = penality(p, deriv=True)
#             chi2 += v_pen
#             grad += grad_pen
#             hess += hess_pen
#             reg_chi2.append(v_pen)

#         self._log = {
#             'chi2': main_chi2,
#             'log_det_v': log_det_v,
#             'cons': np.sum(cons_chi2),
#             'reg': np.sum(reg_chi2),
#         }

#         msg = f'chi2={main_chi2:.6e} | log_det_v={log_det_v} | cons='
#         for cons_val in cons_chi2:
#             msg += f'{cons_val:8.6e}'
#         msg += ' | reg='
#         for reg_val in reg_chi2:
#             msg += f'{reg_val:.6e}'
#         logging.debug(msg)

#         return chi2, grad, hess

#     def get_weighted_residuals(self, p):
#         """a utility function to get the weighted residuals
#         """
#         model_flux = self.model(p, jac=False)
#         res = self.y - model_flux
#         var = self.yerr**2
#         if self.variance_model is not None:
#             model_var = self.variance_model(model_flux=model_flux,
#                                             jac=False)
#             var += model_var
#         w = 1. / np.sqrt(var)
#         W = scipy.sparse.dia_matrix((w, [0]), shape=(N,N))
#         w_res = W @ res

#         return w_res


# class LogLikelihood:
#     """Compute a LogLikelihood and its derivatives from a model.

#     The main purpose of this class, is to assemble the ingredients of the
#     linearized normal equations, from (1) a model (2) a dataset (3) optional
#     add-ons such as contraints, regularization and an error model.

#     It was written to mimimize the typical Likelihood of the NaCl model
#     (see Guy's thesis, equation (1) page XX).
#     """

#     def __init__(self, wres_func, cons=None, reg=None, error_snake=None):
#         """
#         """
#         self.func = wres_func
#         self.model = self.func.model
#         self.pars = self.func.model.pars.copy()
#         self.cons = cons if cons is not None else []
#         self.reg = reg if reg is not None else []
#         self.error_snake = error_snake if error_snake is not None else []
#         self.bads = wres_func.model.training_dataset.get_valid() == 0

#     def __call__(self, p, deriv=False):
#         """evaluate for the current parameters
#         """
#         self.model.pars.free = p
#         bads = self.bads

#         # if no derivatives requested,
#         # just add the penalities and we should be ok
#         if not deriv:
#             w_res = self.func(p, jac=False)
#             chi2 = (w_res[~bads]**2).sum()
#             for cons in self.cons:
#                 chi2 += cons(p, deriv=False)
#             for reg in self.reg:
#                 chi2 += reg(p, deriv=False)
#             return chi2

#         # if derivatives requested, then
#         # 1) base chi2 + gradient + hessian
#         w_res, w_J, _ = self.func(p, jac=True)
#         w_res = w_res[~bads]
#         w_J = w_J[~bads,:]
#         chi2 = (w_res**2).sum()
#         grad = 2. * w_J.T @ w_res
#         hess = 2. * w_J.T @ w_J

#         # just for logging purposes
#         main_chi2 = chi2
#         cons_chi2 = []
#         reg_chi2 = []

#         # add the penalities and their derivatives
#         for penality in self.cons:
#             v_pen, grad_pen, hess_pen = penality(p, deriv=True)
#             chi2 += v_pen
#             grad += grad_pen
#             hess += hess_pen
#             cons_chi2.append(v_pen)

#         for penality in self.reg:
#             v_pen, grad_pen, hess_pen = penality(p, deriv=True)
#             chi2 += v_pen
#             grad += grad_pen
#             hess += hess_pen
#             reg_chi2.append(v_pen)

#         msg = f' LogLikelihood: chi2={main_chi2:.6e} | cons='
#         for cons_val in cons_chi2:
#             msg += f'{cons_val:.6e}'
#         msg += ' | reg='
#         for reg_val in reg_chi2:
#             msg += f'{reg_val:.6e}'
#         logging.info(msg)

#         return chi2, grad, hess


class WeightedResiduals:

    def __init__(self, model, variance_model=None):
        """iniate the residual function"""
        self.model = model
        self.training_dataset = model.training_dataset
        self.variance_model = variance_model
        self.y = self.training_dataset.get_all_fluxes()
        self.yerr = self.training_dataset.get_all_fluxerr()

    def __call__(self, p, jac=False):
        """evaluate"""
        self.model.pars.free = p

        # evaluate the residuals
        val, J = None, None
        if jac:
            val, J = self.model(p, jac=True)
        else:
            val = self.model(p, jac=False)
        res = self.y - val

        # measurement variance and weights
        var, Jvar = 0., None
        if self.variance_model is not None:
            if not jac:
                var = self.variance_model(p, jac=False)
            else:
                var, Jvar = self.variance_model(p, jac=True)

        res_var = self.yerr**2 + var
        w = 1. / np.sqrt(res_var)
        N = len(self.y)
        W = scipy.sparse.dia_matrix((w, [0]), shape=(N, N))

        # weighted residuals
        wres = W @ res
        if jac:
            wJ = W @ J
            return wres, wJ, Jvar
        return wres
