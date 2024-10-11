
import scipy.sparse as sparse
import numpy as np
from saltworks.fitparameters import FitParameters


def check_grad(model, pars, dx=1.E-6):
    """
    """
    v, jacobian = model(pars, jac=True)
    pp = pars.copy()
    df = []
    for i in range(len(pp.full)):
        k = pp.indexof(i)
        if k < 0:
            continue
        pp.full[i] += dx
        vp = model(pp, jac=False)
        df.append((vp-v)/dx)
        pp.full[i] -= dx
    return np.array(jacobian.todense()), np.vstack(df).T


def check_deriv(pen, pars, dx=1.E-6):
    """
    """
    v, grad, hess = pen(pars.free, deriv=True)
    pp = pars.copy()

    df, d2f = [], []
    for i in range(len(pp.full)):
        k = pars.indexof(i)
        if k < 0:
            continue
        pp.full[i] += dx
        vp = pen(pp.free, deriv=False)
        pp.full[i] -= (2*dx)
        vm = pen(pp.free, deriv=False)
        df.append((vp-vm)/(2*dx))
        pp.full[i] += dx
    return np.array(grad), np.vstack(df).T


def check_deriv_old(pen, pars, dx=1.E-6):
    """Temporary version, to accomodate the LogLikelihood transitional interface
    """
    v, grad, hess = pen(pars.free, deriv=True)
    pp = pars.copy()

    df, d2f = [], []
    for i in range(len(pp.full)):
        pp.full[i] += dx
        vp = pen(pp.free, deriv=False)
        pp.full[i] -= (2*dx)
        vm = pen(pp.free, deriv=False)
        df.append((vp-vm)/(2*dx))
        pp.full[i] += dx
    return np.array(grad), np.vstack(df).T
