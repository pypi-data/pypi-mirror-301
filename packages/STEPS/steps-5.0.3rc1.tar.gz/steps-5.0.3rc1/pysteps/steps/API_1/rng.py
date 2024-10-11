###___license_placeholder___###

from steps import stepslib

class RNG(stepslib._py_RNG): 
    """
    Base class for all random number generators in STEPS.
    """
    pass



#Static func
create = stepslib._py_rng_create
create_mt19937 = stepslib._py_rng_create_mt19937

