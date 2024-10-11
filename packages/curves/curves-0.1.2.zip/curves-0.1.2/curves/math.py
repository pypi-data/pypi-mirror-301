# -*- coding: utf-8 -*-

# curves
# ------
# functional curve algebra (created by auxilium)
#
# Author:
# Version:  0.1, copyright Thursday, 10 October 2024
# Website:  https://github.com//curves
# License:  Apache License 2.0 (see LICENSE file)


import math

from .curves import Curve


def ramp(x): return max(0, x)


def step(x): return 1 if 0 <= x else 0


ramp = Curve(ramp)
step = Curve(step)

e = math.e
inf = math.inf
nan = math.nan
pi = math.pi

acos = Curve(math.acos)
acosh = Curve(math.acosh)
asin = Curve(math.asin)
asinh = Curve(math.asinh)
atan = Curve(math.atan)
atan2 = Curve(math.atan2)
atanh = Curve(math.atanh)
ceil = Curve(math.ceil)
comb = Curve(math.comb)
copysign = Curve(math.copysign)
cos = Curve(math.cos)
cosh = Curve(math.cosh)
degrees = Curve(math.degrees)
dist = Curve(math.dist)
erf = Curve(math.erf)
erfc = Curve(math.erfc)
exp = Curve(math.exp)
expm1 = Curve(math.expm1)
fabs = Curve(math.fabs)
factorial = Curve(math.factorial)
floor = Curve(math.floor)
fmod = Curve(math.fmod)
frexp = Curve(math.frexp)
fsum = Curve(math.fsum)
gamma = Curve(math.gamma)
gcd = Curve(math.gcd)
hypot = Curve(math.hypot)
isclose = Curve(math.isclose)
isfinite = Curve(math.isfinite)
isinf = Curve(math.isinf)
isnan = Curve(math.isnan)
isqrt = Curve(math.isqrt)
lcm = Curve(math.lcm)
ldexp = Curve(math.ldexp)
lgamma = Curve(math.lgamma)
log = Curve(math.log)
log10 = Curve(math.log10)
log1p = Curve(math.log1p)
log2 = Curve(math.log2)
modf = Curve(math.modf)
nextafter = Curve(math.nextafter)
perm = Curve(math.perm)
pow = Curve(math.pow)
prod = Curve(math.prod)
radians = Curve(math.radians)
remainder = Curve(math.remainder)
sin = Curve(math.sin)
sinh = Curve(math.sinh)
sqrt = Curve(math.sqrt)
tan = Curve(math.tan)
tanh = Curve(math.tanh)
trunc = Curve(math.trunc)
ulp = Curve(math.ulp)
