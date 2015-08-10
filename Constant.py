###############################################################################################################################
#
#        Analysis constants: detector caracteristics and usefull constants
#
###############################################################################################################################

import future_builtins
SensorType=future_builtins.SensorType
Assembly=future_builtins.Assembly
from os import environ, path
#import ToolBox

# this should really stay in ToolBox, why can't I import it?
def ReadCalibFile(calibFile):
    from ROOT import TFile
    a = [[ 0. for x in xrange(npix_X)] for x in xrange(npix_Y)]
    b = [[ 0. for x in xrange(npix_X)] for x in xrange(npix_Y)]
    c = [[ 0. for x in xrange(npix_X)] for x in xrange(npix_Y)]
    t = [[ 0. for x in xrange(npix_X)] for x in xrange(npix_Y)]
    
    rootfile = TFile(calibFile)
    tree = rootfile.Get("fitPara")

    for entry in tree:
        col = int(tree.pixx)
        row = int(tree.pixy)

        a[col][row] = tree.a
        b[col][row] = tree.b
        c[col][row] = tree.c
        t[col][row] = tree.d

    return a,b,c,t

if "Timepix" in SensorType :
# Timepix Specifications
    pitchX = 0.055
    pitchY = 0.055
    npix_X = 256
    npix_Y = 256
    
    print "Using Timepix or Timepix3 detector"
    

elif SensorType=="CLICpix" : 
# CLICPix Specifications
    pitchX = 0.025
    pitchY = 0.025
    npix_X = 64
    npix_Y = 64
    
    print "Using CLICpix detector"


halfChip_X = npix_X*pitchX/2.
halfChip_Y = npix_Y*pitchY/2.

# sigma = 0.015
um = 1e-3
mm = 1
cm =10


someData_in_um = 1000*um

scaler =1

home = environ['HOME']

# calibration constants
if Assembly == "B06-W0126":
    print "Taking calibration constants for B06-W0126"
    globalCalib_a = 30.8
    globalCalib_b = 484.3
    globalCalib_c = 1301.0
    globalCalib_t = 1.65

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/B06-W0125_KDECalibration_Pixels.root" %home
    if path.isfile(pixelCalib_file):
        pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)
    else:
        print "Error, can't find pixel calibration file. You probably need to mount eos. Read README."
        exit()

elif Assembly == "A06-W0110":
    print "Taking calibration constants for A06-W0110"
    globalCalib_a = 12.76
    globalCalib_b = 399.3
    globalCalib_c = 2104.0
    globalCalib_t = -1.663

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/A06-W0110_KDECalibration_Pixels.root" %home
    if path.isfile(pixelCalib_file):
        pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)
    else:
        print "Error, can't find pixel calibration file. You probably need to mount eos. Read README."
        exit()

elif Assembly == "D09-W0126":
    print "Taking calibration constants for D09-W0126"
    globalCalib_a = 17.49
    globalCalib_b = 449.6
    globalCalib_c = 1132.0
    globalCalib_t = 1.727

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/D09-W0126_KDECalibration_Pixels.root" %home
    if path.isfile(pixelCalib_file):
        pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)
    else:
        print "Error, can't find pixel calibration file. You probably need to mount eos. Read README."
        exit()

elif Assembly == "B07-W0125":
    print "Taking calibration constants for B07-W0125"
    globalCalib_a = 14.1
    globalCalib_b = 405.7
    globalCalib_c = 2148.0
    globalCalib_t = -1.408

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/B07-W0125_KDECalibration_Pixels.root" %home
    if path.isfile(pixelCalib_file):
        pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)
    else:
        print "Error, can't find pixel calibration file. You probably need to mount eos. Read README."
        exit()

elif Assembly == "L04-W0125":
    print "Taking calibration constants for L04-W0125"
    globalCalib_a = 15.36
    globalCalib_b = 414.0
    globalCalib_c = 2026.0
    globalCalib_t = -1.043

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/L04-W0125_KDECalibration_Pixels.root" %home
    if path.isfile(pixelCalib_file):
        pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)
    else:
        print "Error, can't find pixel calibration file. You probably need to mount eos. Read README."
        exit()

elif Assembly == "C04-W0110":
    print "Taking calibration constants for C04-W0110"
    globalCalib_a = 14.56
    globalCalib_b = 289.4
    globalCalib_c = 869.3
    globalCalib_t = 0.4814

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/C04-W0110_KDECalibration_Pixels.root" %home
    if path.isfile(pixelCalib_file):
        pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)
    else:
        print "Error, can't find pixel calibration file. You probably need to mount eos. Read README."
        exit()

else:
    print "Assembly not defined or not recognised. No calibration constants loaded."
    future_builtins.Assembly="AssemblyNotDefined"
