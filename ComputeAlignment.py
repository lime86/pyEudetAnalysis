# Will process a tbtrack file
# Will produce an alignment file
# For options, run:
# python ComputeAlignment.py -h

from math import fsum
import time,os
from optparse import OptionParser
import future_builtins

parser = OptionParser()
parser.add_option("-r", "--run",
                  help="Run number", dest="RUN", type="int")

parser.add_option("-n", "--nevent",
                  help="Number of events to process", dest="NEVENT")

parser.add_option("-m", "--method",
                  help="Position reconstruction method (QWeighted, DigitalCentroid, maxTOT, EtaCorrection)", dest="METHOD", default="QWeighted")

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
    
if(options.METHOD) :
    if(options.METHOD=="QWeighted"):
        method_name=options.METHOD
    elif(options.METHOD=="maxTOT"):
        method_name=options.METHOD
    elif(options.METHOD=="DigitalCentroid"):
        method_name=options.METHOD
    elif(options.METHOD=="EtaCorrection"):
        method_name=options.METHOD
    else :
        print "Please provide a valid cluster position reconstruction method (-m [method])"
        parser.print_help()
        exit()

else:
    print "Please provide a valid cluster position reconstruction method (-m [method])"
    parser.print_help()
    exit()

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

if(("Timepix" in options.SENSOR) or options.SENSOR=="CLICpix" or options.SENSOR=="FEI4"):
    future_builtins.SensorType=options.SENSOR
else :
    print "Please provide known sensor name. Timepix/Timepix3 (default) or CLICpix"
    parser.print_help()
    exit()

if(options.DUTID) :
    dutID = int(options.DUTID)
else :
    dutID=6


future_builtins.Assembly="AssemblyNotDefined"
if(options.ASSEMBLY) :
    future_builtins.Assembly=options.ASSEMBLY
else :
    future_builtins.Assembly="AssemblyNotDefined"
    print "Assembly not defined. You will not get calibrated data."

os.system("mkdir %s/Run%i"%(PlotPath,RunNumber))

from ROOT import *

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
        n_proc= int(options.NEVENT)
        print "WARNING it is strongly recommended to use all events in the run (-n -1)"
        print "WARNING this ensures the best alignment for the whole run"
else:
    n_proc= aDataSet.t_nEntries

if n_proc > 10000:
    skip = int((n_proc)/10000.)
else:
    skip = 1
print "Running on run %i, with method %s, on %i events with skip %i" %(RunNumber,method_name,n_proc,skip)

AlignmentPath = "%s/Run%i/alignment_%i_%s_%i_%i.txt" %(PlotPath,RunNumber,RunNumber,method_name,int(options.NEVENT),skip)
print "Alignment path will be", AlignmentPath

prev_pixel_xhits = [999, 999]
clusters_tmp = []
last_time=time.time()

# Load hot pixels
hotpixel_filename = "%s/Run%i/HotPixels_%i_0.01.txt" %(PlotPath,RunNumber,RunNumber)
print "Hotpixel filename:", hotpixel_filename
if os.path.isfile(hotpixel_filename):
    aDataSet.LoadHotPixel(hotpixel_filename)
else:
    print "WARNING no hot pixel file found. No hot pixels set"

for i in range(0,n_proc) :
    aDataSet.getEvent(i)

    # is this a new pixel map?
    npixels_hit = len(aDataSet.p_col)
    pixel_x_hits = []
    for k in xrange(npixels_hit):
        pixel_x_hits.append(aDataSet.p_col[k])

    if (pixel_x_hits == prev_pixel_xhits ):
        # same pixel map as before, will add clusters already computed
        aDataSet.AllClusters.append(clusters_tmp)
    else:
        # this is a new event, will cluster
        #etacorr_sigma = 0.003 # 50um
        #etacorr_sigma = 0.005 # 100um
        #etacorr_sigma = 0.004 # 150um
        etacorr_sigma = 0.009 # 200um
        #etacorr_sigma = 0.013 # 300um
        #etacorr_sigma = 0.010 # 500um
        aDataSet.ClusterEvent(i, method_name, etacorr_sigma)
        clusters_tmp = aDataSet.AllClusters[i]
    prev_pixel_xhits = pixel_x_hits

    aDataSet.GetTrack(i)
    if i%1000 ==0 :
        print "Event %d"%i
        print "Elapsed time/1000 Event. Clustering : %f s"%(time.time()-last_time)
        last_time = time.time()

last_time=time.time()

tccorx1,tccory1 = TrackClusterCorrelation(aDataSet, dutID,n_proc)
tccorx1.SetName("tccorx1")
tccory1.SetName("tccory1")
cantccorx1 = TCanvas()
tccorx1.Draw("colz")
cantccory1 = TCanvas()
tccory1.Draw("colz")

print "Performing prealignment"

if future_builtins.SensorType=="Timepix3" or future_builtins.SensorType=="CLICpix": 
    print "WARNING adding 180 degree rotation around Z for Timepix3 and CLICpix data"
    print "WARNING please fix this if this is not what is wanted"
    alignment_constants, prealix, prealiy = PerformPreAlignment(aDataSet,n_proc,skip,AlignmentPath,dutID,[0,0,180])
else :
    alignment_constants, prealix, prealiy = PerformPreAlignment(aDataSet,n_proc,skip,AlignmentPath, dutID,[0,0,0])

canprealix = TCanvas()
prealix.Draw()
canprealiy = TCanvas()
prealiy.Draw()

distances_histo_afterpreali = TH1F("distances_histo_afterpreali","",100,0.0,1.0)

last_time = time.time()

for i in range(0,n_proc) :

    for alignment in alignment_constants :
        ApplyAlignment_at_event(i,aDataSet,[alignment[3],alignment[4],0],[alignment[0],alignment[1],alignment[2]], dutID)

    aDataSet.FindMatchedCluster(i,searchRadiusPreAlignment, dutID,distances_histo_afterpreali)
    a,b=aDataSet.ComputeResiduals(i, dutID)
    if i%1000 ==0 :
        print "Event %d"%i
        print "Elapsed time/1000 Event. Apply Alignment and TrackMatching : %f s"%(time.time()-last_time)
        last_time = time.time()

candist = TCanvas()
candist.SetLogy()
distances_histo_afterpreali.GetXaxis().SetTitle("Track-cluster distance (mm)")
distances_histo_afterpreali.Draw()

tccorx2,tccory2 = TrackClusterCorrelation(aDataSet, dutID,n_proc)
tccorx2.SetName("tccorx2")
tccory2.SetName("tccory2")
cancorx2 = TCanvas()
tccorx2.Draw("colz")
cancory2 = TCanvas()
tccory2.Draw("colz")

max_matched_dist = searchRadiusAlignment
resr,rest = PerformAlignement(aDataSet,n_proc,skip,max_matched_dist,AlignmentPath,dutID)
ApplyAlignment(aDataSet,rest,resr,dutID)

tccorx3,tccory3 = TrackClusterCorrelation(aDataSet, dutID,n_proc)
tccorx3.SetName("tccorx3")
tccory3.SetName("tccory3")
cancorx3 = TCanvas()
tccorx3.Draw("colz")
cancory3 = TCanvas()
tccory3.Draw("colz")


n_matched = 0
distances_histo_afterfullali = TH1F("distances_histo_afterfullali","",100,0.0,1.0)

for i in range(0,n_proc) :

    aDataSet.FindMatchedCluster(i,searchRadius, dutID,distances_histo_afterfullali)
    a,b=aDataSet.ComputeResiduals(i, dutID)
    n_matched+=a
    if i%1000 ==0 :
        print "Event %d"%i
        print "Elapsed time/1000 Event. Apply Alignment and TrackMatching : %f s"%(time.time()-last_time)
        last_time = time.time()

candist2 = TCanvas()
candist2.SetLogy()
distances_histo_afterfullali.GetXaxis().SetTitle("Track-cluster distance (mm)")
distances_histo_afterfullali.Draw()
      
resX_hist = TH1F("resX_hist","",100,-0.5,0.5)
resY_hist = TH1F("resY_hist","",100,-0.5,0.5)
resX2hit_hist = TH1F("resX2hit_hist","",100,-0.1,0.1)
resY2hit_hist = TH1F("resY2hit_hist","",100,-0.1,0.1)
for i,clusters in enumerate(aDataSet.AllClusters[0:n_proc]) :
    for cluster in clusters :
        for track in aDataSet.AllTracks[i] :
            resX_hist.Fill(cluster.absX - track.trackX[track.iden.index(dutID)])
            resY_hist.Fill(cluster.absY - track.trackY[track.iden.index(dutID)])
            if cluster.size==2:
                if cluster.sizeX==2 and cluster.sizeY==1:
                    resX2hit_hist.Fill(cluster.absX - track.trackX[track.iden.index(dutID)])
                if cluster.sizeX==1 and cluster.sizeY==2:
                    resY2hit_hist.Fill(cluster.absY - track.trackY[track.iden.index(dutID)])

c_resX = TCanvas()
resX_hist.Fit("gaus")
resX_hist.Draw()
c_resX.Update()
resX = resX_hist.GetListOfFunctions()[0].GetParameter(2)

c_resY = TCanvas()
resY_hist.Fit("gaus")
resY_hist.Draw()
c_resY.Update()
resY = resY_hist.GetListOfFunctions()[0].GetParameter(2)

c_resX2hit = TCanvas()
resX2hit_hist.Fit("gaus")
resX2hit_hist.Draw()
c_resX2hit.Update()
resX2hit = resX2hit_hist.GetListOfFunctions()[0].GetParameter(2)

c_resY2hit = TCanvas()
resY2hit_hist.Fit("gaus")
resY2hit_hist.Draw()
c_resY2hit.Update()
resY2hit = resY2hit_hist.GetListOfFunctions()[0].GetParameter(2)

print "Found %i matched track-cluster binome"%n_matched
print "resX", resX
print "resY", resY
print "sqrt(resX**2 + resY**2)", sqrt(resX**2 + resY**2)
print "resX2hit", resX2hit
print "resY2hit", resY2hit
print "sqrt(resX2hit**2 + resY2hit**2)", sqrt(resX2hit**2 + resY2hit**2)

print "Writing alignment constants to file", AlignmentPath
f = open(AlignmentPath,'a')
f.write("Rotation : %f %f %f [deg] Trans : %f %f  [mm] \n"%(resr[0],resr[1],resr[2],rest[0],rest[1]))
f.close()

# Write all histograms to output root file
out = TFile("%s/Run%i/AlignmentPlots_%i_%s_%i_%i.root" %(PlotPath,RunNumber,RunNumber,method_name,int(options.NEVENT),skip), "recreate")
tccorx1.Write()
tccory1.Write()
tccorx2.Write()
tccory2.Write()
tccorx3.Write()
tccory3.Write()
prealix.Write()
prealiy.Write()
distances_histo_afterpreali.Write()
distances_histo_afterfullali.Write()
resX_hist.Write()
resY_hist.Write()
resX2hit_hist.Write()
resY2hit_hist.Write()
out.Close()
