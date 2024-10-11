import gc
import functools

_inclB0del = True
_mudim = 1
_releps = 1e-10
_diffeps = 1e-12

def clearCache() -> None:
    """ Clears the cache. """
    gc.collect()
    objects = [i for i in gc.get_objects() 
            if isinstance(i, functools._lru_cache_wrapper)]
    for object in objects:
        object.cache_clear()

def setInclB0del(inclB0del: bool) -> None:
    """ Sets whether B0del is calculated (`True`) or set to zero (`False`).
    The default is `True`.

    Args:
        inclB0del: determines whether B0del is calculated (`True`) or set to zero (`False`).
    """
    clearCache()
    global _inclB0del
    _inclB0del = inclB0del

def getInclB0del() -> bool:
    """ Returns whether B0del is calculated (`True`) or set to zero (`False`).

    Returns:
        `inclB0del`
    """
    return _inclB0del

def setMudim(mudim: float) -> None:
    """ Sets squared renormalization scale.
    The default is `1`.

    Args:
        mudim: squared renormalization scale
    """
    clearCache()
    global _mudim
    _mudim = mudim

def getMudim() -> float:
    """ Returns squared renormalization scale.

    Returns:
        squared renormalization scale
    """
    return _mudim

def setReleps(releps: float) -> None:
    """ Sets releps.
    The default is `1e-10`.

    Args:
        releps: relative epsilon used in `cond`
    """
    clearCache()
    global _releps
    _releps = releps

def getReleps() -> float:
    """ Get releps.

    Returns:
        relative epsilon used in `cond`
    """
    return _releps

def setDiffeps(diffeps: float) -> None:
    """ Sets diffeps.
    The default is `1e-12`.

    Args:
        diffeps: relative epsilon used in `cond`
    """
    clearCache()
    global _diffeps
    _diffeps = diffeps

def getDiffeps() -> float:
    """ Get diffeps.

    Returns:
        difference epsilon used in `cond`
    """
    return _diffeps

def cond(m1: float, m2: float) -> bool:
    """ Condition to return wheter m1 and m2 are degenerate.

    Args:
        m1: first mass
        m2: second mass

    Returns:
        `True` if `abs(m1 - m2) < max(releps*(m1 + m2), diffeps)`, `False` otherwise.
        `releps` and `diffeps` can be set using `setReleps` and `setDiffeps`.
    """
    return abs(m1 - m2) < max(_releps*(m1 + m2), _diffeps)