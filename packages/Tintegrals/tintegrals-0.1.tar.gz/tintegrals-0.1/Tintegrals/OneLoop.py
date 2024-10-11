import numpy as np
from functools import lru_cache
from .config import cond

@lru_cache(maxsize=150)
def A0fin(msq: float) -> float:
    """ Computes the UV finite part of the A0 integral.

    Args:
        msq: squared mass

    Returns:
        value of the finite part
    """
    from .config import _mudim
    
    try:
        if cond(msq, 0):
            return 0.0
        else:
            return msq*(1 - np.log(msq/_mudim))
    except Exception as e:
        raise Exception(f"There was an error when evaluating the A0fin integral with arguments {msq} from {e}")


@lru_cache(maxsize=150)
def B0fin(p2: float, m1sq: float, m2sq: float) -> float:
    """ Computes the UV finite part of the B0 integral.
    **Only implemented for zero momentum!**

    Args:
        p2: squared momentum
        m1sq: first squared mass
        m2sq: second squared mass

    Returns:
        value of the finite part
    """
    from .config import _mudim
    
    try:
        if p2 != 0:
            raise ValueError("B0fin only implemented for p2 = 0")
        
        if cond(m1sq, 0) and cond(m2sq, 0):
            return 0
        elif cond(m1sq, 0):
            return 1 - np.log(m2sq/_mudim)
        elif cond(m2sq, 0):
            return 1 - np.log(m1sq/_mudim)
        elif cond(m1sq, m2sq):
            return - np.log(m1sq/_mudim)
        else:
            return (A0fin(m1sq) - A0fin(m2sq))/(m1sq - m2sq)
    except Exception as e:
        raise Exception(f"There was an error when evaluating the B0fin integral with arguments {p2}, {m1sq}, {m2sq} from {e}")


@lru_cache(maxsize=150)
def B0del(p2: float, m1sq: float, m2sq: float) -> float:
    """ Computes the $\\epsilon^1$ part of the B0 integral.
    **Only implemented for zero momentum!**

    Args:
        p2: squared momentum
        m1sq: first squared mass
        m2sq: second squared mass

    Returns:
        value of the $\\epsilon^1$ part if `inclB0del == True`; `0` if `inclB0del == False`
    """
    from .config import _inclB0del, _mudim
    try:
        if not _inclB0del:
            return 0
        
        if p2 != 0:
            raise ValueError("B0del only implemented for p2 = 0")
        
        if cond(m1sq, 0) and cond(m2sq, 0):
            return 0
        elif cond(m1sq, 0):
            return .5 + np.pi**2/12 + .5*(1 - np.log(m2sq/_mudim))**2
        elif cond(m2sq, 0):
            return .5 + np.pi**2/12 + .5*(1 - np.log(m1sq/_mudim))**2
        elif cond(m1sq, m2sq):
            return np.pi**2/12 + .5*np.log(m1sq/_mudim)**2
        else:
            return 1/(m1sq-m2sq)*(m1sq*(.5 + np.pi**2/12 + .5*(1 - np.log(m1sq/_mudim))**2) - m2sq*(.5 + np.pi**2/12 + .5*(1 - np.log(m2sq/_mudim))**2))
    except Exception as e:
        raise Exception(f"There was an error when evaluating the B0del integral with arguments {p2}, {m1sq}, {m2sq} from {e}")


@lru_cache(maxsize=150)
def C0fin(m1sq: float, m2sq: float, m3sq: float) -> float:
    """ Computes the UV finite part of the B0 integral.
    **Only implemented for zero momentum!**

    Args:
        p2: squared momentum
        m1sq: first squared mass
        m2sq: second squared mass

    Returns:
        value of the finite part
    """
    from .config import _mudim
    
    try:
        if cond(m1sq, 0):
            #raise ValueError("C0fin only implemented for m1sq != 0")
            if cond(m2sq,m3sq):
                return -1/m3sq
            elif cond(m2sq,0):
                return 1/m3sq - np.log(m3sq/_mudim)/m3sq
            else: 
                return -np.log(m2sq/m3sq)/(m2sq - m3sq)
        elif cond(m2sq, 0):
            #raise ValueError("C0fin only implemented for m2sq != 0")
            if cond(m1sq,m3sq):
                return -1/m3sq
            elif cond(m3sq,0):
                return 1/m1sq - np.log(m1sq/_mudim)/m1sq
            else: 
                return -np.log(m1sq/m3sq)/(m1sq - m3sq)            
        elif cond(m3sq, 0):
            #raise ValueError("C0fin only implemented for m3sq != 0")
            if cond(m1sq,m2sq):
                return -1/m2sq
            elif cond(m1sq,0):
                return 1/m2sq - np.log(m2sq/_mudim)/m2sq
            else: 
                return -np.log(m1sq/m2sq)/(m1sq - m2sq)            
        elif cond(m1sq, m2sq) and cond(m2sq, m3sq):
            return -1/(2*m1sq)
        elif cond(m1sq, m2sq):
            return (-np.log(m1sq/_mudim) - (A0fin(m1sq) - A0fin(m3sq))/(m1sq - m3sq))/(m1sq - m3sq)
        elif cond(m2sq, m3sq):
            return (-np.log(m2sq/_mudim) - (A0fin(m2sq) - A0fin(m1sq))/(m2sq - m1sq))/(m2sq - m1sq)
        else:
            return ((A0fin(m1sq) - A0fin(m2sq))/(m1sq - m2sq) - (A0fin(m1sq) - A0fin(m3sq))/(m1sq - m3sq))/(m2sq - m3sq)
    except Exception as e:
        raise Exception(f"There was an error when evaluating the C0fin integral with arguments {m1sq}, {m2sq}, {m3sq} from {e}")
