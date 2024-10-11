###___license_placeholder___###

from steps import stepslib

__all__ = [
    'RNG',
]


class RNG:
    """Random number generator class

    :param algoStr: Algorithm used to generate random numbers (see below).
    :type algoStr: str
    :param buffSz: Pre-allocated buffer size
    :type buffSz: int
    :param seed: Seed for the random number generator
    :type seed: int

    Available algorithms:
        - ``'mt19937'`` (Mersenne Twister, based on the original mt19937.c)
        - ``'r123'``

    Method and attributes are the same as in :py:class:`steps.API_1.rng.RNG`.
    """

    def __init__(self, algoStr='mt19937', buffSz=512, seed=1):
        self.stepsrng = stepslib._py_rng_create(algoStr, buffSz)
        self.stepsrng.initialize(seed)

    def __getattr__(self, name):
        return getattr(self.stepsrng, name)

    def __call__(self, *args, **kwargs):
        return self.stepsrng.__call__(*args, **kwargs)
