# -*- coding: utf-8 -*-

# curves
# ------
# functional curve algebra (created by auxilium)
#
# Author:
# Version:  0.1, copyright Thursday, 10 October 2024
# Website:  https://github.com//curves
# License:  Apache License 2.0 (see LICENSE file)


def init(curve):
    if callable(curve):
        return curve
    if not isinstance(curve, (float, int)):
        cls = curve.__class__.__qualname__
        msg = f"float or callable required but type {cls} given"
        raise TypeError(msg)
    return γ(curve)


class γ:

    def __init__(self, curve=None, /, *, op=None, other=None):
        self.curve = curve
        self._inplace_ops = []
        self._op = op
        self._other = other

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
        return repr(self) == repr(other)

    def __copy__(self):
        new = self.__class__(self.curve, op=self._op, other=self._other)
        new._inplace_ops = list(self._inplace_ops)
        return new

    def __repr__(self, /, *, sep=''):
        if self.curve is None:
            s = f"{self.__class__.__name__}()"
        elif callable(self.curve):
            s = f"{getattr(self.curve, '__name__', self.curve)}"
        else:
            s = f"{self.__class__.__name__}({self.curve})"

        if isinstance(self.curve, (int, float, str)):
            s = str(self.curve)

        # for op, other in [(self._op, self._other)]  + self._inplace_ops:
        for op, other in [(self._op, self._other)]:
            if op == 'neg':
                s = f"({s})" if '**' in s else self._embrace(s)
                s = f"-{s}"
            elif op == 'abs':
                # s = f"|{s}|" if ... else f"abs({s})"
                s = f"abs({s})"
            elif op == '@':
                other = getattr(other, '__name__', repr(other))
                s = self._embrace(s)
                s = f"{s}({other})"
            elif op == '**':
                other = getattr(other, '__name__', repr(other))
                other = self._embrace(other)
                s = self._embrace(s)
                s = f"{s} {op} {other}"
            elif op == '*' or op == '/':
                other = getattr(other, '__name__', repr(other))
                other = self._embrace(other, '+-')
                s = self._embrace(s, '+-')
                s = f"{s} {op} {other}"
            elif op is not None:
                other = getattr(other, '__name__', repr(other))
                s = f"{s} {op} {other}"

        for op, other in self._inplace_ops:
            if op not in '+-':
                s = f"({s})"
            other = getattr(other, '__name__', repr(other))
            s = f"{s} {op} {other}"
        return s  # .replace('_', '-')

    def __abs__(self):
        return self.__class__(self, op='abs')

    def __neg__(self):
        return self.__class__(self, op='neg')

    def __add__(self, other):
        return self.__class__(self, op='+', other=init(other))

    def __sub__(self, other):
        return self.__class__(self, op='-', other=init(other))

    def __mul__(self, other):
        return self.__class__(self, op='*', other=init(other))

    def __truediv__(self, other):
        return self.__class__(self, op='/', other=init(other))

    def __pow__(self, power, modulo=None):
        return self.__class__(self, op='**', other=power)

    def __matmul__(self, other):
        return self.__class__(self, op='@', other=init(other))

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

    def clear(self):
        self._op = None
        self._other = None
        self._inplace_ops.clear()


Curve = γ
