import re
from .elements import elements

__all__ = ['molecular_weight']


def _find_end(tokens):
    """
    Find index of closing parenthesis.

    Parameters
    ----------
    tokens : list of str
        List of strings representing molecular formula.

    Return
    ------
    idx : int
        Index of closing parenthesis.
    """
    count = 0

    for idx, t in enumerate(tokens):
        if t == ')':
            count -= 1
            if count == 0:
                return idx
        elif t == '(':
            count += 1

    raise ValueError('Unmatched parentheses')


def _parse(tokens, stack):
    """
    Parse items in formula list. Get atomic weight of each item or multiply by
    number of elements. Final value is molecular weight of the formula.

    Parameters
    ----------
    tokens : list of str
        List of strings representing molecular formula.
    stack : list of float
        Molecular weights of each element in formula.

    Returns
    -------
    mw : float
        Sum of molecular weights from molecular formula.
    """
    if len(tokens) == 0:
        mw = sum(stack)
        return mw

    t = tokens[0]

    if t == '(':
        end = _find_end(tokens)
        stack.append(_parse(tokens[1:end], []))
        return _parse(tokens[end + 1:], stack)
    elif t in elements:
        stack.append(elements[t]['atomic_weight'])
    elif t.isdigit():
        stack[-1] *= int(t)

    return _parse(tokens[1:], stack)


def molecular_weight(formula):
    """
    Tokenize a molecular formula to determine total molecular weight.
    Calculation is based on atomic weight values from IUPAC [1]_.

    Parameters
    ----------
    formula : str
        Molecular formula or element.

    Returns
    -------
    mw : float
       Molecular weight of the formula or element [g/mol]

    Examples
    --------
    >>> molecular_weight('C')
    12.011

    >>> molecular_weight('CH4')
    16.04

    >>> molecular_weight('(NH4)2SO4')
    132.13

    References
    ----------
    .. [1] IUPAC Periodic Table of the Elements. International Union of Pure
       and Applied Chemistry, 2016.
       https://iupac.org/what-we-do/periodic-table-of-elements/.
    """
    tokens = re.findall(r'[A-Z][a-z]*|\d+|\(|\)', formula)
    mw = _parse(tokens, [])
    return mw