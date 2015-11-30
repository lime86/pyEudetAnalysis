# Will process a tbtrack file
# Will produce a hot pixel file
# For options, run:
# python FindHotPixels.py -h

from math import fsum
import time,os
from optparse import OptionParser
import future_builtins

parser = OptionParser()
parser.add_option("-r", "--run",
                  help="Run number", dest="RUN", type="int")

parser.add_option("-n", "--nevent",
                  help="Number of events to process", dest="NEVENT")

parser.add_option("-d", "--data",
                  help="Path to tbtrack input folder", dest="INPUT")

parser.add_option("-o", "--output",
                  help="Path to histograms and results output folder", dest="OUTPUT", default=".")

parser.add_option("-e", "--edge",
                  help="Edge width", dest="EDGE", default=0.0, type="float")

parser.add_option("-s", "--sensor",
                  help="Sensor type", dest="SENSOR", default="Timepix")
parser.add_option("-i", "--dut ID",
                  help="DUT ID", dest="DUTID", type="int", default=6)
parser.add_option("-b", "--assembly",
                  help="Assembly name", dest="ASSEMBLY", default="AssemblyNotDefined")

(options, args) = parser.parse_args()

if(options.RUN) :
    RunNumber = int(options.RUN)
else :
    print "Please provide a run number (-r [run number])"
    parser.print_help()
    exit()

if(options.EDGE) :
    edge_width = float(options.EDGE)
else :
    edge_width = 0.0

if(options.INPUT):
    input_folder=options.INPUT
else :
    print "Please provide path to input folder with tbtrack files (-d [PathToData], put no / at the end)"
    parser.print_help()
    exit()

if(options.OUTPUT):
    PlotPath=options.OUTPUT
else :
    print "Please provide path to output folder for histograms and results (-o [PathToOutput], put no / at the end)"
    parser.print_help()
    exit()
if(options.DUTID) :
    dutID = int(options.DUTID)
else :
    dutID=6

if(("Timepix" in options.SENSOR) or options.SENSOR=="CLICpix"):
    future_builtins.SensorType=options.SENSOR
else :
    print "Please provide known sensor name. Timepix/Timepix3 (default) or CLICpix"
    parser.print_help()
    exit()

future_builtins.Assembly="AssemblyNotDefined"
if(options.ASSEMBLY) :
    future_builtins.Assembly=options.ASSEMBLY
else :
    future_builtins.Assembly="AssemblyNotDefined"
    print "Assembly not defined. You will not get calibrated data."

os.system("mkdir %s/Run%i"%(PlotPath,RunNumber))

from ROOT import *
import ROOT
from ROOT import gStyle
from ROOT import TMath
from ToolBox import *
import pyximport; pyximport.install(pyimport=True)
from EudetData import *
from array import array


gStyle.SetOptStat("nemruoi")
gStyle.SetOptFit(1111)


aDataSet = EudetData("%s/tbtrackrun%06i.root"%(input_folder,RunNumber),50000.0,edge_width,1,RunNumber,"tbtrack")


if(options.NEVENT):
    if int(options.NEVENT) > aDataSet.p_nEntries or int(options.NEVENT) == -1:
        n_proc = aDataSet.p_nEntries
    else:
        n_proc = aDataSet.p_nEntries
        print "WARNING it is strongly recommended to use all events in the run (-n -1)"
        print "WARNING this is the best way to define hot pixels"
        print "WARNING overwriting your choice with -n -1"
else:
    n_proc = aDataSet.p_nEntries

print "Running on run %i, on %i events" %(RunNumber,n_proc)

# Find hot pixels
hotpixel_threshold = 0.01
hotpixel_filename = "%s/Run%i/HotPixels_%i_%i_%0.2f.txt" %(PlotPath,RunNumber,RunNumber,dutID,hotpixel_threshold)
print "Hotpixel filename:", hotpixel_filename
histo_nhits,histo_hit,histo_hot,histo_freq = aDataSet.FindHotPixel(hotpixel_threshold,n_proc,hotpixel_filename,dutID)

cannhits = TCanvas()
histo_nhits.Draw()
cannhits.SaveAs("%s/Run%i/NHitPixels_%i.pdf" %(PlotPath,RunNumber,RunNumber))

canhit = TCanvas()
histo_hit.Draw("colz")
canhit.SaveAs("%s/Run%i/HitPixels_%i.pdf" %(PlotPath,RunNumber,RunNumber))

canhot = TCanvas()
histo_hot.Draw("colz")
canhot.SaveAs("%s/Run%i/HotPixels_%i_%0.2f.pdf" %(PlotPath,RunNumber,RunNumber,hotpixel_threshold))

canfreq = TCanvas()
canfreq.SetLogx()
canfreq.SetLogy()
histo_freq.Draw("")
canfreq.SaveAs("%s/Run%i/FiringFrequency_%i_%0.2f.pdf" %(PlotPath,RunNumber,RunNumber,hotpixel_threshold))

# Write all histograms to output root file
out = TFile("%s/Run%i/hotpixel_rootfile.root"%(PlotPath,RunNumber), "recreate")
out.cd()
histo_nhits.Write()
histo_hit.Write()
histo_hot.Write()
histo_freq.Write()
