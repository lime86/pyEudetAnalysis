###############################################################################################################################
#
#        Analysis constants: detector caracteristics and usefull constants
#
###############################################################################################################################

import future_builtins
SensorType=future_builtins.SensorType
Assembly=future_builtins.Assembly

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

# global calibration constants
# taken from the draft of the calibration note on 26 Jan 2015
if Assembly == "B06-W0126":
    print "Taking calibration constants for B06-W0126"
    globalCalib_a = 29.79
    globalCalib_b = 534.1
    globalCalib_c = 1817.0
    globalCalib_t = 0.6562

elif Assembly == "A06-W0110":
    print "Taking calibration constants for A06-W0110"
    # the eight point fit, not yet including data from LNLS
    globalCalib_a = 13.89
    globalCalib_b = 333.2
    globalCalib_c = 1220
    globalCalib_t = -0.07229

elif Assembly == "D09-W0126":
    print "Taking calibration constants for D09-W0126"
    globalCalib_a = 17.46
    globalCalib_b = 451.4
    globalCalib_c = 1090.0
    globalCalib_t = 1.958

elif Assembly == "B07-W0125":
    print "Taking calibration constants for B07-W0125"
    globalCalib_a = 14.63
    globalCalib_b = 368.2
    globalCalib_c = 1624.0
    globalCalib_t = -0.1656

elif Assembly == "L04-W0125":
    print "Taking calibration constants for L04-W0125"
    globalCalib_a = 15.3
    globalCalib_b = 374.7
    globalCalib_c = 1000.0
    globalCalib_t = 2.018

elif Assembly == "C04-W0110":
    print "Taking calibration constants for C04-W0110"
    globalCalib_a = 13.18
    globalCalib_b = 398.5
    globalCalib_c = 3822.0
    globalCalib_t = -9.067

else:
    print "Assembly not defined or not recognised. No calibration constants loaded."
    future_builtins.Assembly="AssemblyNotDefined"

# Elementary charge
echarge=1.60217646e-19 # [C=As]
