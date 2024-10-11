# -*- coding: utf-8 -*-

###___license_placeholder___###
from __future__ import print_function

import sys

from steps import stepslib

_mpiSuffixes = ['mpi', 'dist']
if not any(stepslib.__name__.endswith(suff) for suff in _mpiSuffixes):
    raise ImportError(
        f'[ERROR] Could not load cysteps_mpi.so. Please verify it exists and system steps was '
        f'built with MPI support.'
    )

# Force stderr flush when an exception is raised.
# Without this, under some conditions, if one process raises a python exception,
# the corresponding message is not always printed out as it should be.
def customHook(tpe, val, bt):
    sys.__excepthook__(tpe, val, bt)
    sys.stderr.flush()
    stepslib.mpiAbort()

sys.excepthook = customHook

stepslib.mpiInit()
import atexit
atexit.register(stepslib.mpiFinish)

rank = stepslib.getRank()
nhosts = stepslib.getNHosts()

import steps
if not steps._quiet and rank == 0:
    print("-----------------------------------------------------------------")
    print("STEPS is running in parallel mode with ", nhosts, " processes")
    print("-----------------------------------------------------------------")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# END
