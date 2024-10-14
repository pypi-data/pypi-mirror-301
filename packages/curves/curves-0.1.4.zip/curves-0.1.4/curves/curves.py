# -*- coding: utf-8 -*-

# curves
# ------
# functional curve algebra (created by auxilium)
#
# Author:   sonntagsgesicht
# Version:  0.1.4, copyright Friday, 11 October 2024
# Website:  https://github.com/sonntagsgesicht/curves
# License:  Apache License 2.0 (see LICENSE file)


def init(curve):
    """initialize Curve instance

    :param curve: item to initialize,
        i.e. turn into a |Curve| instance if **curve** isn't already one.
    :return: |Curve| instance

    >>> from curves import init

    for functions

    >>> from math import exp
    >>> f = init(exp)
    >>> f
    exp

    >>> type(f)
    <class 'curves.curves.Curve'>

    >>> f == exp
    False

    >>> f is init(f)
    True

    for functions numbers

    >>> n = init(1.23)
    >>> n
    1.23

    >>> type(n)
    <class 'curves.curves.Curve'>

    >>> n == 1.23
    False

    >>> n is init(n)
    True

    """
    if isinstance(curve, Curve):
        return curve
    if callable(curve):
        return Curve(curve)
    if not isinstance(curve, (float, int, str)):
        cls = curve.__class__.__qualname__
        msg = f"float or callable required but type {cls} given"
        raise TypeError(msg)
    return Curve(curve)


class Curve:

    def __init__(self, curve=None, /, *, _op=None, _other=None):
        """Curve object with algebraic operations

        :param curve: inner curve or curve value or curve variable

        This turns any function (aka curve) into an algebraic object
        which can handle operators +, -, * , / and @.

        >>> from curves import Curve

        >>> eye = Curve()  # identity function
        >>> eye(123.456)
        123.456

        >>> zero = Curve(0.0)  # constant function
        >>> zero(123.456)
        0.0

        >>> one = Curve(1.0)
        >>> one(123.456)
        1.0

        >>> X = Curve('X')  # variable
        >>> X
        X

        >>> p = 2 * X ** 2 + 3 * X + 1
        >>> p
        2 * X ** 2 + 3 * X + 1

        >>> p(123.456)
        30854.135872

        >>> q = p(X - 1)
        >>> q
        (2 * X ** 2 + 3 * X + 1)(X - 1)

        >>> q1 = p @ (X - 1)
        >>> q1
        (2 * X ** 2 + 3 * X + 1)(X - 1)

        >>> q2 = 2 * (X - 1) ** 2 + 3 * (X - 1) + 1
        >>> q2
        2 * (X - 1) ** 2 + 3 * (X - 1) + 1

        >>> q(123.456)
        30359.311872

        >>> q1(123.456)
        30359.311872

        >>> q2(123.456)
        30359.311872

        and for constant curves

        >>> int(Curve(1))
        1

        >>> float(Curve(1))
        1.0

        >>> int(Curve(1.7))
        1

        >>> float(Curve(1.7))
        1.7

        """
        self.curve = curve
        self._inplace_ops = []
        self._op = _op
        self._other = _other

    @staticmethod
    def _apply(op, other=None, x=None, y=None):
        try:
            match op:
                case 'abs':
                    return abs(y)
                case 'neg':
                    return -y
                case '+':
                    return y + other(x)
                case '-':
                    return y - other(x)
                case '*':
                    return y * other(x)
                case '/':
                    return y / other(x)
                case '**':
                    return y ** other
                case '@':
                    return other(x)
        except TypeError as e:
            raise TypeError(f"{y} {op} [{other}]({x}) failed for {e}")

        raise ValueError(f"operation {op} not fount.")

    @staticmethod
    def _embrace(s, ops='+-/*'):
        s = str(s)
        if not any(f" {_} " in s for _ in ops):
            return s
        ignore = '(|abcdefghijklmnopqrstuvwxyz'
        if (any(s.lower().startswith(_) for _ in ignore)
                and not s.startswith('X')):
            return s
        return f"({s})"

    def _repr(self, /, *, sep='', use_repr=True):
        r = repr if use_repr else str
        if self.curve is None:
            s = f"{self.__class__.__name__}()"
        elif callable(self.curve):
            s = f"{getattr(self.curve, '__name__', r(self.curve))!s}"
        elif use_repr:
            s = f"{self.__class__.__name__}({self.curve}!r)"
        else:
            s = f"{self.__class__.__name__}({self.curve}!s)"

        if isinstance(self.curve, (int, float, str)):
            s = str(self.curve)

        # for op, other in [(self._op, self._other)]  + self._inplace_ops:
        for op, other in [(self._op, self._other)]:
            if op == 'neg':
                s = f"({sep}{s}{sep})" if '**' in s else self._embrace(s)
                s = f"-{s}"
            elif op == 'abs':
                s = f"abs({sep}{s}{sep})" if use_repr or sep else f"|{s}|"
            elif op == '@':
                other = getattr(other, '__name__', r(other))
                s = self._embrace(s)
                s = f"{s}({sep}{other}{sep})"
            elif op == '**':
                other = getattr(other, '__name__', r(other))
                other = self._embrace(other)
                s = self._embrace(s)
                s = f"{s}{sep} {op} {other}"
            elif op == '*' or op == '/':
                other = getattr(other, '__name__', r(other))
                other = self._embrace(other, '+-')
                s = self._embrace(s, '+-')
                s = f"{s}{sep} {op} {other}"
            elif op is not None:
                other = getattr(other, '__name__', r(other))
                s = f"{s}{sep} {op} {other}"

        for op, other in self._inplace_ops:
            if op not in '+-':
                s = f"({s})"
            other = getattr(other, '__name__', r(other))
            s = f"{s}{sep} {op} {other}"
        return s

    def __call__(self, x):
        if not isinstance(x, (int, float)):
            return self @ x

        if self._op == '@':
            x = self._other(x)

        if self.curve is None or isinstance(self.curve, str):
            y = x
        elif callable(self.curve):
            y = self.curve(x)
        else:
            y = self.curve

        if self._op and not self._op == '@':
            op, other = self._op, self._other
            y = self._apply(op, other, x, y)

        for op, other in self._inplace_ops:
            if op == '@':
                y = self._apply(op, other, y)
            else:
                y = self._apply(op, other, x, y)
        return y

    def __eq__(self, other):
        return (repr(self) == repr(other)
                and type(self) == type(other)   # noqa E721
                and self.curve == other.curve)

    def __copy__(self):
        new = self.__class__(self.curve, _op=self._op, _other=self._other)
        new._inplace_ops = list(self._inplace_ops)
        return new

    def __int__(self):
        return int(self.curve)

    def __float__(self):
        return float(self.curve)

    def __str__(self):
        s = self._repr(use_repr=False)
        return s if len(s) < 80 else self._repr(sep='\n', use_repr=False)

    def __repr__(self):
        s = self._repr()
        return s if len(s) < 80 else self._repr(sep='\n')

    def __abs__(self):
        return self.__class__(self, _op='abs')

    def __neg__(self):
        return self.__class__(self, _op='neg')

    def __add__(self, other):
        return self.__class__(self, _op='+', _other=init(other))

    def __sub__(self, other):
        return self.__class__(self, _op='-', _other=init(other))

    def __mul__(self, other):
        return self.__class__(self, _op='*', _other=init(other))

    def __truediv__(self, other):
        return self.__class__(self, _op='/', _other=init(other))

    def __pow__(self, power, modulo=None):
        return self.__class__(self, _op='**', _other=power)

    def __matmul__(self, other):
        return self.__class__(self, _op='@', _other=init(other))

    def __radd__(self, other):
        cls = self.__class__
        return cls(other).__add__(self)

    def __rsub__(self, other):
        cls = self.__class__
        return cls(other).__sub__(self)

    def __rmul__(self, other):
        cls = self.__class__
        return cls(other).__mul__(self)

    def __rtruediv__(self, other):
        cls = self.__class__
        return cls(other).__truediv__(self)

    def __rmatmul__(self, other):
        cls = self.__class__
        return cls(other).__matmul__(self)

    def __iadd__(self, other):
        if self._inplace_ops:
            op, oth = self._inplace_ops[-1]
            if op == '-' and oth == init(other):
                self._inplace_ops.pop(-1)
                return self
        self._inplace_ops.append(('+', init(other)))
        return self

    def __isub__(self, other):
        if self._inplace_ops:
            op, oth = self._inplace_ops[-1]
            if op == '+' and oth == init(other):
                self._inplace_ops.pop(-1)
                return self
        self._inplace_ops.append(('-', init(other)))
        return self

    def __imul__(self, other):
        if self._inplace_ops:
            op, oth = self._inplace_ops[-1]
            if op == '/' and oth == init(other):
                self._inplace_ops.pop(-1)
                return self
        self._inplace_ops.append(('*', init(other)))
        return self

    def __itruediv__(self, other):
        if self._inplace_ops:
            op, oth = self._inplace_ops[-1]
            if op == '*' and oth == init(other):
                self._inplace_ops.pop(-1)
                return self
        self._inplace_ops.append(('/', init(other)))
        return self

    def __ipow__(self, other):
        self._inplace_ops.append(('**', other))
        return self

    def __imatmul__(self, other):
        self._inplace_ops.append(('@', init(other)))
        return self
