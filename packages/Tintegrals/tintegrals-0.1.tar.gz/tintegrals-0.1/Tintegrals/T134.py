import numpy as np
from functools import lru_cache
from scipy.special import spence
from .config import cond
from .OneLoop import B0fin, B0del
import cmath

@lru_cache(maxsize=150)
def T134uv2(m1: float, m2: float, m3: float) -> float:
    """ Computes the double UV poles ($\\propto 1/\\epsilon^2$) of the T134 integral.

    Args:
        m1: first mass
        m2: second mass
        m3: third mass

    Returns:
        value of double UV pole
    """
    try:
        return .5*(m1**2 + m2**2 + m3**2)
    except Exception as e:
        raise Exception(f"There was an error when evaluating the T134uv2 integral with masses {m1}, {m2}, {m3} from {e}")

@lru_cache(maxsize=150)
def T134uv1(m1: float, m2: float, m3: float) -> float:
    """ Computes the single UV pole ($\\propto 1/\\epsilon$) of the T134 integral.

    Args:
        m1: first mass
        m2: second mass
        m3: third mass

    Returns:
        value of single UV pole
    """
    try:
        m1sq = m1**2
        m2sq = m2**2
        m3sq = m3**2
        return .5*(m1sq + m2sq + m3sq) + m1sq*B0fin(0,0,m1sq) + m2sq*B0fin(0,0,m2sq) + m3sq*B0fin(0,0,m3sq)
    except Exception as e:
        raise Exception(f"There was an error when evaluating the T134uv1 integral with masses {m1}, {m2}, {m3} from {e}")

@lru_cache(maxsize=150)
def T134fin(m1: float, m2: float, m3: float) -> float:
    """ Computes the UV finite part of the T134 integral.

    Args:
        m1: first mass
        m2: second mass
        m3: third mass

    Returns:
        value of the finite part
    """
    try:
        m1sq = m1**2
        m2sq = m2**2
        m3sq = m3**2
        return m1sq + m2sq + m3sq \
            + m1sq*B0del(0,0,m1sq) + m2sq*B0del(0,0,m2sq) + m3sq*B0del(0,0,m3sq) \
            + m1sq*B0fin(0,0,m1sq) + m2sq*B0fin(0,0,m2sq) + m3sq*B0fin(0,0,m3sq) \
            + .5*(m1sq*B0fin(0,0,m1sq)**2 + m2sq*B0fin(0,0,m2sq)**2 + m3sq*B0fin(0,0,m3sq)**2) \
            + PhiCyc(m1sq, m2sq, m3sq)
    except Exception as e:
         raise Exception(f"There was an error when evaluating the T134fin integral with masses {m1}, {m2}, {m3} from {e}")

@lru_cache(maxsize=150)
def Li2(x: float) -> float:
    """ Computes $\\rm{Li}_2(x)$. """
    return spence(1-x)

@lru_cache(maxsize=150)
def PhiCyc(m1sq: float, m2sq: float, m3sq: float) -> float:
    """ Computes cyclic Phi function entering T134fin

    Args:
        m1sq: first squared mass
        m2sq: second squared mass
        m3sq: third squared mass

    Returns:
        value of PhyCyc
    """
    m1, m2, m3 = np.sqrt(m1sq), np.sqrt(m2sq), np.sqrt(m3sq)
    if cond(m1, 0) and cond(m2, 0) and cond(m3, 0):
        return 0
    elif cond(m1, 0) and cond(m2, 0):
        return m3sq*np.pi**2/6
    elif cond(m1, 0) and cond(m3, 0):
        return m2sq*np.pi**2/6
    elif cond(m2, 0) and cond(m3, 0):
        return m1sq*np.pi**2/6
    elif cond(m1, 0):
        return m2sq*Li2((m2sq - m3sq)/m2sq) + m3sq*Li2((m3sq - m2sq)/m3sq)
    elif cond(m2, 0):
        return m1sq*Li2((m1sq - m3sq)/m1sq) + m3sq*Li2((m3sq - m1sq)/m3sq)
    elif cond(m3, 0):
        return m1sq*Li2((m1sq - m2sq)/m1sq) + m2sq*Li2((m2sq - m1sq)/m2sq)
    else:
        # use cmath log and sqrt here to avoid issues with imaginary R
        R = cmath.sqrt(m1sq**2 + m2sq**2 + m3sq**2 - 2*m1sq*m2sq - 2*m2sq*m3sq - 2*m3sq*m1sq)
        res = - .5*m1sq*cmath.log(m1sq/m2sq)*cmath.log(m1sq/m3sq) \
              - .5*m2sq*cmath.log(m2sq/m3sq)*cmath.log(m2sq/m1sq) \
              - .5*m3sq*cmath.log(m3sq/m1sq)*cmath.log(m3sq/m2sq) \
              + R*(cmath.pi**2/6 - .5*cmath.log(m1sq/m3sq)*cmath.log(m2sq/m3sq) \
                   + cmath.log((m1sq - m2sq + m3sq - R)/(2*m3sq))*cmath.log((m2sq - m1sq + m3sq - R)/(2*m3sq)) \
                   - Li2((m1sq - m2sq + m3sq - R)/(2*m3sq)) - Li2((m2sq - m1sq + m3sq - R)/(2*m3sq)))
        return res.real