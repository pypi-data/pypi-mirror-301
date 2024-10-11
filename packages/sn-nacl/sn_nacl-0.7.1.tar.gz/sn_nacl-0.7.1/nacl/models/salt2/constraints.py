r"""This module implements the constraints that are needed to train a
nacl.model.SALT2Like model on a dataset.

At variance with the original SALT2 work and with what is described in Guy
Augarde's thesis, we have made a special effort to implement constraints which
are linear.

The contraints are implemented as quadratic penalties that are added to the
:math:`\chi^2`. These penalities are typically of the form:

.. math ::
    (f(\theta) - \alpha)^2

where :math:`f(\theta)` is a function of the parameters, and :math:`\alpha`
is a number.

Since there are several constraints, it is convenient to express them in vector
form:

.. math ::
    (\vec{F}(\theta) - \vec{\alpha})^T \cdot (\vec{F}(\theta) - \vec{\alpha})
"""

import logging
import numpy as np
from scipy.sparse import coo_matrix, dok_matrix


class AllParametersFixedError(Exception): pass


def solve_constraints(cons, pars):
    """
    Solve the linearized constraints for the given parameters.

    This function linearizes the constraints provided by `cons` and solves
    for the parameter adjustments needed to satisfy these constraints.

    Parameters
    ----------
    cons : Constraints
        The constraints object containing the linearized constraints and the right-hand side values.
    pars : Parameters
        The parameters object containing the current values of the parameters.

    Returns
    -------
    numpy.array
        The adjusted free parameters that satisfy the constraints.

    Notes
    -----
    The function uses QR decomposition to solve the linear system of equations formed by the constraints.
    """
    H = cons.get_linearized_constraints(pars.free)
    rhs = cons.get_rhs()
    Q,R = np.linalg.qr(H.T.todense())
    dx = np.linalg.solve(R.T, rhs - H @ pars.full)
    dx = np.array(Q.dot(dx)).squeeze()

    pp = pars.copy()
    pp.full[:] = dx

    return pp.free


def ab_flux_at_10Mpc(Mb=-19.5):
    """
    Calculate the AB flux at a distance of 10 Megaparsecs.

    Parameters
    ----------
    Mb : float, optional
        The absolute magnitude in the B-band (default is -19.5).

    Notes
    -----
    The formula used is `10**(-0.4 * (30 + Mb))`, where 30 is the distance modulus
    for 10 Megaparsecs.
    """
    return 10**(-0.4 * (30+Mb))


class Constraint:
    """
    Represents a constraint in the NaCl optimization problem.

    This class is used to define and apply constraints to the parameters
    of a model during optimization.
    """
    def __init__(self, model, rhs):
        """
        Initialize the Constraint class.

        Parameters
        ----------
        model : object
            The model to which the constraints are applied.
        rhs : numpy.array
            The right-hand side of the constraint equations.
        """
        self.model = model
        self.rhs = rhs

    def __call__(self, p=None, deriv=False):
        """
        Evaluate the constraint function or its derivative.

        Parameters
        ----------
        p : numpy.array, optional
            The parameters at which to evaluate the constraint (default is None).
        deriv : bool, optional
            If True, return the derivative of the constraint (default is False).

        Returns
        -------
        None
            This method should be implemented to return the constraint value or its derivative.
        """
        pass


class LinearConstraint(Constraint):
    """
    Generic linear constraints for a model.

    This class represents linear constraints applied to a model's parameters,
    ensuring that certain conditions are met during optimization.

    Parameters
    ----------
    model : object
        The model to which the constraints are applied.
    rhs : numpy.array
        The right-hand side of the constraint equations.
    """
    def __init__(self, model, rhs):
        """
        Initialize the LinearConstraint class.

        Parameters
        ----------
        model : object
            The model to which the constraints are applied.
        rhs : numpy.array
            The right-hand side of the constraint equations.
        """
        super().__init__(model, rhs)
        self.h_matrix = None
        self.rhs = rhs

    def init_h_matrix(self, pars):
        """
        Initialize the H matrix based on the parameters.

        This method should be implemented by subclasses.

        Parameters
        ----------
        pars : object
            The parameters used to initialize the H matrix.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        raise NotImplementedError()

    def init_pars(self, pars):
        """
        Initialize the constraint with the given parameters.

        Parameters
        ----------
        pars : object
            The parameters used to initialize the constraint.
        """
        self.h_matrix = self.init_h_matrix(pars)

    def __call__(self, pars, deriv=False):
        """
        Evaluate the constraint and optionally its derivatives.

        Parameters
        ----------
        pars : object
            The parameters at which to evaluate the constraint.
        deriv : bool, optional
            If True, return the derivative of the constraint (default is False).

        Returns
        -------
        float
            The value of the constraint.
        tuple
            If deriv is True, returns a tuple containing the constraint value, the H matrix, and None.
        """
        if self.h_matrix is None:
            self.h_matrix = self.init_h_matrix(pars)

        cons = self.h_matrix @ pars.full - self.rhs
        cons = float(cons)
        if not deriv:
            return cons
        return cons, self.h_matrix, None


class ConstraintSet:
    """Combine a series of constraints (linear or not)

    This class combines a set of constraints and produces a (quadratic)
    penality, added to the Log Likelihood. Compute the gradient and the hessian
    of this penality if required.
    """

    def __init__(self, constraints, mu=1.E10):
        """constructor
        """
        # self.model = model
        self.constraints = constraints
        self.mu = mu

    def init_pars(self, pars):
        """
        """
        for c in self.constraints:
            c.init_pars(pars)

    def __call__(self, pars, deriv=False):
        """evaluate the penality
        """
        npars = len(pars.full)

        pen = 0.
        # if no derivatives specified, return the sum of the quadratic
        # penalities associated with each constraint
        if not deriv:
            for cons in self.constraints:
                pen += cons(pars, deriv=False)**2
            return self.mu * float(pen)

        # otherwise, compute and return the gradient and hessian
        # along with the quadratic penality
        grad = coo_matrix(([], ([], [])), shape=(1,npars))
        hess = coo_matrix(([], ([],[])), shape=(npars,npars))
        for cons in self.constraints:
            # p=None, because self.model.pars was just updated
            c, dc, d2c = cons(pars, deriv=True)
            pen  += c**2
            # we have restored the true grad convention (-2 -> +2)
            grad += +2. * float(c) * dc
            hess += +2. * dc.T.dot(dc)
            if d2c is not None:
                hess += 2. * c * d2c

        # fixed parameters ?
        idx = pars.indexof() >= 0
        pen = float(pen)
        grad = np.array(grad[:,idx].todense()).squeeze()
        hess = hess[:,idx][idx,:]

        return self.mu * pen, self.mu * grad, self.mu * hess

    def get_rhs(self):
        return np.array([c.rhs for c in self.constraints])


class int_M0_at_phase_cons(LinearConstraint):
    """constraint on the integral of the M0 surface at peak

    This function builds a linear constraint on the M0 parameters.

    .. note:: at this stage, the constraints are a function of the *full*
       parameter vector, not just the free parameters.
    """
    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase

    def init_h_matrix(self, pars):
        J_phase = self.model.basis.by.eval(np.array([self.phase])).toarray()
        pp = pars.copy()
        pp.release()
        gram_dot_filter = self.model.get_gram_dot_filter()
        C = coo_matrix(np.outer(J_phase, gram_dot_filter).ravel())
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        i = np.full(len(C.col), 0)
        j = pp['M0'].indexof(C.col)
        M = coo_matrix((C.data, (i, j)), shape=(1, npars))
        M.data *= (self.model.norm / self.model.int_ab_spec)
        return M


class int_dM0_at_phase_cons(LinearConstraint):
    """constraint on the integral of the phase derivatives of M0 at peak
    """
    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase
    def init_h_matrix(self, pars):
        J_dphase = self.model.basis.by.deriv(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter()
        C = coo_matrix(np.outer(J_dphase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['M0'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data # / self.model.int_M0_phase_0 # (1.E5 * self.model.int_ab_spec)
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        M.data *= (self.model.norm)
        return M


class int_M1_at_phase_cons(LinearConstraint):
    """constraint on the integral of the M1 surface at peak
    """
    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase
    def init_h_matrix(self, pars):
        J_phase = self.model.basis.by.eval(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter()
        C = coo_matrix(np.outer(J_phase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['M1'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data   #/ model.int_M0_phase_0
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        M.data *= self.model.norm
        return M


class int_dM1_at_phase_cons(LinearConstraint):
    """constraint on the integral of the phase derivatives of M1 at peak
    """
    def __init__(self, model, rhs, phase):
        super().__init__(model, rhs)
        self.phase = phase
    def init_h_matrix(self, pars):
        J_dphase = self.model.basis.by.deriv(np.array([self.phase])).toarray()
        gram_dot_filter = self.model.get_gram_dot_filter()
        C = coo_matrix(np.outer(J_dphase, gram_dot_filter).ravel())
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['M1'].indexof(C.col)
        i = np.full(len(C.col), 0)
        v = C.data  # / model.int_M0_phase_0
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                        shape=(1, npars))
        M.data *= self.model.norm
        return M


class mean_col_cons(LinearConstraint):
    """constraint on the mean of the color parameters
    """
    def __init__(self, model, rhs):
        super().__init__(model, rhs)
    def init_h_matrix(self, pars):
        nsn = len(pars['X0'].full)
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['c'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = np.full(nsn, 1./nsn)
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])), shape=(1, npars))
        return M


class mean_x1_cons(LinearConstraint):
    """constraint on the mean of the x1 parameters
    """
    def __init__(self, model, rhs):
        super().__init__(model, rhs)
    def init_h_matrix(self, pars):
        nsn = len(pars['X0'].full)
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full)
        j = pp['X1'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = np.full(nsn, 1./nsn)
        idx = j >= 0
        M = coo_matrix((v[idx], (i[idx], j[idx])),
                            shape=(1, npars))
        return M


class x1_var_cons(Constraint):

    def __init__(self, model, rhs):
        self.model = model
        self.rhs = rhs

    def __call__(self, pars, deriv=False):
        """
        """
        # if p is not None:
        #     self.model.pars.free = p.free

        # CHECK: do we need all_pars_released, or just self.model.pars ?
        pp = pars.copy()
        pp.release()
        # pars = self.model.all_pars_released
        npars = len(pp.full) # len(self.model.all_pars_released.full)
        nsn = len(pp['X0'].full)

        # constraint function: h(X1) = \sum_i X1**2
        cons = (pp['X1'].full**2).sum() / nsn  # pp or pars ?
        if not deriv:
            return cons

        # first derivatives of h
        pars.full[:] = 0.
        j = pars['X1'].indexof(np.arange(nsn))
        i = np.full(nsn, 0)
        v = pars['X1'].full
        idx = j >= 0
        J = coo_matrix((v[idx], (i[idx], j[idx])), shape=(1, npars)) # was +1

        # second derivatives of h
        i = pars['X1'].indexof(np.arange(nsn))
        v = np.full(nsn, 2./nsn)
        idx = j >= 0
        H = coo_matrix((v[idx], (i[idx], i[idx])), shape=(npars, npars))

        return cons, J, H


def salt2like_linear_constraints(model, mu=1.E6, Mb=-19.5, dm15=1.): # was 0.96
    """
    """
    m0_0 = int_M0_at_phase_cons(model, 14381300.77605067, phase=0.) # ab_flux_at_10Mpc(Mb=Mb),
    dm0_0 = int_dM0_at_phase_cons(model, 0., phase=0.)
    m1_0 = int_M1_at_phase_cons(model, 0., phase=0.)
    m1_15 = int_M1_at_phase_cons(model, dm15, phase=15.)  # rhs was 0.96
    # dm1 = int_dM1_at_phase_cons(model, 0.)
    col = mean_col_cons(model, 0.)
    x1  = mean_x1_cons(model, 0.)
    # x1_var = x1_var_cons(model, 1.)

    return ConstraintSet([m0_0, dm0_0, m1_0, m1_15, col, x1], mu=mu)


def salt2like_classical_constraints(model, mu=1.E6, Mb=-19.5):
    """
    """
    # m0_0 = int_M0_at_phase_cons(model, ab_flux_at_10Mpc(Mb=Mb), phase=0.)
    m0_0 = int_M0_at_phase_cons(model, 14381300.77605067, phase=0.)
    dm0_0 = int_dM0_at_phase_cons(model, 0., phase=0.)
    m1_0 = int_M1_at_phase_cons(model, 0., phase=0.)
    dm1 = int_dM1_at_phase_cons(model, 0.)
    col = mean_col_cons(model, 0.)
    x1  = mean_x1_cons(model, 0.)
    x1_var = x1_var_cons(model, 1.)

    return ConstraintSet(
        model,
        [m0_0, dm0_0, m1_0, dm1, col, x1, x1_var],
        mu=mu)
