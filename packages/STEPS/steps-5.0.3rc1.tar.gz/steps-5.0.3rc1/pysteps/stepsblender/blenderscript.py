###___license_placeholder___###

import pickle
import sys

if __name__ == '__main__':
    # Not using argparse here because this module is not meant to be ran by users
    paramPath, sitepackages = sys.argv[sys.argv.index('--') + 1:]

    sys.path.append(sitepackages)

    from stepsblender.blenderloader import HDF5BlenderLoader

    with open(paramPath, 'rb') as f:
        parameters = pickle.load(f)

    ld = HDF5BlenderLoader(parameters=parameters)
