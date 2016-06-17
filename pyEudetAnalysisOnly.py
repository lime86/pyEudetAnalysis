# Will process an ntuple created from pyEudetReconstructionOnly.py
# Will produce histograms and an output root file
# For options, run:
# python pyEudetAnalysisOnly.py -h

import time,os
from optparse import OptionParser
import future_builtins

parser = OptionParser()

parser.add_option("-r", "--run",
                  help="Run Number", dest="RUN", type="str")

parser.add_option("-n", "--nevent",
                  help="Number of events to process", dest="NEVENT")

parser.add_option("-m", "--method",
                  help="Position Reconstruction Method, QWeighted, DigitalCentroid, maxTOT, EtaCorrection", dest="METHOD", default="QWeighted")

parser.add_option("-d", "--data",
                  help="pyEudetNtuple Input Folder", dest="INPUT")

parser.add_option("-o", "--output",
                  help="Histograms and results output folder", dest="OUTPUT", default=".")

parser.add_option("-a", "--alignment",
                  help="alignment file", dest="ALIGNMENT", default="Alignment.txt")

parser.add_option("-e", "--edge",
                  help="edge width", dest="EDGE", default=0.0, type="float")

parser.add_option("-s", "--sensor",
                  help="Sensor type", dest="SENSOR", default="Timepix")

parser.add_option("-i", "--dut ID",
                  help="DUT ID", dest="DUTID", type="int", default=6)

parser.add_option("-b", "--assembly",
                  help="Assembly name", dest="ASSEMBLY", default="AssemblyNotDefined")
                  
parser.add_option("-B", "--batch",
                  help="Batch", dest="BATCH", action="store_true", default=False)

(options, args) = parser.parse_args()

if(options.RUN) :
    RunNumber = int(options.RUN)
else :
    print "Please provide a Run Number (-r [Run Number])"
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
        print "Please provide a valid cluster position reconstruction method ( -m [method]  QWeighted,maxTOT,DigitalControid,EtaCorrection)"
        parser.print_help()
        exit()

else:
    print "Please provide a valid cluster position reconstruction method ( -m [method]  QWeighted,maxTOT,DigitalControid,EtaCorrection)"
    parser.print_help()
    exit()

if(options.INPUT):
    input_folder=options.INPUT
else :
    print "Please provide an input folder with pyEudetNtuple files (-d [PathToData] , put no / at the end )"
    parser.print_help()
    exit()

if(options.OUTPUT):
    PlotPath=options.OUTPUT
else :
    print "Please provide an output folder (-o [PathToOutput] , put no / at the end )"
    parser.print_help()
    exit()

if(options.ALIGNMENT):
    AlignementPath = "%s"%(options.ALIGNMENT)
else :
    print "Please provide an Alignment File (-a [PathToFile]  0 0 0 0 0 if no alignement needed )"
    parser.print_help()
    exit()

future_builtins.SensorType= "Timepix"
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
os.system("mkdir %s/Run%i/%s"%(PlotPath,RunNumber,method_name))


from ROOT import *
import ROOT
from ROOT import gStyle
from ROOT import TMath
from ToolBox import *
import pyximport; pyximport.install(pyimport=True)
from EudetData import *
from array import array
gROOT.SetBatch(options.BATCH)

alignment_constants = ReadAlignment(AlignementPath)

def h1_style(h, optstat=0) :
    h.SetStats(optstat)
    h.SetLabelFont(42,"X")
    h.SetLabelFont(42,"Y")
    h.SetLabelOffset(0.005,"X")
    h.SetLabelOffset(0.005,"Y")
    h.SetLabelSize(0.045,"X")
    h.SetLabelSize(0.045,"Y")
    h.SetTitleOffset(1.15,"X")
    h.SetTitleOffset(1.15,"Y")
    h.SetTitleSize(0.04,"X")
    h.SetTitleSize(0.04,"Y")
    #h.SetTitle(0)
    h.SetTitleFont(42, "XYZ")
    
def SquareCanvas(can):
    aspectRatio = pitchX/pitchY

    can.SetWindowSize(int(aspectRatio*1024),1024)

def TGraph_style (h) :
    h.GetXaxis().SetLabelOffset(0.005)
    h.GetXaxis().SetLabelFont(42)
    h.GetXaxis().SetLabelSize(0.055)
    h.GetXaxis().SetTitleOffset(1.15)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleFont(42)
#     h.GetYaxis().SetRangeUser(0.,1.)
    h.GetYaxis().SetLabelOffset(0.005)
    h.GetYaxis().SetLabelFont(42)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetTitleFont(42)
    h.GetYaxis().SetTitleSize(0.04)

gStyle.SetOptStat("nemruoi")
gStyle.SetOptFit(1111)


aDataSet = EudetData("%s/Run%i/%s/pyEudetNtuple_run%i_%s.root"%(input_folder,RunNumber,method_name,RunNumber,method_name),50000.0,edge_width,1,RunNumber,"pyEudetNTuple")
aDataSet.ReadReconstructedData()


# Computing Chi2 cut and plotting Chi2 distribution
h_chi2,h_chi2ndof = aDataSet.GetChi2Cut(0.95,False)

can_chi2 = TCanvas()
h_chi2.Draw("")
can_chi2.SetLogx()
can_chi2.SetLogy()
can_chi2.SaveAs("%s/Run%i/Chi2_Distribution.pdf"%(PlotPath,RunNumber))

can_chi2ndof = TCanvas()
h_chi2ndof.Draw("")
can_chi2ndof.SetLogx()
can_chi2ndof.SetLogy()
can_chi2ndof.SaveAs("%s/Run%i/Chi2nDof_Distribution.pdf"%(PlotPath,RunNumber))


if(options.NEVENT):
    n_proc= int(options.NEVENT)

    if n_proc >= aDataSet.t_nEntries:
        n_proc = -1
    if n_proc == -1:
        n_proc = aDataSet.t_nEntries

else :
    n_proc= aDataSet.t_nEntries

if len(aDataSet.AllTracks)< n_proc :
    print "Only %i events in file"%len(aDataSet.AllTracks)
    n_proc=len(aDataSet.AllTracks)


print "Running on run %i, with Method %s, on %i Events"%(RunNumber,method_name,n_proc)


# ComputeEfficiency
n_matched_in_main = 0
n_matched_in_edge = 0
last_time = time.time()


if (method_name == "EtaCorrection") :
    ressigmacharge, ressigmachargeGC, ressigmachargePbPC = FindSigmaMin(aDataSet,aDataSet.p_nEntries,PlotPath,RunNumber,method_name,10, dutID)

else: 
    ressigmacharge=0.01
    ressigmachargeGC=0.01
    ressigmachargePbPC=0.01

for i in range(n_proc-1) :

    aDataSet.FindMatchedCluster(i,searchRadius,dutID)
    aDataSet.ComputePosition(i,method_name,ressigmacharge,ressigmachargeGC,ressigmachargePbPC)

    m,me = aDataSet.ComputeResiduals(i, dutID)
    n_matched_in_main += m
    n_matched_in_edge += me

    if i%10000 ==0 :
        print "Event %d"%i
        print "Elapsed time/10000 Event : %f s"%(time.time()-last_time)
        last_time = time.time()

print "Found %i matched track-cluster binome in main" %n_matched_in_main
print "And %i matched track-cluster binome in edges" %n_matched_in_edge

ComputeEfficiency(aDataSet,n_matched_in_main,n_matched_in_edge,edge_width,"%s/Run%i/%s"%(PlotPath,RunNumber,method_name), dutID)


# EdgeEfficiency
edge_tracks, edge_matched, edge_efficiencies, edge_tots = EdgeEfficiency(aDataSet,dutID)

eff_can = TCanvas()
edge_efficiencies[0].SetMinimum(0)
edge_efficiencies[0].Draw("")
for i in range(1,4) :
    edge_efficiencies[i].Draw("same")
eff_can.BuildLegend()
eff_can.SaveAs("%s/Run%i/%s/Edge_Efficiency_edge_by_edge.pdf"%(PlotPath,RunNumber,method_name))

edge_matched[0].SetMinimum(0)
edge_matched[0].Draw("")
for i in range(1,4) :
    edge_matched[i].Draw("same")
eff_can.BuildLegend()
eff_can.SaveAs("%s/Run%i/%s/Edge_MatchedTracks_edge_by_edge.pdf"%(PlotPath,RunNumber,method_name))

edge_tracks[0].SetMinimum(0)
edge_tracks[0].Draw("")
for i in range(1,4) :
    edge_tracks[i].Draw("same")
eff_can.BuildLegend()
eff_can.SaveAs("%s/Run%i/%s/Edge_Tracks_edge_by_edge.pdf"%(PlotPath,RunNumber,method_name))

edge_tots[0].Draw("colz")
eff_can.SaveAs("%s/Run%i/%s/Edge_TOT_edge0.pdf"%(PlotPath,RunNumber,method_name))
edge_tots[1].Draw("colz")
eff_can.SaveAs("%s/Run%i/%s/Edge_TOT_edge1.pdf"%(PlotPath,RunNumber,method_name))
edge_tots[2].Draw("colz")
eff_can.SaveAs("%s/Run%i/%s/Edge_TOT_edge2.pdf"%(PlotPath,RunNumber,method_name))
edge_tots[3].Draw("colz")
eff_can.SaveAs("%s/Run%i/%s/Edge_TOT_edge3.pdf"%(PlotPath,RunNumber,method_name))


# CountClusterSize
hClusterSize, hClusterSizeX, hClusterSizeY, hClusterSizeXvsSizeY, hClusterSizeCounter,hClusterSizeCounter_percent = CountClusterSize(aDataSet)

h1_style(hClusterSize)
h1_style(hClusterSizeX)
h1_style(hClusterSizeY)
h1_style(hClusterSizeXvsSizeY)
h1_style(hClusterSizeCounter)
h1_style(hClusterSizeCounter_percent)

cClusterSize = TCanvas()
hClusterSize.Draw()
cClusterSize.SaveAs("%s/Run%i/%s/ClusterSize.pdf"%(PlotPath,RunNumber,method_name))

hClusterSizeX.Draw()
cClusterSize.SaveAs("%s/Run%i/%s/ClusterSizeX.pdf"%(PlotPath,RunNumber,method_name))

hClusterSizeY.Draw()
cClusterSize.SaveAs("%s/Run%i/%s/ClusterSizeY.pdf"%(PlotPath,RunNumber,method_name))

hClusterSizeXvsSizeY.Draw("colz")
cClusterSize.SaveAs("%s/Run%i/%s/ClusterSizeXvsSizeY.pdf"%(PlotPath,RunNumber,method_name))

cClusterSizeCounter = TCanvas()
hClusterSizeCounter.Draw()
cClusterSizeCounter.SetLogy()
cClusterSizeCounter.SaveAs("%s/Run%i/%s/ClusterSizeCounter.pdf"%(PlotPath,RunNumber,method_name))

cClusterSizeCounter_percent = TCanvas()
hClusterSizeCounter_percent.Draw()
cClusterSizeCounter_percent.SetLogy()
cClusterSizeCounter_percent.SaveAs("%s/Run%i/%s/ClusterSizeCounter_percent.pdf"%(PlotPath,RunNumber,method_name))


#for i in range(aDataSet_calib.p_nEntries) :
#===============================================================================
# for i in range(10000) :
#    aDataSet_calib.ClusterEvent(i)
#    if i%1000 ==0 :
#        print "Event %d"%i
#    aDataSet_calib.GetTrack(i)
#    aDataSet_calib.FindMatchedCluster(i, 0.350, 0.350,6)
#
#    aDataSet_calib.ComputeResiduals(i)
#===============================================================================


last_time = time.time()
hx,hy = TrackClusterCorrelation(aDataSet,dutID,n_proc)
print "Elapsed time for Correlation : %f s"%(time.time()-last_time)

h1_style(hx,1)
h1_style(hy,1)

cancorx = TCanvas()
hx.Draw("colz")
cancorx.SaveAs("%s/Run%i/%s/corx.pdf"%(PlotPath,RunNumber,method_name))

cancory = TCanvas()
hy.Draw("colz")
cancory.SaveAs("%s/Run%i/%s/cory.pdf"%(PlotPath,RunNumber,method_name))




relX_vs_relY = TH2D("relX_vs_relY","Hit probability in local coordinates",300,0.,15.,300,0.,15.)
relX_vs_relY.GetXaxis().SetRangeUser(-0.,14.08)
relX_vs_relY.GetXaxis().SetTitle("Cluster relX position within pixel [mm]")
relX_vs_relY.GetYaxis().SetRangeUser(-0.,14.08)
relX_vs_relY.GetYaxis().SetTitle("Cluster relY position within pixel [mm]")

HitProb_1_cluster_binning1m,HitProb_2_cluster_binning1m,HitProb_3_cluster_binning1m,HitProb_4_cluster_binning1m = ClusterHitProb(aDataSet,55,dutID)
HitProb_1_cluster_binning2m,HitProb_2_cluster_binning2m,HitProb_3_cluster_binning2m,HitProb_4_cluster_binning2m = ClusterHitProb(aDataSet,28,dutID)

HitProb_1_correlationX,HitProb_2_correlationX,HitProb_3_correlationX,HitProb_4_correlationX = HitProbCorrelationX(aDataSet,55,dutID)
HitProb_1_correlationY,HitProb_2_correlationY,HitProb_3_correlationY,HitProb_4_correlationY = HitProbCorrelationY(aDataSet,55,dutID)

TOTProfileX_1_cluster_binning1m,TOTProfileX_2_cluster_binning1m,TOTProfileX_3_cluster_binning1m,TOTProfileX_4_cluster_binning1m,TOTProfileY_1_cluster_binning1m,TOTProfileY_2_cluster_binning1m,TOTProfileY_3_cluster_binning1m,TOTProfileY_4_cluster_binning1m,TOTProfileX,TOTProfileY,TOTProfile = TOTProfile(aDataSet,55,dutID)


h1_style(HitProb_1_cluster_binning1m)
h1_style(HitProb_2_cluster_binning1m)
h1_style(HitProb_3_cluster_binning1m)
h1_style(HitProb_4_cluster_binning1m)

h1_style(TOTProfileX_1_cluster_binning1m)
h1_style(TOTProfileX_2_cluster_binning1m)
h1_style(TOTProfileX_3_cluster_binning1m)
h1_style(TOTProfileX_4_cluster_binning1m)
h1_style(TOTProfileY_1_cluster_binning1m)
h1_style(TOTProfileY_2_cluster_binning1m)
h1_style(TOTProfileY_3_cluster_binning1m)
h1_style(TOTProfileY_4_cluster_binning1m)
h1_style(TOTProfileX)
h1_style(TOTProfileY)
h1_style(TOTProfile)

h1_style(HitProb_1_cluster_binning2m)
h1_style(HitProb_2_cluster_binning2m)
h1_style(HitProb_3_cluster_binning2m)
h1_style(HitProb_4_cluster_binning2m)
h1_style(relX_vs_relY)

h1_style(HitProb_1_correlationX)
h1_style(HitProb_2_correlationX)
h1_style(HitProb_3_correlationX)
h1_style(HitProb_4_correlationX)
h1_style(HitProb_1_correlationY)
h1_style(HitProb_2_correlationY)
h1_style(HitProb_3_correlationY)
h1_style(HitProb_4_correlationY)



print "ComputeChargeDistance"
QrelWrtMindistance = ComputeChargeDistance(aDataSet,0.004, dutID)

canEtaCorr = TCanvas()
QrelWrtMindistance.Draw("colz")
QrelWrtMindistance.SetTitle("Relative charge as a function of the track distance to the pixel edge")
QrelWrtMindistance.GetXaxis().SetTitle("Track-pixel edge distance (mm)")
QrelWrtMindistance.GetYaxis().SetTitle("Relative charge")
h1_style(QrelWrtMindistance)
canEtaCorr.SaveAs("%s/Run%i/%s/Eta_hist.pdf"%(PlotPath,RunNumber,method_name))


last_time = time.time()

allTOT = TH1D("allTOT","TOT spectrum, all cluster sizes",5000,0,10000)
TOT1 = TH1D("TOT1","TOT spectrum, cluster size = 1",5000,0,10000)
TOT1.SetLineColor(1)
TOT2 = TH1D("TOT2","TOT spectrum, cluster size = 2",5000,0,10000)
TOT2.SetLineColor(2)
TOT3 = TH1D("TOT3","TOT spectrum, cluster size = 3",5000,0,10000)
TOT3.SetLineColor(3)
TOT4 = TH1D("TOT4","TOT spectrum, cluster size = 4",5000,0,10000)
TOT4.SetLineColor(4)

allEnergyGC = TH1D("allEnergyGC","EnergyGC spectrum, all cluster sizes",5000,0,500)
EnergyGC1 = TH1D("EnergyGC1","EnergyGC spectrum, cluster size = 1",5000,0,500)
EnergyGC1.SetLineColor(1)
EnergyGC2 = TH1D("EnergyGC2","EnergyGC spectrum, cluster size = 2",5000,0,500)
EnergyGC2.SetLineColor(2)
EnergyGC3 = TH1D("EnergyGC3","EnergyGC spectrum, cluster size = 3",5000,0,500)
EnergyGC3.SetLineColor(3)
EnergyGC4 = TH1D("EnergyGC4","EnergyGC spectrum, cluster size = 4",5000,0,500)
EnergyGC4.SetLineColor(4)

allEnergyPbPC = TH1D("allEnergyPbPC","EnergyPbPC spectrum, all cluster sizes",5000,0,500)
EnergyPbPC1 = TH1D("EnergyPbPC1","EnergyPbPC spectrum, cluster size = 1",5000,0,500)
EnergyPbPC1.SetLineColor(1)
EnergyPbPC2 = TH1D("EnergyPbPC2","EnergyPbPC spectrum, cluster size = 2",5000,0,500)
EnergyPbPC2.SetLineColor(2)
EnergyPbPC3 = TH1D("EnergyPbPC3","EnergyPbPC spectrum, cluster size = 3",5000,0,500)
EnergyPbPC3.SetLineColor(3)
EnergyPbPC4 = TH1D("EnergyPbPC4","EnergyPbPC spectrum, cluster size = 4",5000,0,500)
EnergyPbPC4.SetLineColor(4)

resX = TH1D("resX","Unbiased residual X, all clusters",600,-0.150,0.150)
resY = TH1D("resY","Unbiased residual Y, all clusters",600,-0.150,0.150)
resX.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX,1)
h1_style(resY,1)

resX_s1x1y1 = TH1D("resX_s1x1y1","Unbiased residual X, cluster size = 1, sizeX = 1 and sizeY = 1",600,-0.150,0.150)
resY_s1x1y1 = TH1D("resY_s1x1y1","Unbiased residual Y, cluster size = 1, sizeX = 1 and sizeY = 1",600,-0.150,0.150)
resX_s1x1y1.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY_s1x1y1.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX_s1x1y1,1)
h1_style(resY_s1x1y1,1)

resX_s2x2y1 = TH1D("resX_s2x2y1","Unbiased residual X, cluster size = 2, sizeX = 2 and sizeY = 1",600,-0.150,0.150)
resY_s2x2y1 = TH1D("resY_s2x2y1","Unbiased residual Y, cluster size = 2, sizeX = 2 and sizeY = 1",600,-0.150,0.150)
resX_s2x2y1.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY_s2x2y1.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX_s2x2y1,1)
h1_style(resY_s2x2y1,1)

resXGC_s2x2y1 = TH1D("resXGC_s2x2y1","Unbiased residual X, cluster size = 2, sizeX = 2 and sizeY = 1",600,-0.150,0.150)
resXGC_s2x2y1.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
h1_style(resXGC_s2x2y1,1)
resXPbPC_s2x2y1 = TH1D("resXPbPC_s2x2y1","Unbiased residual X, cluster size = 2, sizeX = 2 and sizeY = 1",600,-0.150,0.150)
resXPbPC_s2x2y1.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
h1_style(resXPbPC_s2x2y1,1)

resX_s2x2y1_relX = TH2F("resX_s2x2y1_relX","",100,0.,15.,50,-0.050,0.050)
resY_s2x1y2_relY = TH2F("resY_s2x1y2_relY","",100,0.,15.,50,-0.050,0.050)

resXGC_s2x2y1_relX = TH2F("resXGC_s2x2y1_relX","",100,0.,15.,50,-0.050,0.050)
resYGC_s2x1y2_relY = TH2F("resYGC_s2x1y2_relY","",100,0.,15.,50,-0.050,0.050)

resXPbPC_s2x2y1_relX = TH2F("resXPbPC_s2x2y1_relX","",100,0.,15.,50,-0.050,0.050)
resYPbPC_s2x1y2_relY = TH2F("resYPbPC_s2x1y2_relY","",100,0.,15.,50,-0.050,0.050)

Qrel_s2x2y1 = TH1F("Qrel_s2x2y1","",100,0,1)
Qrel_s2x1y2 = TH1F("Qrel_s2x1y2","",100,0,1)
QrelGC_s2x2y1 = TH1F("QrelGC_s2x2y1","",100,0,1)
QrelGC_s2x1y2 = TH1F("QrelGC_s2x1y2","",100,0,1)
QrelPbPC_s2x2y1 = TH1F("QrelPbPC_s2x2y1","",100,0,1)
QrelPbPC_s2x1y2 = TH1F("QrelPbPC_s2x1y2","",100,0,1)

Qrel_s2x2y1_relX = TH2F("Qrel_s2x2y1_relX","",100,0.,15.,100,0,1)
Qrel_s2x1y2_relY = TH2F("Qrel_s2x1y2_relY","",100,0.,15.,100,0,1)
QrelGC_s2x2y1_relX = TH2F("QrelGC_s2x2y1_relX","",100,0.,15.,100,0,1)
QrelGC_s2x1y2_relY = TH2F("QrelGC_s2x1y2_relY","",100,0.,15.,100,0,1)
QrelPbPC_s2x2y1_relX = TH2F("QrelPbPC_s2x2y1_relX","",100,0.,15.,100,0,1)
QrelPbPC_s2x1y2_relY = TH2F("QrelPbPC_s2x1y2_relY","",100,0.,15.,100,0,1)

resX_s2x1y2 = TH1D("resX_s2x1y2","Unbiased residual X, cluster size = 2, sizeX = 1 and sizeY = 2",600,-0.150,0.150)
resY_s2x1y2 = TH1D("resY_s2x1y2","Unbiased residual Y, cluster size = 2, sizeX = 1 and sizeY = 2",600,-0.150,0.150)
resX_s2x1y2.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY_s2x1y2.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX_s2x1y2,1)
h1_style(resY_s2x1y2,1)

resYGC_s2x1y2 = TH1D("resYGC_s2x1y2","Unbiased residual Y, cluster size = 2, sizeX = 1 and sizeY = 2",600,-0.150,0.150)
resYGC_s2x1y2.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resYGC_s2x1y2,1)
resYPbPC_s2x1y2 = TH1D("resYPbPC_s2x1y2","Unbiased residual Y, cluster size = 2, sizeX = 1 and sizeY = 2",600,-0.150,0.150)
resYPbPC_s2x1y2.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resYPbPC_s2x1y2,1)

resX_s2x2y2 = TH1D("resX_s2x2y2","Unbiased residual X, cluster size = 2, sizeX = 2 and sizeY = 2",600,-0.150,0.150)
resY_s2x2y2 = TH1D("resY_s2x2y2","Unbiased residual Y, cluster size = 2, sizeX = 2 and sizeY = 2",600,-0.150,0.150)
resX_s2x2y2.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY_s2x2y2.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX_s2x2y2,1)
h1_style(resY_s2x2y2,1)

resX_s3x2y2 = TH1D("resX_s3x2y2","Unbiased residual X, cluster size = 3, sizeX = 2 and sizeY = 2",600,-0.150,0.150)
resY_s3x2y2 = TH1D("resY_s3x2y2","Unbiased residual Y, cluster size = 3, sizeX = 2 and sizeY = 2",600,-0.150,0.150)
resX_s3x2y2.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY_s3x2y2.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX_s3x2y2,1)
h1_style(resY_s3x2y2,1)

resX_s4x2y2 = TH1D("resX_s4x2y2","Unbiased residual X, cluster size = 4, sizeX = 2 and sizeY = 2",600,-0.150,0.150)
resY_s4x2y2 = TH1D("resY_s4x2y2","Unbiased residual Y, cluster size = 4, sizeX = 2 and sizeY = 2",600,-0.150,0.150)
resX_s4x2y2.GetXaxis().SetTitle("X_{track} - X_{Timepix} (mm)")
resY_s4x2y2.GetXaxis().SetTitle("Y_{track} - Y_{Timepix} (mm)")
h1_style(resX_s4x2y2,1)
h1_style(resY_s4x2y2,1)

for j,tracks in enumerate(aDataSet.AllTracks) :
    for track in tracks :
        if track.cluster!=-11 and len(aDataSet.AllClusters[j])!=0 :
            aCluster = aDataSet.AllClusters[j][track.cluster]
            allTOT.Fill(aCluster.totalTOT)
            allEnergyGC.Fill(aCluster.totalEnergyGC)
            allEnergyPbPC.Fill(aCluster.totalEnergyPbPC)
            relX_vs_relY.Fill(aCluster.relX,aCluster.relY)
            resX.Fill(aCluster.resX)
            resY.Fill(aCluster.resY)
            if (aCluster.size==1 and (aCluster.sizeX==1 and aCluster.sizeY==1)) :
                resX_s1x1y1.Fill(aCluster.resX)
                resY_s1x1y1.Fill(aCluster.resY)
            elif(aCluster.size==2 and (aCluster.sizeX==2 and aCluster.sizeY==2)) :
                resX_s2x2y2.Fill(aCluster.resX)
                resY_s2x2y2.Fill(aCluster.resY)
            elif(aCluster.size==2 and (aCluster.sizeX==2 and aCluster.sizeY==1)) :
                resX_s2x2y1.Fill(aCluster.resX)
                resY_s2x2y1.Fill(aCluster.resY)
                resX_s2x2y1_relX.Fill(aCluster.relX, aCluster.resX)
                Qrel_s2x2y1.Fill(aCluster.tot[aCluster.col.index(min(aCluster.col))] / aCluster.totalTOT)
                Qrel_s2x2y1_relX.Fill(aCluster.relX,aCluster.tot[aCluster.col.index(min(aCluster.col))] / aCluster.totalTOT)
                if ((aCluster.totalEnergyGC > 0) and (0 not in aCluster.energyGC)):
                    resXGC_s2x2y1.Fill(aCluster.resX_energyGC)
                    resXGC_s2x2y1_relX.Fill(aCluster.relX, aCluster.resX_energyGC)
                    QrelGC_s2x2y1.Fill(aCluster.energyGC[aCluster.col.index(min(aCluster.col))] / aCluster.totalEnergyGC)
                    QrelGC_s2x2y1_relX.Fill(aCluster.relX,aCluster.energyGC[aCluster.col.index(min(aCluster.col))] / aCluster.totalEnergyGC)
                if ((aCluster.totalEnergyPbPC > 0) and (0 not in aCluster.energyPbPC)):
                    resXPbPC_s2x2y1.Fill(aCluster.resX_energyPbPC)
                    resXPbPC_s2x2y1_relX.Fill(aCluster.relX, aCluster.resX_energyPbPC)
                    QrelPbPC_s2x2y1.Fill(aCluster.energyPbPC[aCluster.col.index(min(aCluster.col))] / aCluster.totalEnergyPbPC)
                    QrelPbPC_s2x2y1_relX.Fill(aCluster.relX,aCluster.energyPbPC[aCluster.col.index(min(aCluster.col))] / aCluster.totalEnergyPbPC)
            elif(aCluster.size==2 and (aCluster.sizeX==1 and aCluster.sizeY==2)) :
                resX_s2x1y2.Fill(aCluster.resX)
                resY_s2x1y2.Fill(aCluster.resY)
                resY_s2x1y2_relY.Fill(aCluster.relY, aCluster.resY)
                Qrel_s2x1y2.Fill(aCluster.tot[aCluster.row.index(min(aCluster.row))] / aCluster.totalTOT)
                Qrel_s2x1y2_relY.Fill(aCluster.relY,aCluster.tot[aCluster.row.index(min(aCluster.row))] / aCluster.totalTOT)
                if ((aCluster.totalEnergyGC > 0) and (0 not in aCluster.energyGC)):
                    resYGC_s2x1y2.Fill(aCluster.resY_energyGC)
                    resYGC_s2x1y2_relY.Fill(aCluster.relY, aCluster.resY_energyGC)
                    QrelGC_s2x1y2.Fill(aCluster.energyGC[aCluster.row.index(min(aCluster.row))] / aCluster.totalEnergyGC)
                    QrelGC_s2x1y2_relY.Fill(aCluster.relY,aCluster.energyGC[aCluster.row.index(min(aCluster.row))] / aCluster.totalEnergyGC)
                if ((aCluster.totalEnergyPbPC > 0) and (0 not in aCluster.energyPbPC)):
                    resYPbPC_s2x1y2.Fill(aCluster.resY_energyPbPC)
                    resYPbPC_s2x1y2_relY.Fill(aCluster.relY, aCluster.resY_energyPbPC)
                    QrelPbPC_s2x1y2.Fill(aCluster.energyPbPC[aCluster.row.index(min(aCluster.row))] / aCluster.totalEnergyPbPC)
                    QrelPbPC_s2x1y2_relY.Fill(aCluster.relY,aCluster.energyPbPC[aCluster.row.index(min(aCluster.row))] / aCluster.totalEnergyPbPC)
            elif(aCluster.size==3 and (aCluster.sizeX==2 and aCluster.sizeY==2)) :
                resX_s3x2y2.Fill(aCluster.resX)
                resY_s3x2y2.Fill(aCluster.resY)
            elif(aCluster.size==4 and (aCluster.sizeX==2 and aCluster.sizeY==2)) :
                resX_s4x2y2.Fill(aCluster.resX)
                resY_s4x2y2.Fill(aCluster.resY)

            if(aCluster.size==1) :
                TOT1.Fill(aCluster.totalTOT)
                EnergyGC1.Fill(aCluster.totalEnergyGC)
                EnergyPbPC1.Fill(aCluster.totalEnergyPbPC)
            if(aCluster.size==2) :
                TOT2.Fill(aCluster.totalTOT)
                EnergyGC2.Fill(aCluster.totalEnergyGC)
                EnergyPbPC2.Fill(aCluster.totalEnergyPbPC)
            if(aCluster.size==3) :
                TOT3.Fill(aCluster.totalTOT)
                EnergyGC3.Fill(aCluster.totalEnergyGC)
                EnergyPbPC3.Fill(aCluster.totalEnergyPbPC)
            if(aCluster.size==4) :
                TOT4.Fill(aCluster.totalTOT)
                EnergyGC4.Fill(aCluster.totalEnergyGC)
                EnergyPbPC4.Fill(aCluster.totalEnergyPbPC)
print "Elapsed time for Residual, cluster and TOT plots: %f s"%(time.time()-last_time)

can3 = TCanvas()
resX.Draw("")
resX.Fit("gaus","R","",-0.03,0.03)
can3.SaveAs("%s/Run%i/%s/resX.pdf"%(PlotPath,RunNumber,method_name))

can4 = TCanvas()
resY.Draw("")
resY.Fit("gaus","R","",-0.03,0.03)
can4.SaveAs("%s/Run%i/%s/resY.pdf"%(PlotPath,RunNumber,method_name))

canvas_resX_s1x1y1 = TCanvas()
resX_s1x1y1.Draw()
resX_s1x1y1.Fit("gaus","R","",-0.03,0.03)
canvas_resX_s1x1y1.SaveAs("%s/Run%i/%s/resX_s1x1y1.pdf"%(PlotPath,RunNumber,method_name))

canvas_resY_s1x1y1 = TCanvas()
resY_s1x1y1.Draw()
resY_s1x1y1.Fit("gaus","R","",-0.03,0.03)
canvas_resY_s1x1y1.SaveAs("%s/Run%i/%s/resY_s1x1y1.pdf"%(PlotPath,RunNumber,method_name))

canvas_resX_s2x2y2 = TCanvas()
resX_s2x2y2.Draw()
resX_s2x2y2.Fit("gaus","R","",-0.03,0.03)
canvas_resX_s2x2y2.SaveAs("%s/Run%i/%s/resX_s2x2y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resY_s2x2y2 = TCanvas()
resY_s2x2y2.Draw()
resY_s2x2y2.Fit("gaus","R","",-0.03,0.03)
canvas_resY_s2x2y2.SaveAs("%s/Run%i/%s/resY_s2x2y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resX_s2x2y1 = TCanvas()
resX_s2x2y1.Draw()
resX_s2x2y1.Fit("gaus","R","",-0.03,0.03)
canvas_resX_s2x2y1.SaveAs("%s/Run%i/%s/resX_s2x2y1.pdf"%(PlotPath,RunNumber,method_name))

canvas_resY_s2x2y1 = TCanvas()
resY_s2x2y1.Draw()
resY_s2x2y1.Fit("gaus","R","",-0.03,0.03)
canvas_resY_s2x2y1.SaveAs("%s/Run%i/%s/resY_s2x2y1.pdf"%(PlotPath,RunNumber,method_name))

canvas_resXGC_s2x2y1 = TCanvas()
resXGC_s2x2y1.Draw()
resXGC_s2x2y1.Fit("gaus","R","",-0.03,0.03)
canvas_resXGC_s2x2y1.SaveAs("%s/Run%i/%s/resXGC_s2x2y1.pdf"%(PlotPath,RunNumber,method_name))

canvas_resXPbPC_s2x2y1 = TCanvas()
resXPbPC_s2x2y1.Draw()
resXPbPC_s2x2y1.Fit("gaus","R","",-0.03,0.03)
canvas_resXPbPC_s2x2y1.SaveAs("%s/Run%i/%s/resXPbPC_s2x2y1.pdf"%(PlotPath,RunNumber,method_name))

canvas_resX_s2x2y1_relX = TCanvas()
resX_s2x2y1_relX.Draw("cont4")
canvas_resX_s2x2y1_relX.SaveAs("%s/Run%i/%s/resX_s2x2y1_relX.pdf"%(PlotPath,RunNumber,method_name))

canvas_resXGC_s2x2y1_relX = TCanvas()
resXGC_s2x2y1_relX.Draw("cont4")
canvas_resXGC_s2x2y1_relX.SaveAs("%s/Run%i/%s/resXGC_s2x2y1_relX.pdf"%(PlotPath,RunNumber,method_name))

canvas_resXPbPC_s2x2y1_relX = TCanvas()
resXPbPC_s2x2y1_relX.Draw("cont4")
canvas_resXPbPC_s2x2y1_relX.SaveAs("%s/Run%i/%s/resXPbPC_s2x2y1_relX.pdf"%(PlotPath,RunNumber,method_name))

resX_s2x2y1_relX.FitSlicesY(0, 0, -1, 0, "QNR G5")
resX_s2x2y1_relX_1 = gDirectory.Get("resX_s2x2y1_relX_1")
resX_s2x2y1_relX_2 = gDirectory.Get("resX_s2x2y1_relX_2")

resXGC_s2x2y1_relX.FitSlicesY(0, 0, -1, 0, "QNR G5")
resXGC_s2x2y1_relX_1 = gDirectory.Get("resXGC_s2x2y1_relX_1")
resXGC_s2x2y1_relX_2 = gDirectory.Get("resXGC_s2x2y1_relX_2")

resXPbPC_s2x2y1_relX.FitSlicesY(0, 0, -1, 0, "QNR G5")
resXPbPC_s2x2y1_relX_1 = gDirectory.Get("resXPbPC_s2x2y1_relX_1")
resXPbPC_s2x2y1_relX_2 = gDirectory.Get("resXPbPC_s2x2y1_relX_2")

canvas_resY_s2x1y2_relY = TCanvas()
resY_s2x1y2_relY.Draw("cont4")
canvas_resY_s2x1y2_relY.SaveAs("%s/Run%i/%s/resY_s2x1y2_relY.pdf"%(PlotPath,RunNumber,method_name))

canvas_resYGC_s2x1y2_relY = TCanvas()
resYGC_s2x1y2_relY.Draw("cont4")
canvas_resYGC_s2x1y2_relY.SaveAs("%s/Run%i/%s/resYGC_s2x1y2_relY.pdf"%(PlotPath,RunNumber,method_name))

canvas_resYPbPC_s2x1y2_relY = TCanvas()
resYPbPC_s2x1y2_relY.Draw("cont4")
canvas_resYPbPC_s2x1y2_relY.SaveAs("%s/Run%i/%s/resYPbPC_s2x1y2_relY.pdf"%(PlotPath,RunNumber,method_name))

resY_s2x1y2_relY.FitSlicesY(0, 0, -1, 0, "QNR G5")
resY_s2x1y2_relY_1 = gDirectory.Get("resY_s2x1y2_relY_1")
resY_s2x1y2_relY_2 = gDirectory.Get("resY_s2x1y2_relY_2")

resYGC_s2x1y2_relY.FitSlicesY(0, 0, -1, 0, "QNR G5")
resYGC_s2x1y2_relY_1 = gDirectory.Get("resYGC_s2x1y2_relY_1")
resYGC_s2x1y2_relY_2 = gDirectory.Get("resYGC_s2x1y2_relY_2")

resYPbPC_s2x1y2_relY.FitSlicesY(0, 0, -1, 0, "QNR G5")
resYPbPC_s2x1y2_relY_1 = gDirectory.Get("resYPbPC_s2x1y2_relY_1")
resYPbPC_s2x1y2_relY_2 = gDirectory.Get("resYPbPC_s2x1y2_relY_2")

canvas_resX_s2x1y2 = TCanvas()
resX_s2x1y2.Draw()
resX_s2x1y2.Fit("gaus","R","",-0.03,0.03)
canvas_resX_s2x1y2.SaveAs("%s/Run%i/%s/resX_s2x1y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resY_s2x1y2 = TCanvas()
resY_s2x1y2.Draw()
resY_s2x1y2.Fit("gaus","R","",-0.03,0.03)
canvas_resY_s2x1y2.SaveAs("%s/Run%i/%s/resY_s2x1y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resYGC_s2x1y2 = TCanvas()
resYGC_s2x1y2.Draw()
resYGC_s2x1y2.Fit("gaus","R","",-0.03,0.03)
canvas_resYGC_s2x1y2.SaveAs("%s/Run%i/%s/resYGC_s2x1y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resYPbPC_s2x1y2 = TCanvas()
resYPbPC_s2x1y2.Draw()
resYPbPC_s2x1y2.Fit("gaus","R","",-0.03,0.03)
canvas_resYPbPC_s2x1y2.SaveAs("%s/Run%i/%s/resYPbPC_s2x1y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resX_s3x2y2 = TCanvas()
resX_s3x2y2.Draw()
resX_s3x2y2.Fit("gaus","R","",-0.03,0.03)
canvas_resX_s3x2y2.SaveAs("%s/Run%i/%s/resX_s3x2y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resY_s3x2y2 = TCanvas()
resY_s3x2y2.Draw()
resY_s3x2y2.Fit("gaus","R","",-0.03,0.03)
canvas_resY_s3x2y2.SaveAs("%s/Run%i/%s/resY_s3x2y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resX_s4x2y2 = TCanvas()
resX_s4x2y2.Draw()
resX_s4x2y2.Fit("gaus","R","",-0.03,0.03)
canvas_resX_s4x2y2.SaveAs("%s/Run%i/%s/resX_s4x2y2.pdf"%(PlotPath,RunNumber,method_name))

canvas_resY_s4x2y2 = TCanvas()
resY_s4x2y2.Draw()
resY_s4x2y2.Fit("gaus","R","",-0.03,0.03)
canvas_resY_s4x2y2.SaveAs("%s/Run%i/%s/resY_s4x2y2.pdf"%(PlotPath,RunNumber,method_name))

can1 = TCanvas()
h1_style(allTOT,1)
allTOT.Draw()
can1.SaveAs("%s/Run%i/%s/allTOT.pdf"%(PlotPath,RunNumber,method_name))

h1_style(allEnergyGC,1)
allEnergyGC.Draw()
can1.SaveAs("%s/Run%i/%s/allEnergyGC.pdf"%(PlotPath,RunNumber,method_name))

h1_style(allEnergyPbPC,1)
allEnergyPbPC.Draw()
can1.SaveAs("%s/Run%i/%s/allEnergyPbPC.pdf"%(PlotPath,RunNumber,method_name))


###############################################################################################################################
#
#                        landau * gauss fit, allTOT
#
################################################################################################################################

# #langaufit(allTOT,fr_allTOT,sv_allTOT,pllo_allTOT,plhi_allTOT,fp_allTOT,fpe_allTOT,chisqr_allTOT,ndf_allTOT)
# #
# # allTOT : his               histogram to fit
# # fr_allTOT : fitrange       lo and hi boundaries of fit range
# # sv_allTOT : startvalues    reasonable start values for the fit
# # pllo_allTOT : parlimitslo  lower parameter limits
# # plhi_allTOT : parlimitshi  upper parameter limits
# # fp_allTOT : fitparams      returns the final fit parameters
# # fpe_allTOT : fiterrors     returns the final fit errors
#
#
# fr_allTOT = array('d',[0.2*TOT2.GetMean(),3.0*TOT2.GetMean()])
# sv_allTOT = array('d',[1.8,20.0,50000.0,3.0])
# pllo_allTOT = array('d',[0.5,5.0,1.0,0.4])
# plhi_allTOT = array('d',[5.0,50.0,1000000.0,5.0])
# fp_allTOT = array('d',[0.])
# fpe_allTOT = array('d',[0.])
#
# chisqr_allTOT = array('d',[0.])
# ndf_allTOT = array('i',[0])
# allTOTPeak = ROOT.Double(0.)
# allTOTFWHM = ROOT.Double(0.)
#
#
# fitallTOT = langaufit(allTOT,fr_allTOT,sv_allTOT,pllo_allTOT,plhi_allTOT,fp_allTOT,fpe_allTOT,chisqr_allTOT,ndf_allTOT)
# langaupro(fp_allTOT,allTOTPeak,allTOTFWHM)
#
# print"Fitting done\nPlotting results...\n"
#
#
# canvasTest_allTOT = TCanvas()
# canvasTest_allTOT.cd()
# allTOT.Draw()
# fitallTOT.Draw("lsame")
# canvasTest_allTOT.Update()
# canvasTest_allTOT.SaveAs("%s/Run%i/%s/allTOT_landaugausFit.pdf"%(PlotPath,RunNumber,method_name))

###############################################################################################################################


###############################################################################################################################
#
#                        landau * gauss fit, TOT2
#
################################################################################################################################

# #langaufit(TOT2,fr_TOT2,sv_TOT2,pllo_TOT2,plhi_TOT2,fp_TOT2,fpe_TOT2,chisqr_TOT2,ndf_TOT2)
# #
# # TOT2 : his               histogram to fit
# # fr_TOT2 : fitrange       lo and hi boundaries of fit range
# # sv_TOT2 : startvalues    reasonable start values for the fit
# # pllo_TOT2 : parlimitslo  lower parameter limits
# # plhi_TOT2 : parlimitshi  upper parameter limits
# # fp_TOT2 : fitparams      returns the final fit parameters
# # fpe_TOT2 : fiterrors     returns the final fit errors
#
# fr_TOT2 = array('d',[0.2*TOT2.GetMean(),3.0*TOT2.GetMean()])
# sv_TOT2 = array('d',[1.8,20.0,50000.0,3.0])
# pllo_TOT2 = array('d',[0.5,5.0,1.0,0.4])
# plhi_TOT2 = array('d',[5.0,50.0,1000000.0,5.0])
# fp_TOT2 = array('d',[0.])
# fpe_TOT2 = array('d',[0.])
#
# chisqr_TOT2 = array('d',[0.])
# ndf_TOT2 = array('i',[0])
# TOT2Peak = ROOT.Double(0.)
# TOT2FWHM = ROOT.Double(0.)
#
#
# fitTOT2 = langaufit(TOT2,fr_TOT2,sv_TOT2,pllo_TOT2,plhi_TOT2,fp_TOT2,fpe_TOT2,chisqr_TOT2,ndf_TOT2)
# langaupro(fp_TOT2,TOT2Peak,TOT2FWHM)
#
# print"Fitting done\nPlotting results...\n"
#
#
# canvasTest_TOT2 = TCanvas()
# canvasTest_TOT2.cd()
# TOT2.Draw()
# fitTOT2.Draw("lsame")
# canvasTest_TOT2.Update()
# canvasTest_TOT2.SaveAs("%s/Run%i/%s/TOT2_landaugausFit.pdf"%(PlotPath,RunNumber,method_name))

###############################################################################################################################

###############################################################################################################################
#
#                        landau * gauss fit, TOT4
#
###############################################################################################################################

# #langaufit(TOT4,fr_TOT4,sv_TOT4,pllo_TOT4,plhi_TOT4,fp_TOT4,fpe_TOT4,chisqr_TOT4,ndf_TOT4)
# #
# # TOT4 : his               histogram to fit
# # fr_TOT4 : fitrange       lo and hi boundaries of fit range
# # sv_TOT4 : startvalues    reasonable start values for the fit
# # pllo_TOT4 : parlimitslo  lower parameter limits
# # plhi_TOT4 : parlimitshi  upper parameter limits
# # fp_TOT4 : fitparams      returns the final fit parameters
# # fpe_TOT4 : fiterrors     returns the final fit errors
#
# fr_TOT4 = array('d',[0.2*TOT4.GetMean(),3.0*TOT4.GetMean()])
# sv_TOT4 = array('d',[1.8,20.0,50000.0,3.0])
# pllo_TOT4 = array('d',[0.5,5.0,1.0,0.4])
# plhi_TOT4 = array('d',[5.0,50.0,1000000.0,5.0])
# fp_TOT4 = array('d',[0.])
# fpe_TOT4 = array('d',[0.])
#
# chisqr_TOT4 = array('d',[0.])
# ndf_TOT4 = array('i',[0])
# TOT4Peak = ROOT.Double(0.)
# TOT4FWHM = ROOT.Double(0.)
#
#
# fitTOT4 = langaufit(TOT4,fr_TOT4,sv_TOT4,pllo_TOT4,plhi_TOT4,fp_TOT4,fpe_TOT4,chisqr_TOT4,ndf_TOT4)
# langaupro(fp_TOT4,TOT4Peak,TOT4FWHM)
#
# print"Fitting done\nPlotting results...\n"
#
#
# canvasTest_TOT4 = TCanvas()
# canvasTest_TOT4.cd()
# TOT4.Draw()
# fitTOT4.Draw("lsame")
# canvasTest_TOT4.Update()
# canvasTest_TOT4.SaveAs("%s/Run%i/%s/TOT4_landaugausFit.pdf"%(PlotPath,RunNumber,method_name))

###############################################################################################################################

h1_style(TOT1,1)
h1_style(TOT2,1)
h1_style(TOT3,1)
h1_style(TOT4,1)
h1_style(EnergyGC1,1)
h1_style(EnergyGC2,1)
h1_style(EnergyGC3,1)
h1_style(EnergyGC4,1)
h1_style(EnergyPbPC1,1)
h1_style(EnergyPbPC2,1)
h1_style(EnergyPbPC3,1)
h1_style(EnergyPbPC4,1)

can2=TCanvas()
can2.cd()
TOT1.Draw()
TOT2.Draw("sames")
TOT3.Draw("sames")
TOT4.Draw("sames")
gPad.Update()
st_TOT1 = TOT1.GetListOfFunctions().FindObject("stats")
st_TOT1.SetX1NDC(0.690)
st_TOT1.SetY1NDC(0.623)
st_TOT1.SetX2NDC(0.838)
st_TOT1.SetY2NDC(0.879)
st_TOT1.SetOptStat(111111)
# gPad.Update()
st_TOT2 = TOT2.GetListOfFunctions().FindObject("stats")
st_TOT2.SetX1NDC(0.846)
st_TOT2.SetY1NDC(0.623)
st_TOT2.SetX2NDC(0.984)
st_TOT2.SetY2NDC(0.879)
st_TOT2.SetOptStat(111111)
# gPad.Update()
st_TOT3 = TOT3.GetListOfFunctions().FindObject("stats")
st_TOT3.SetX1NDC(0.690)
st_TOT3.SetY1NDC(0.360)
st_TOT3.SetX2NDC(0.838)
st_TOT3.SetY2NDC(0.616)
st_TOT3.SetOptStat(111111)
# gPad.Update()
st_TOT4 = TOT4.GetListOfFunctions().FindObject("stats")
st_TOT4.SetX1NDC(0.846)
st_TOT4.SetY1NDC(0.360)
st_TOT4.SetX2NDC(0.984)
st_TOT4.SetY2NDC(0.616)
st_TOT4.SetOptStat(111111)
leg2 = TLegend(0.48,0.69,0.68,0.88)
leg2.SetBorderSize(0)
leg2.AddEntry(TOT1,"cluster size 1","l")
leg2.AddEntry(TOT2,"cluster size 2","l")
leg2.AddEntry(TOT3,"cluster size 3","l")
leg2.AddEntry(TOT4,"cluster size 4","l")
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.Draw("SAME")
TOT1.SetTitle("Tot spectrum")
can2.SaveAs("%s/Run%i/%s/TOTnormalized.pdf"%(PlotPath,RunNumber,method_name))

EnergyGC1.Draw()
EnergyGC2.Draw("sames")
EnergyGC3.Draw("sames")
EnergyGC4.Draw("sames")
gPad.Update()
st_EnergyGC1 = EnergyGC1.GetListOfFunctions().FindObject("stats")
st_EnergyGC1.SetX1NDC(0.690)
st_EnergyGC1.SetY1NDC(0.623)
st_EnergyGC1.SetX2NDC(0.838)
st_EnergyGC1.SetY2NDC(0.879)
st_EnergyGC1.SetOptStat(111111)
# gPad.Update()
st_EnergyGC2 = EnergyGC2.GetListOfFunctions().FindObject("stats")
st_EnergyGC2.SetX1NDC(0.846)
st_EnergyGC2.SetY1NDC(0.623)
st_EnergyGC2.SetX2NDC(0.984)
st_EnergyGC2.SetY2NDC(0.879)
st_EnergyGC2.SetOptStat(111111)
# gPad.Update()
st_EnergyGC3 = EnergyGC3.GetListOfFunctions().FindObject("stats")
st_EnergyGC3.SetX1NDC(0.690)
st_EnergyGC3.SetY1NDC(0.360)
st_EnergyGC3.SetX2NDC(0.838)
st_EnergyGC3.SetY2NDC(0.616)
st_EnergyGC3.SetOptStat(111111)
# gPad.Update()
st_EnergyGC4 = EnergyGC4.GetListOfFunctions().FindObject("stats")
st_EnergyGC4.SetX1NDC(0.846)
st_EnergyGC4.SetY1NDC(0.360)
st_EnergyGC4.SetX2NDC(0.984)
st_EnergyGC4.SetY2NDC(0.616)
st_EnergyGC4.SetOptStat(111111)
leg2 = TLegend(0.48,0.69,0.68,0.88)
leg2.SetBorderSize(0)
leg2.AddEntry(EnergyGC1,"cluster size 1","l")
leg2.AddEntry(EnergyGC2,"cluster size 2","l")
leg2.AddEntry(EnergyGC3,"cluster size 3","l")
leg2.AddEntry(EnergyGC4,"cluster size 4","l")
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.Draw("SAME")
EnergyGC1.SetTitle("EnergyGC spectrum")
can2.SaveAs("%s/Run%i/%s/EnergyGCnormalized.pdf"%(PlotPath,RunNumber,method_name))

EnergyPbPC1.Draw()
EnergyPbPC2.Draw("sames")
EnergyPbPC3.Draw("sames")
EnergyPbPC4.Draw("sames")
gPad.Update()
st_EnergyPbPC1 = EnergyPbPC1.GetListOfFunctions().FindObject("stats")
st_EnergyPbPC1.SetX1NDC(0.690)
st_EnergyPbPC1.SetY1NDC(0.623)
st_EnergyPbPC1.SetX2NDC(0.838)
st_EnergyPbPC1.SetY2NDC(0.879)
st_EnergyPbPC1.SetOptStat(111111)
# gPad.Update()
st_EnergyPbPC2 = EnergyPbPC2.GetListOfFunctions().FindObject("stats")
st_EnergyPbPC2.SetX1NDC(0.846)
st_EnergyPbPC2.SetY1NDC(0.623)
st_EnergyPbPC2.SetX2NDC(0.984)
st_EnergyPbPC2.SetY2NDC(0.879)
st_EnergyPbPC2.SetOptStat(111111)
# gPad.Update()
st_EnergyPbPC3 = EnergyPbPC3.GetListOfFunctions().FindObject("stats")
st_EnergyPbPC3.SetX1NDC(0.690)
st_EnergyPbPC3.SetY1NDC(0.360)
st_EnergyPbPC3.SetX2NDC(0.838)
st_EnergyPbPC3.SetY2NDC(0.616)
st_EnergyPbPC3.SetOptStat(111111)
# gPad.Update()
st_EnergyPbPC4 = EnergyPbPC4.GetListOfFunctions().FindObject("stats")
st_EnergyPbPC4.SetX1NDC(0.846)
st_EnergyPbPC4.SetY1NDC(0.360)
st_EnergyPbPC4.SetX2NDC(0.984)
st_EnergyPbPC4.SetY2NDC(0.616)
st_EnergyPbPC4.SetOptStat(111111)
leg3 = TLegend(0.48,0.69,0.68,0.88)
leg3.SetBorderSize(0)
leg3.AddEntry(EnergyPbPC1,"cluster size 1","l")
leg3.AddEntry(EnergyPbPC2,"cluster size 2","l")
leg3.AddEntry(EnergyPbPC3,"cluster size 3","l")
leg3.AddEntry(EnergyPbPC4,"cluster size 4","l")
leg3.SetFillColor(0)
leg3.SetFillStyle(0)
leg3.Draw("SAME")
EnergyPbPC1.SetTitle("EnergyPbPC spectrum")
can2.SaveAs("%s/Run%i/%s/EnergyPbPCnormalized.pdf"%(PlotPath,RunNumber,method_name))

can7 = TCanvas()
SquareCanvas(can7)
HitProb_1_cluster_binning1m.Draw("colz")
can7.SaveAs("%s/Run%i/%s/HitProb_1_cluster_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can8 = TCanvas()
SquareCanvas(can8)
HitProb_2_cluster_binning1m.Draw("colz")
can8.SaveAs("%s/Run%i/%s/HitProb_2_cluster_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can9 = TCanvas()
SquareCanvas(can9)
HitProb_3_cluster_binning1m.Draw("colz")
can9.SaveAs("%s/Run%i/%s/HitProb_3_cluster_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can10 = TCanvas()
SquareCanvas(can10)
HitProb_4_cluster_binning1m.Draw("colz")
can10.SaveAs("%s/Run%i/%s/HitProb_4_cluster_binning1m.pdf"%(PlotPath,RunNumber,method_name))


can7bis = TCanvas()
SquareCanvas(can7bis)
HitProb_1_cluster_binning2m.Draw("colz")
can7bis.SaveAs("%s/Run%i/%s/HitProb_1_cluster_binning2m.pdf"%(PlotPath,RunNumber,method_name))

can8bis = TCanvas()
SquareCanvas(can8bis)
HitProb_2_cluster_binning2m.Draw("colz")
can8bis.SaveAs("%s/Run%i/%s/HitProb_2_cluster_binning2m.pdf"%(PlotPath,RunNumber,method_name))

can9bis = TCanvas()
SquareCanvas(can9bis)
HitProb_3_cluster_binning2m.Draw("colz")
can9bis.SaveAs("%s/Run%i/%s/HitProb_3_cluster_binning2m.pdf"%(PlotPath,RunNumber,method_name))

can10bis = TCanvas()
SquareCanvas(can10bis)
HitProb_4_cluster_binning2m.Draw("colz")
can10bis.SaveAs("%s/Run%i/%s/HitProb_4_cluster_binning2m.pdf"%(PlotPath,RunNumber,method_name))


can11 = TCanvas()
SquareCanvas(can11)
relX_vs_relY.Draw("colz")
can11.SaveAs("%s/Run%i/%s/relX_vs_relY.pdf"%(PlotPath,RunNumber,method_name))


last_time = time.time()
HitProb_1_track_binning1m,HitProb_2_track_binning1m,HitProb_3_track_binning1m,HitProb_4_track_binning1m = TrackHitProb(aDataSet,55,dutID)
HitProb_1_track_binning2m,HitProb_2_track_binning2m,HitProb_3_track_binning2m,HitProb_4_track_binning2m = TrackHitProb(aDataSet,28,dutID)
print "Elapsed time for hitprob plots : %f s"%(time.time()-last_time)

h1_style(HitProb_1_track_binning1m)
h1_style(HitProb_2_track_binning1m)
h1_style(HitProb_3_track_binning1m)
h1_style(HitProb_4_track_binning1m)
h1_style(HitProb_1_track_binning2m)
h1_style(HitProb_2_track_binning2m)
h1_style(HitProb_3_track_binning2m)
h1_style(HitProb_4_track_binning2m)

can12 = TCanvas()
SquareCanvas(can12)
HitProb_1_track_binning1m.Draw("colz")
can12.SaveAs("%s/Run%i/%s/HitProb_1_track_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can13 = TCanvas()
SquareCanvas(can13)
HitProb_2_track_binning1m.Draw("colz")
can13.SaveAs("%s/Run%i/%s/HitProb_2_track_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can14 = TCanvas()
SquareCanvas(can14)
HitProb_3_track_binning1m.Draw("colz")
can14.SaveAs("%s/Run%i/%s/HitProb_3_track_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can15 = TCanvas()
SquareCanvas(can15)
HitProb_4_track_binning1m.Draw("colz")
can15.SaveAs("%s/Run%i/%s/HitProb_4_track_binning1m.pdf"%(PlotPath,RunNumber,method_name))

can12bis = TCanvas()
SquareCanvas(can12bis)
HitProb_1_track_binning2m.Draw("colz")
can12bis.SaveAs("%s/Run%i/%s/HitProb_1_track_binning2m.pdf"%(PlotPath,RunNumber,method_name))

can13bis = TCanvas()
SquareCanvas(can13bis)
HitProb_2_track_binning2m.Draw("colz")
can13bis.SaveAs("%s/Run%i/%s/HitProb_2_track_binning2m.pdf"%(PlotPath,RunNumber,method_name))

can14bis = TCanvas()
SquareCanvas(can14bis)
HitProb_3_track_binning2m.Draw("colz")
can14bis.SaveAs("%s/Run%i/%s/HitProb_3_track_binning2m.pdf"%(PlotPath,RunNumber,method_name))

can15bis = TCanvas()
SquareCanvas(can15bis)
HitProb_4_track_binning2m.Draw("colz")
can15bis.SaveAs("%s/Run%i/%s/HitProb_4_track_binning2m.pdf"%(PlotPath,RunNumber,method_name))

# Hit position vs track position
can22 = TCanvas()
SquareCanvas(can22)
HitProb_1_correlationX.Draw("colz")
can22.SaveAs("%s/Run%i/%s/HitProb_1_correlationX.pdf"%(PlotPath,RunNumber,method_name))

can23 = TCanvas()
SquareCanvas(can23)
HitProb_2_correlationX.Draw("colz")
can23.SaveAs("%s/Run%i/%s/HitProb_2_correlationX.pdf"%(PlotPath,RunNumber,method_name))

can24 = TCanvas()
SquareCanvas(can24)
HitProb_3_correlationX.Draw("colz")
can24.SaveAs("%s/Run%i/%s/HitProb_3_correlationX.pdf"%(PlotPath,RunNumber,method_name))

can25 = TCanvas()
SquareCanvas(can25)
HitProb_4_correlationX.Draw("colz")
can25.SaveAs("%s/Run%i/%s/HitProb_4_correlationX.pdf"%(PlotPath,RunNumber,method_name))

can26 = TCanvas()
SquareCanvas(can26)
HitProb_1_correlationY.Draw("colz")
can26.SaveAs("%s/Run%i/%s/HitProb_1_correlationY.pdf"%(PlotPath,RunNumber,method_name))

can27 = TCanvas()
SquareCanvas(can27)
HitProb_2_correlationY.Draw("colz")
can27.SaveAs("%s/Run%i/%s/HitProb_2_correlationY.pdf"%(PlotPath,RunNumber,method_name))

can28 = TCanvas()
SquareCanvas(can28)
HitProb_3_correlationY.Draw("colz")
can28.SaveAs("%s/Run%i/%s/HitProb_3_correlationY.pdf"%(PlotPath,RunNumber,method_name))

can29 = TCanvas()
SquareCanvas(can29)
HitProb_4_correlationY.Draw("colz")
can29.SaveAs("%s/Run%i/%s/HitProb_4_correlationY.pdf"%(PlotPath,RunNumber,method_name))

# TOT vs track position
can30 = TCanvas()
TOTProfileX_1_cluster_binning1m.Draw("colz")
can30.SaveAs("%s/Run%i/%s/TOTProfileX_1.pdf"%(PlotPath,RunNumber,method_name))

can31 = TCanvas()
TOTProfileX_2_cluster_binning1m.Draw("colz")
can31.SaveAs("%s/Run%i/%s/TOTProfileX_2.pdf"%(PlotPath,RunNumber,method_name))

can32 = TCanvas()
TOTProfileX_3_cluster_binning1m.Draw("colz")
can32.SaveAs("%s/Run%i/%s/TOTProfileX_3.pdf"%(PlotPath,RunNumber,method_name))

can33 = TCanvas()
TOTProfileX_4_cluster_binning1m.Draw("colz")
can33.SaveAs("%s/Run%i/%s/TOTProfileX_4.pdf"%(PlotPath,RunNumber,method_name))

can34 = TCanvas()
TOTProfileY_1_cluster_binning1m.Draw("colz")
can34.SaveAs("%s/Run%i/%s/TOTProfileY_1.pdf"%(PlotPath,RunNumber,method_name))

can35 = TCanvas()
TOTProfileY_2_cluster_binning1m.Draw("colz")
can35.SaveAs("%s/Run%i/%s/TOTProfileY_2.pdf"%(PlotPath,RunNumber,method_name))

can36 = TCanvas()
TOTProfileY_3_cluster_binning1m.Draw("colz")
can36.SaveAs("%s/Run%i/%s/TOTProfileY_3.pdf"%(PlotPath,RunNumber,method_name))

can37 = TCanvas()
TOTProfileY_4_cluster_binning1m.Draw("colz")
can37.SaveAs("%s/Run%i/%s/TOTProfileY_4.pdf"%(PlotPath,RunNumber,method_name))

can38 = TCanvas()
TOTProfileX.Draw("colz")
can38.SaveAs("%s/Run%i/%s/TOTProfileX.pdf"%(PlotPath,RunNumber,method_name))

can39 = TCanvas()
TOTProfileY.Draw("colz")
can39.SaveAs("%s/Run%i/%s/TOTProfileY.pdf"%(PlotPath,RunNumber,method_name))

can40 = TCanvas()
TOTProfile.Draw("colz")
SquareCanvas(can40)
can40.SaveAs("%s/Run%i/%s/TOTProfile.pdf"%(PlotPath,RunNumber,method_name))

# Write all histograms to output root file
out = TFile("%s/Run%i/%s/output_rootfile.root"%(PlotPath,RunNumber,method_name), "recreate")
out.cd()

h_chi2.Write()
h_chi2ndof.Write()
for i in range(4) :
    edge_efficiencies[i].Write()
    edge_matched[i].Write()
    edge_tracks[i].Write()
    edge_tots[i].Write()
hClusterSize.Write()
hClusterSizeX.Write()
hClusterSizeY.Write()
hClusterSizeXvsSizeY.Write()
hClusterSizeCounter.Write()
hClusterSizeCounter_percent.Write()
hx.Write()
hy.Write()
QrelWrtMindistance.Write()
resX_s1x1y1.Write()
resY_s1x1y1.Write()
resX_s2x2y2.Write()
resY_s2x2y2.Write()
resX_s2x1y2.Write()
resY_s2x1y2.Write()
resX_s2x2y1.Write()
resY_s2x2y1.Write()
resX_s3x2y2.Write()
resY_s3x2y2.Write()
resX_s4x2y2.Write()
resY_s4x2y2.Write()
resXGC_s2x2y1.Write()
resXPbPC_s2x2y1.Write()
resYGC_s2x1y2.Write()
resYPbPC_s2x1y2.Write()
resX_s2x2y1_relX.Write()
resX_s2x2y1_relX_1.Write()
resX_s2x2y1_relX_2.Write()
resXGC_s2x2y1_relX.Write()
resXGC_s2x2y1_relX_1.Write()
resXGC_s2x2y1_relX_2.Write()
resXPbPC_s2x2y1_relX.Write()
resXPbPC_s2x2y1_relX_1.Write()
resXPbPC_s2x2y1_relX_2.Write()
resY_s2x1y2_relY.Write()
resY_s2x1y2_relY_1.Write()
resY_s2x1y2_relY_2.Write()
resYGC_s2x1y2_relY.Write()
resYGC_s2x1y2_relY_1.Write()
resYGC_s2x1y2_relY_2.Write()
resYPbPC_s2x1y2_relY.Write()
resYPbPC_s2x1y2_relY_1.Write()
resYPbPC_s2x1y2_relY_2.Write()
Qrel_s2x2y1.Write()
QrelGC_s2x2y1.Write()
QrelPbPC_s2x2y1.Write()
Qrel_s2x1y2.Write()
QrelGC_s2x1y2.Write()
QrelPbPC_s2x1y2.Write()
Qrel_s2x2y1_relX.Write()
Qrel_s2x1y2_relY.Write()
QrelGC_s2x2y1_relX.Write()
QrelGC_s2x1y2_relY.Write()
QrelPbPC_s2x2y1_relX.Write()
QrelPbPC_s2x1y2_relY.Write()
allTOT.Write()
TOT1.Write()
TOT2.Write()
TOT3.Write()
TOT4.Write()
allEnergyGC.Write()
EnergyGC1.Write()
EnergyGC2.Write()
EnergyGC3.Write()
EnergyGC4.Write()
allEnergyPbPC.Write()
EnergyPbPC1.Write()
EnergyPbPC2.Write()
EnergyPbPC3.Write()
EnergyPbPC4.Write()
resX.Write()
resY.Write()
HitProb_1_cluster_binning1m.Write()
HitProb_2_cluster_binning1m.Write()
HitProb_3_cluster_binning1m.Write()
HitProb_4_cluster_binning1m.Write()
HitProb_1_cluster_binning2m.Write()
HitProb_2_cluster_binning2m.Write()
HitProb_3_cluster_binning2m.Write()
HitProb_4_cluster_binning2m.Write()
relX_vs_relY.Write()
HitProb_1_track_binning1m.Write()
HitProb_2_track_binning1m.Write()
HitProb_3_track_binning1m.Write()
HitProb_4_track_binning1m.Write()
HitProb_1_track_binning2m.Write()
HitProb_2_track_binning2m.Write()
HitProb_3_track_binning2m.Write()
HitProb_4_track_binning2m.Write()
HitProb_1_correlationX.Write()
HitProb_2_correlationX.Write()
HitProb_3_correlationX.Write()
HitProb_4_correlationX.Write()
HitProb_1_correlationY.Write()
HitProb_2_correlationY.Write()
HitProb_3_correlationY.Write()
HitProb_4_correlationY.Write()
TOTProfileX_1_cluster_binning1m.Write()
TOTProfileX_2_cluster_binning1m.Write()
TOTProfileX_3_cluster_binning1m.Write()
TOTProfileX_4_cluster_binning1m.Write()
TOTProfileY_1_cluster_binning1m.Write()
TOTProfileY_2_cluster_binning1m.Write()
TOTProfileY_3_cluster_binning1m.Write()
TOTProfileY_4_cluster_binning1m.Write()
TOTProfileX.Write()
TOTProfileY.Write()
TOTProfile.Write()
