###############################################################################################################################
#
#        Analysis constants: detector caracteristics and usefull constants
#
###############################################################################################################################

import future_builtins
SensorType=future_builtins.SensorType
Assembly=future_builtins.Assembly
from os import environ
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
    
    searchRadiusPreAlignment = 0.3 #search radius for tracks in mm  
    searchRadiusAlignment = 0.1 #search radius for tracks in mm
    searchRadius = 0.1 #search radius for tracks in mm

    
    print "Using Timepix or Timepix3 detector"


elif SensorType=="FEI4" : 
# CLICPix Specifications
    pitchX = 0.250
    pitchY = 0.050
    npix_X = 80
    npix_Y = 336
    
    print "Using FEI4 detector"

    searchRadiusPreAlignment = 0.8 #search radius for tracks in mm  
    searchRadiusAlignment = 0.4 #search radius for tracks in mm
    searchRadius = 0.4 #search radius for tracks in mm

   

elif SensorType=="CLICpix" : 
# CLICPix Specifications
    pitchX = 0.025
    pitchY = 0.025
    npix_X = 64
    npix_Y = 64
    
    print "Using CLICpix detector"

    searchRadiusPreAlignment = 0.3 #search radius for tracks in mm  
    searchRadiusAlignment = 0.1 #search radius for tracks in mm
    searchRadius = 0.1 #search radius for tracks in mm

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
    globalCalib_a = 30.07
    globalCalib_b = 513.4
    globalCalib_c = 1793.0
    globalCalib_t = 0.4356

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/B06-W0125_KDECalibration_Pixels.root" %home
    pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)

elif Assembly == "A06-W0110":
    print "Taking calibration constants for A06-W0110"
    globalCalib_a = 13.45
    globalCalib_b = 351.4
    globalCalib_c = 1249.0
    globalCalib_t = 0.2151

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/A06-W0110_KDECalibration_Pixels.root" %home
    pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)

elif Assembly == "D09-W0126":
    print "Taking calibration constants for D09-W0126"
    globalCalib_a = 16.72
    globalCalib_b = 499.8
    globalCalib_c = 1805.0
    globalCalib_t = 0.125

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/D09-W0126_KDECalibration_Pixels.root" %home
    pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)

elif Assembly == "B07-W0125":
    print "Taking calibration constants for B07-W0125"
    globalCalib_a = 14.04
    globalCalib_b = 424.3
    globalCalib_c = 2366.0
    globalCalib_t = -1.637

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/B07-W0125_KDECalibration_Pixels.root" %home
    pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)

elif Assembly == "L04-W0125":
    print "Taking calibration constants for L04-W0125"
    globalCalib_a = 15.58
    globalCalib_b = 382.7
    globalCalib_c = 1756.0
    globalCalib_t = -0.6598

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/L04-W0125_KDECalibration_Pixels.root" %home
    pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)

elif Assembly == "C04-W0110":
    print "Taking calibration constants for C04-W0110"
    globalCalib_a = 14.1
    globalCalib_b = 292.3
    globalCalib_c = 780.2
    globalCalib_t = 1.074

    pixelCalib_file = "%s/eos/clicdp/data/VertexCalibration/LatestResults/C04-W0110_KDECalibration_Pixels.root" %home
    pixelCalib_a,pixelCalib_b,pixelCalib_c,pixelCalib_t = ReadCalibFile(pixelCalib_file)

else:
    print "Assembly not defined or not recognised. No calibration constants loaded."
    future_builtins.Assembly="AssemblyNotDefined"
