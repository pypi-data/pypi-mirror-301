###___license_placeholder___###
from __future__ import print_function
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pyqtgraph.Qt import QtCore, QtGui

def pickColorF():
    """
    Pick a color and return it as a (0,1) floating point [r,g,b,a] list
        
    Parameters:
        None
        
    Return:
        List of the color
    """
    col = QtGui.QColorDialog.getRgba()
    qcolor = QtGui.QColor.fromRgba(col[0])
    return [qcolor.redF(), qcolor.greenF(), qcolor.blueF(), qcolor.alphaF()]

def printColorF():
    """
    Pick a color and print(out the list)
        
    Parameters:
        None
        
    Return:
        None
    """
    print(pickColorF())
