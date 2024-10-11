r"""

The purpose of regularization is to constrain the surfaces :math:`M_0` and
:math:`M_1` in areas of the plane that are empty of data. We use a classical
regularization scheme, called Generalized Tikhonov Regularization, consisting
in adding a small quadratic penalty. This penalty is designed to limit the
abrupt variations of the model (oscillations) and to make the model tend slowly
towards zero in the absence of data, in particular at the phases :math:`p <
-20` and :math:`p > 60` days.

The :math:`\chi^2_{reg}` is defined as :

.. math::
    \chi^2_{reg} = \mu_{reg} \beta^T P \beta

With :math:`P`, listing parameters in four blocs
([:math:`X_0`, :math:`t_{max}^{B^\star}`, :math:`X_1`, :math:`c`], :math:`M_0`, :math:`M_1`,
[:math:`CL`, :math:`s` , :math:`\eta`, :math:`\kappa`]), by:

.. math::
    \begin{equation}
    P = \left (
    \begin{array}{c c c c}
    0 & 0 & 0 & 0 \\
    0 & P_{\theta_{0|1}} & 0 & 0\\
    0 & 0 & P_{\theta_{0|1}} & 0\\
    0 & 0 & 0 & 0
    \end{array}
    \right)
    \end{equation}

The matrix :math:`P_{\theta_{0|1}}` is defined in the different
regularization class.

"""

import numpy as np
from scipy.sparse import coo_matrix, dia_matrix, csc_matrix, dok_matrix


# this is a minimal rewrite of the original class SplineRegul2D by Guy
# to simplify it (we can condense both regulization inside one single class
# and also to adapt it to the interface expected by the LogLikelihood class.

class SplineRegularization:
    """
    """
    def __init__(self, model, pars, to_regularize=None, mu=1.E-6):
        """
        """
        self.model = model
        # self.pars = self.model.pars
        self.to_regularize = to_regularize
        if to_regularize is None:
            self.to_regularize = ['M0', 'M1']
        self.mu = mu
        # we call it P_full, to remind us that it regularizes all
        # the parameters (free and fixed) of the selected blocks
        self.P_full = self._init_regularization_matrices(pars)

    def _init_regularization_matrices(self, pars):
        raise NotImplementedError('SplineRegularization is pure virtual')

    def __call__(self, pars, deriv=False):
        """
        """
        full_pars = pars.full
        penality = float(full_pars.T @ self.P_full @ full_pars)
        if not deriv:
            return self.mu * penality

        # gradient of the free parameters
        n = self.P_full.shape[0]
        idx = pars.indexof(np.arange(n)) >= 0
        grad = -2. * (self.P_full @ full_pars)[idx]

        # and finally, the hessian (needs to be sliced also)
        if idx.sum() > 0:
            P = self.P_full[:,idx][idx,:]
        else:
            P = self.P_full
        hess = 2. * P

        mu = self.mu

        return mu * penality, mu * grad, mu * hess


def get_naked_regularization_matrix(size, order=0):
    """
    """
    if order == 0:
        data = np.ones(size)
        return dia_matrix((data, [0]), shape=(size,size)).tocoo()

    data = np.vstack(([3.] * size, [-1.] * size, [-1.] * size))
    data[0, 0] = data[0, -1] = 2.
    mat = dia_matrix((data, [0, -1, 1]), shape=(size,size)).tocoo()
    return mat


class NaClSplineRegularization(SplineRegularization):

    def __init__(self, model, pars, to_regularize, mu=1.E-6, order=1):
        """
        """
        self.order = order
        super().__init__(model, pars, to_regularize, mu)

    def _init_regularization_matrices(self, pars):
        """Build a NaCl regularization matrix
        """
        pars_full = pars.copy()
        pars_full.release()
        npars = len(pars_full.full)

        P_full = dok_matrix((npars,npars))

        for block_name in self.to_regularize:
            block_pars = pars_full[block_name].full
            block_size = len(block_pars)
            mat = get_naked_regularization_matrix(block_size, order=self.order)

            # full matrix (used to compute the regularization value)
            i = pars_full[block_name].indexof(mat.row)
            j = pars_full[block_name].indexof(mat.col)
            P_full += coo_matrix((mat.data, (i,j)), shape=(npars,npars))

        return P_full


class SplineRegul2D(object):
    r"""
    This regularization focuses on the model variations in phase.
    The density of spectra allows the basis to be constrained correctly, and the density of points
    on the spectra seems to limit the oscillation phenomena.

    The :math:`\chi^2_{reg}` is defined as :

    .. math::
        \chi^2_{reg} &= \mu_{reg} \left[\sum_{i=0}^{N_{\lambda}-1} \sum_{i=0}^{N_{phase}-1}
        \left(\theta_{0|1}^{j, i+1} - \theta_{0|1}^{j, i}\right)^2 + (\theta_{0|1}^{ji})^2 \right] \\

    This gives that by default :math:`P_{\theta_{0|1}}` is given by:

    .. math::
        P_{\theta_{0|1}} = \begin{pmatrix}
        2 & -1 & 0 &  \cdots & & && 0 \\
        -1 & 3 & -1 & \cdots & &  &&0 \\
        \cdots & & & \cdots & & & &\cdots\\
        \cdots & & -1 & 3 & -1 & & &\cdots\\
        \cdots & & & \cdots & & & &\cdots\\
        0 & && \cdots &  &  -1 & 3 & -1 \\
        0 & & &\cdots &  &  & -1 & 2 \\
        \end{pmatrix}

    else :math:`P_{\theta_{0|1}}` is only the identity matrix.

    Attributes
    ----------
    pars : numpy.array
        Model parameter
    mu : float
        Amplitude of the regularization penalty
    matrix_free : scipy.sparse.coo_matrix
        :math:`P_{\theta_{0|1}}` of only the free parameters.
    matrix_full : scipy.sparse.coo_matrix
        :math:`P_{\theta_{0|1}}` of all the parameters.
    """

    def __init__(self, model, surfaces_reg=['M0'], mu=1.E-6, deriv=True):
        r"""
        Constructor.
        Creation of the :math:`P` matrix.

        Parameters
        ----------
        model : nacl.salt
            Model to regularize.
        surfaces_reg : list
            List of surfaces to regularized
        mu : float
            Amplitude of the contribution to the :math:`\chi^2`
        deriv : bool
            if True :math:`P_{\theta_{0|1}}` is used.
            Else its a diagonal matrix.
        """
        self.pars = model.pars.copy()
        self.mu = mu

        # build the regularization matrix for the spline parameters
        n = len(self.pars['M0'].full)
        if deriv:
            data = np.vstack(([3.] * n, [-1.] * n, [-1.] * n))
            data[0, 0] = data[0, -1] = 2.
            idx_data = [0, -1, 1]
        else:
            # only diagonal term
            data = np.ones(n).astype(float)
            idx_data = [0]

        matrix = dia_matrix((data, idx_data), shape=(n, n)).tocoo()
        # embed it in a larger matrix, that corresponds to the model parameters
        n_pars = len(self.pars.free)
        i = self.pars['M0'].indexof(matrix.row)
        j = self.pars['M0'].indexof(matrix.col)
        idx = (i >= 0) & (j >= 0)
        matrix_free0 = coo_matrix((matrix.data[idx]*self.mu, (i[idx], j[idx])), shape=(n_pars, n_pars))

        if 'M1' in surfaces_reg:
            n1 = len(self.pars['M1'].full)
            if deriv:
                data1 = np.vstack(([3.] * n1, [-1.] * n1, [-1.] * n1))
                data1[0, 0] = data1[0, -1] = 2.
                idx_data1 = [0, -1, 1]
            else:
                # only diagonal term
                data1 = np.ones(n1).astype(float)
                idx_data1 = [0]

            matrix_1 = dia_matrix((data1, idx_data1), shape=(n1, n1)).tocoo()
            i1 = self.pars['M1'].indexof(matrix_1.row)
            j1 = self.pars['M1'].indexof(matrix_1.col)
            idx1 = (i1 >= 0) & (j1 >= 0)
            matrix_free1 = coo_matrix((matrix_1.data[idx1]*self.mu, (i1[idx1], j1[idx1])), shape=(n_pars, n_pars))
            self.matrix_free = (matrix_free0 + matrix_free1)
        else:
            self.matrix_free = matrix_free0

        pp = self.pars.copy()
        pp.release()
        n_pars = len(pp.full)
        i = pp['M0'].indexof(matrix.row)
        j = pp['M0'].indexof(matrix.col)

        if 'M1' in surfaces_reg:
            i1 = pp['M1'].indexof(matrix_1.row)
            j1 = pp['M1'].indexof(matrix_1.col)
            self.matrix_full = coo_matrix((matrix.data*self.mu, (i, j)),
                                          shape=(n_pars, n_pars))+coo_matrix((matrix_1.data * self.mu, (i1, j1)),
                                                                             shape=(n_pars, n_pars))
        else:
            self.matrix_full = coo_matrix((matrix.data*self.mu, (i, j)), shape=(n_pars, n_pars))  # sans les self.mu

    def __call__(self, beta):
        r"""
        Calculate the regularization contribution to the final :math:`\chi^2`

        Parameters
        ----------
        beta : array
            Model parameters.

        Returns
        -------
        v : float
            Value of the :math:`\chi^2_{reg}`
        matrix_free : scipy.sparse.coo_matrix
            :math:`P_{\theta_{0|1}}`
        """
        self.pars.free = beta.free
        # there is probably a way to compute this faster
        v = np.dot(self.pars.full.T, self.matrix_full * self.pars.full)
        return v, self.matrix_free


class SplineRegul2DSalt3(object):
    r"""
    This regularization is the one defined in SALT3 (Kenworthy et al. 2021)
    It is focused on the model variations in phase and wavelength.
    The density of spectra allows the basis to be constrained correctly, and the density of points
    on the spectra seems to limit the oscillation phenomena.

    The :math:`\chi^2_{reg}` is defined as :

    .. math::
        \chi^2_{reg} = \mu_{reg} \sum_{j=0}^{2N_{\lambda}} \sum_{i=0}^{2N_{phase}} \left[\frac{\left(
        \left.\frac{\partial M_{0|1}}{\partial p} \right|_{p = p_i,
        \lambda = \lambda_j }\right)^2}{N_{eff}(p_i,\lambda_j)} +
        \frac{\left( \left.\frac{\partial M_{0|1}}{\partial \lambda}
        \right|_{p = p_i, \lambda = \lambda_j } \right)^2}{N_{eff}(p_i,\lambda_j)}
        + \frac{1}{N_{eff}(p_i,\lambda_j)}\left( \frac{\partial M_{0|1}}{\partial p}
        \times \frac{\partial M_{0|1}}{\partial \lambda} + M_{0|1}\frac{\partial^2 M_{0|1}}{\partial
        \lambda \partial p} \right) \right]
    """
    def __init__(self, model, surfaces_reg=['M0'], mu=1.E-6):
        r"""
        Constructor.
        Creation of the :math:`P` matrix.

        Parameters
        ----------
        model : nacl.salt
            Model to regularize.
        surfaces_reg : list
            List of surfaces to regularized
        mu : float
            Amplitude of the contribution to the :math:`\chi^2`
        """
        self.model = model
        self.pars = model.pars.copy()
        self.mu = mu

        self.ph1_range, self.wl1_range, self.N_eff = None, None, None

        self.surfaces_reg = surfaces_reg

        self.wl_range = np.linspace(self.model.wl_range[0], self.model.wl_range[1],
                                    self.model.basis.bx.nj)
        self.ph_range = np.linspace(self.model.phase_range[0], self.model.phase_range[1],
                                    self.model.basis.by.nj)

        self.SP = self.model.training_dataset.spec_data
        # build the regularization matrix for the spline parameters

    def calculate_n_eff(self):
        """
        Calculate the number of data point per bin of wavelength and phase.
        """
        yy_sp, xx_sp = [], []
        bins = self.wl_range
        for sp in self.model.training_dataset.spectra:
            x_sp = sp.data['Wavelength']/(1+sp.data['ZHelio'])
            y_sp = (sp.data['Date']-self.pars['tmax'].free[sp.data['sn_id']])/(1+sp.data['ZHelio'])
            idx_bins = np.where((x_sp.min() < bins) & (x_sp.max() > bins))
            xx_sp.append(bins[idx_bins])
            yy_sp.append(y_sp[0] * np.ones_like(idx_bins[0]))

        xx_sp = np.hstack(xx_sp)
        yy_sp = np.hstack(yy_sp)

        self.ph1_range = np.hstack((self.ph_range, self.ph_range[-1]+1))
        self.wl1_range = np.hstack((self.wl_range, self.wl_range[-1]+1))

        self.N_eff, _, _ = np.histogram2d(xx_sp, yy_sp, bins=[self.wl1_range, self.ph1_range])
        self.N_eff += 1

    def __call__(self, beta):
        r"""
        Calculate the regularization contribution to the final :math:`\chi^2`

        Parameters
        ----------
        beta : array
            Model parameters.

        Returns
        -------
        v : float
            Value of the :math:`\chi^2_{reg}`
        matrix_free : scipy.sparse.coo_matrix
            :math:`P_{\theta_{0|1}}`
        """
        self.pars.free = beta.free
        self.calculate_n_eff()

        x, y = np.meshgrid(self.wl_range, self.ph_range)
        model_eval = self.model.basis.eval(x.ravel(), y.ravel())
        jacobian_model_eval_wavelength, jacobian_model_eval_phase = self.model.basis.gradient(x.ravel(), y.ravel())

        _, _, hessian_model_eval_phase = self.model.basis.hessian(x.ravel(), y.ravel())

        ddiag = jacobian_model_eval_wavelength * jacobian_model_eval_phase - model_eval * hessian_model_eval_phase

        jacobian_model_eval_phase.data *= jacobian_model_eval_phase.data * self.mu * 0.75/1000  # diff or not
        jacobian_model_eval_wavelength.data *= jacobian_model_eval_wavelength.data * self.mu
        jacobian_model_eval_phase.data /= self.N_eff.ravel()[jacobian_model_eval_phase.row]
        jacobian_model_eval_wavelength.data /= self.N_eff.ravel()[jacobian_model_eval_wavelength.row]

        ddiag.data *= self.mu/self.N_eff.ravel()[ddiag.tocoo().row]  # diff or not

        matrix = (jacobian_model_eval_phase + jacobian_model_eval_wavelength + ddiag)
        matrix = matrix.tocoo()
        n_pars = len(self.pars.free)
        matrix_free = coo_matrix((np.zeros_like(matrix.data), (matrix.row, matrix.col)), shape=(n_pars, n_pars))

        if 'M0' in self.surfaces_reg:
            i = self.pars['M0'].indexof(matrix.row)
            j = self.pars['M0'].indexof(matrix.col)
            idx = (i >= 0) & (j >= 0)
            matrix_free0 = coo_matrix((matrix.data[idx], (i[idx], j[idx])), shape=(n_pars, n_pars))
            matrix_free += matrix_free0

        if 'M1' in self.surfaces_reg:
            # n1 = len(self.pars['M1'].full)
            i1 = self.pars['M1'].indexof(matrix.row)
            j1 = self.pars['M1'].indexof(matrix.col)
            idx1 = (i1 >= 0) & (j1 >= 0)
            matrix_free1 = coo_matrix((matrix.data[idx1], (i1[idx1], j1[idx1])), shape=(n_pars, n_pars))
            matrix_free += matrix_free1

        pp = self.pars.copy()
        pp.release()
        n_pars = len(self.pars.full)
        matrix_full = coo_matrix((np.zeros_like(matrix.data), (matrix.row, matrix.col)), shape=(n_pars, n_pars))

        if 'M0' in self.surfaces_reg:
            i = self.pars['M0'].indexof(matrix.row)
            j = self.pars['M0'].indexof(matrix.col)
            idx = (i >= 0) & (j >= 0)
            matrix_full0 = coo_matrix((matrix.data[idx], (i[idx], j[idx])), shape=(n_pars, n_pars))
            matrix_full += matrix_full0

        if 'M1' in self.surfaces_reg:
            # n1 = len(self.pars['M1'].full)
            i1 = self.pars['M1'].indexof(matrix.row)
            j1 = self.pars['M1'].indexof(matrix.col)
            idx1 = (i1 >= 0) & (j1 >= 0)
            matrix_full1 = coo_matrix((matrix.data[idx1], (i1[idx1], j1[idx1])), shape=(n_pars, n_pars))
            matrix_full += matrix_full1

        self.matrix_full = matrix_full
        self.matrix_free = matrix_free

        v = np.dot(self.pars.full.T, self.matrix_full * self.pars.full)
        return v, self.matrix_free
