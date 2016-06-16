from datetime import datetime
startTime = datetime.now()

from ROOT import *
import os
import optparse
from array import array

#debug
#from sys import stdin


parser = optparse.OptionParser()

parser.add_option('-i', '--input', default=".", help="Input directory.")
parser.add_option('-o', '--output', default=".", help="Output directory.")
parser.add_option('-f', '--infile', help="Input file name.")

(options, args) = parser.parse_args()

print (options, args)

print "Converts (Judith reconstructed) cosmic files to tbtrack."

if options.infile is None:
	print "I have nothing to convert."
	parser.print_help()
	exit()
else:

	if not options.input.endswith('/'):
		options.input = options.input+'/'
		
	if not options.output.endswith('/'):
		options.output = options.output+'/'
		
	infilename = options.input+options.infile
	
	if not infilename.endswith(".root"):
		infilename = infilename + ".root"

if os.path.isfile(infilename):
	#print infilename
	
	runnumber = infilename.split(".root")[0][-6:]
	#print runnumber
	
	outfilename = options.output+"tbtrackrun"+runnumber+".root"
	infile = TFile(infilename,'r')
	outfile = TFile(outfilename,"recreate")
	
	pixelTree = TTree("zspix", "zspix")
	trackTree = TTree("eutracks", "eutracks")
	
	nmaxhits = 1000 ##limit for max number of hits per event
	p_nEntries = infile.Get("Plane0").Get("Hits").GetEntriesFast()
	t_nEntries = infile.Get("Tracks").GetEntriesFast()
	
	#print p_nEntries, t_nEntries

	###create arrays for pixel branch
	p_NHits = array('i',[0])
	p_euEvt = array('i',[0])
	p_PixX = array('i',[0]*nmaxhits)
	p_PixY = array('i',[0]*nmaxhits)
	p_Value = array('i',[0]*nmaxhits)
	p_Timing = array('i',[0]*nmaxhits)
	p_Planes = array('i',[0]*nmaxhits)

	##create arrays for track branch
	t_NTracks = array('i',[0])
	t_nTrackParams = array('i',[0])
	t_euEvt = array('i',[0])
	t_SlopeX = array('d',[0]*nmaxhits)
	t_SlopeY = array('d',[0]*nmaxhits)
	t_PosX = array('d',[0]*nmaxhits)
	t_PosY = array('d',[0]*nmaxhits)
	t_trackNum = array('i',[0]*nmaxhits)
	t_Planes = array('i',[0]*nmaxhits)
	t_Chi2 = array('d',[1]*nmaxhits)
	t_ndof = array('i',[1]*nmaxhits)

	##pixel tree
	nPixHits = pixelTree.Branch("nPixHits", p_NHits, "nPixHits/I")
	euEvt = pixelTree.Branch("euEvt", p_euEvt, "euEvt/I")
	col = pixelTree.Branch("col", p_PixX, "col[nPixHits]/I")
	row = pixelTree.Branch("row", p_PixY, "row[nPixHits]/I")
	tot = pixelTree.Branch("tot", p_Value, "tot[nPixHits]/I")
	lv1 = pixelTree.Branch("lv1", p_Timing, "lv1[nPixHits]/I")
	iden = pixelTree.Branch("iden", p_Planes, "iden[nPixHits]/I")

	##track tree, need an integer NTracks to define the size of arrays
	NTracks = trackTree.Branch("NTracks", t_NTracks, "NTracks/I")
	nTrackParams = trackTree.Branch("nTrackParams", t_nTrackParams, "nTrackParams/I")
	euEvt = trackTree.Branch("euEvt", t_euEvt, "euEvt/I")
	xPos = trackTree.Branch("xPos", t_PosX, "xPos[nTrackParams]/D")
	yPos = trackTree.Branch("yPos", t_PosY, "yPos[nTrackParams]/D")
	dxdz = trackTree.Branch("dxdz", t_SlopeX, "dxdz[nTrackParams]/D")
	dydz = trackTree.Branch("dydz", t_SlopeY, "dydz[nTrackParams]/D")
	trackNum = trackTree.Branch("trackNum", t_trackNum, "trackNum[nTrackParams]/I")
	t_iden = trackTree.Branch("iden", t_Planes, "iden[nTrackParams]/I")
	chi2 = trackTree.Branch("chi2", t_Chi2, "chi2[nTrackParams]/D")
	ndof = trackTree.Branch("ndof", t_ndof, "ndof[nTrackParams]/I")

	tmpPixelTrees={}
	tmpTrackTrees={}
	
	for key in infile.GetListOfKeys():
		if "Plane" in key.GetName():
			tmpPixelTrees[key.GetName()]=infile.Get(key.GetName()).Get("Hits")
		else:
			continue
			
	for key in infile.GetListOfKeys():
		if "Plane" in key.GetName():
			tmpTrackTrees[key.GetName()]=infile.Get(key.GetName()).Get("Intercepts")
		elif "Track" in key.GetName():
			tmpTrackTrees[key.GetName()]=infile.Get("Tracks")
		else:
			continue

	#print "=== tmpPixelTrees:", tmpPixelTrees
	#print "=== tmpTrackTrees:", tmpTrackTrees

	##### PIXEL TREE LOOP
	for i in range(p_nEntries): ##loop over events
		if (i%10000 == 0):
			print("Reading pixel event "+str(i))
		if i > 20000:
			break
		p_NHits[0] = 0

		for key, tmpTree in tmpPixelTrees.iteritems():
			#print p_nEntries, key
			#tmpTree.Print()
			tmpTree.GetEntry(i)
			for j in range(p_NHits[0],p_NHits[0]+tmpTree.NHits): ##loop over hits
				#if j > 100:
					#print "event ", i, " hit ", j, " plane ", int(key[5:]), tmpTree.NHits
				#p_NHits[0] is total hits per event for all planes, each hit has an iden
				#p_NHits[0] is therefore cumulativ, len(tmpTree.PixX) >= NHits[0]
				p_PixX[j] = tmpTree.PixX[j-p_NHits[0]]
				p_PixY[j] = tmpTree.PixY[j-p_NHits[0]]
				p_Value[j] = tmpTree.Value[j-p_NHits[0]]
				p_Timing[j] = tmpTree.Timing[j-p_NHits[0]]
				p_Planes[j] = int(key[5:]) ##iden

			##number of hits per event, sum over all planes
			p_NHits[0] = p_NHits[0] + tmpTree.NHits
	
		pixelTree.Fill()
	
	##### TRACK TREE LOOP
	for i in range(t_nEntries): ##loop over tracks
		if (i%10000 == 0):
			print("Reading track event "+str(i))
		if i > 20000:
			break

		tmpTrackTrees["Tracks"].GetEntry(i)
		
		t_NTracks[0]=tmpTrackTrees["Tracks"].NTracks
		t_euEvt[0]=i

	
		iEventEl=0
		for key, interceptTree in tmpTrackTrees.iteritems():
			if "Tracks" in key:  # only intercept trees
				continue
			
			iden=int(key[5:])
			
			interceptTree.GetEntry(i)
			if interceptTree.NIntercepts != t_NTracks[0]:
				raise ValueError("mismatch between tracks and intercepts for event "+str(i))
			
			for iTrack in range (t_NTracks[0]):
				t_trackNum[iEventEl] = iTrack
				t_Planes[iEventEl] = iden

				t_SlopeX[iEventEl] = tmpTrackTrees["Tracks"].SlopeX[iTrack]
				t_SlopeY[iEventEl] = tmpTrackTrees["Tracks"].SlopeY[iTrack]
				t_Chi2[iEventEl] = tmpTrackTrees["Tracks"].Chi2[iTrack]
				t_ndof[iEventEl] = 1
				
				sensorHalfX = 80 * 250 / 2
				sensorHalfY = 336 * 50 / 2
				t_PosX[iEventEl] = (interceptTree.interceptX[iTrack] - sensorHalfX) / 1e3
				t_PosY[iEventEl] = (interceptTree.interceptY[iTrack] - sensorHalfY) / 1e3
				
				iEventEl=iEventEl+1
				
		t_nTrackParams[0]=iEventEl
		
		#if iEventEl > 42:
			#print t_euEvt, iEventEl
		
		#if iEventEl%6:
			#print t_euEvt, t_Planes
			
		trackTree.Fill()


		#for key, tmpTree in tmpTrackTrees.iteritems():
			#tmpTree.GetEntry(i)
			#if "Tracks" in key: ##track tree
				#if tmpTree.NTracks != 1:
					#print tmpTree.NTracks
				#for j in range(tmpTree.NTracks):
					#t_NTracks[0] = tmpTree.NTracks
					#t_SlopeX[j] = tmpTree.SlopeX[j]
					#t_SlopeY[j] = tmpTree.SlopeY[j]
					#t_Chi2[j] = tmpTree.Chi2[j]
			#elif "Plane" in key: ## planes
				#if tmpTree.NIntercepts != 1:
					#print key, tmpTree.NIntercepts
				#for j in range(tmpTree.NIntercepts): ##loop over intercepts
					
					#t_OriginX[j] = tmpTree.interceptX[j]
					#t_OriginY[j] = tmpTree.interceptY[j]
					#t_trackNum[j] = tmpTree.NIntercepts ##???
					#t_Planes[j] = int(key[5:]) ##iden
					
		#trackTree.Fill()
	
	outfile.cd()
	trackTree.Write()
	pixelTree.Write()
	outfile.Close()
	
	infile.Close()
	infile=0

	
else:
	print "Your argument is invalid."
	exit()


print "Wall time: ", datetime.now() - startTime
