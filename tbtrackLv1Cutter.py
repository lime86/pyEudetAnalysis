## lmeng@cern.ch

from datetime import datetime
startTime = datetime.now()

from ROOT import *
import os
import optparse
from array import array

filename = ""

parser = optparse.OptionParser()

parser.add_option('-i', '--indir', default=".", help="indir directory.")
parser.add_option('-o', '--outdir', default=".", help="outdir directory.")
parser.add_option('-r', '--run', help="Run number")

(options, args) = parser.parse_args()

print (options, args)

print "Cuts on lv1 MaximumBin"

if options.run is None:
	print "I have nothing to convert."
	parser.print_help()
	exit()
else:
	if options.indir == options.outdir:
		print "Cannot use the same in- and output directory, exiting."
		exit()
	else:

		if not options.indir.endswith('/'):
			options.indir = options.indir+'/'
			
		if not options.outdir.endswith('/'):
			options.outdir = options.outdir+'/'
		
		runnumber = int(options.run)
		
		diff = 6-len(str(runnumber))
		
		if diff > 0:
			runnumber = diff*'0'+str(runnumber)
			print runnumber
		
		filename = "tbtrackrun"+runnumber+".root"

infilename = options.indir+filename
outfilename = options.outdir+filename

if os.path.isfile(infilename):
	print filename
	
	infile = TFile(infilename,'r')
	outfile = TFile(outfilename,"recreate")
	
	treelist = []
	
	
	
	for key in infile.GetListOfKeys():
		if not key.GetName() == "rawdata":
			treelist.append(infile.Get(key.GetName()).CloneTree())
		else:
			nmaxhits = 1000
			
			p_nPixHits = array('i',[0])
			p_euEvt = array('i',[0])
			p_col = array('i',[0]*nmaxhits)
			p_row = array('i',[0]*nmaxhits)
			p_tot = array('i',[0]*nmaxhits)
			p_lv1 = array('i',[0]*nmaxhits)
			p_iden = array('i',[0]*nmaxhits)

			pixelTree = TTree(key.GetName(), key.GetName())
			nPixHits = pixelTree.Branch("nPixHits", p_nPixHits, "nPixHits/I")
			euEvt = pixelTree.Branch("euEvt", p_euEvt, "euEvt/I")
			col = pixelTree.Branch("col", p_col, "col[nPixHits]/I")
			row = pixelTree.Branch("row", p_row, "row[nPixHits]/I")
			tot = pixelTree.Branch("tot", p_tot, "tot[nPixHits]/I")
			lv1 = pixelTree.Branch("lv1", p_lv1, "lv1[nPixHits]/I")
			iden = pixelTree.Branch("iden", p_iden, "iden[nPixHits]/I")
			#hitTime = pixelTree.Branch("hitTime", p_hitTime, "hitTime[nPixHits]/I")
			#frameTime = pixelTree.Branch("frameTime", p_frameTime, "frameTime[nPixHits]/I")
			
			tmpPixelTree=infile.Get(key.GetName())
				
			p_nentries = tmpPixelTree.GetEntriesFast()

			for i in range(p_nentries):
				tmpPixelTree.GetEntry(i)
				
				lv1hist = TH1I("","",50,0,50)
				for j in range(tmpPixelTree.nPixHits):
					lv1hist.Fill(tmpPixelTree.lv1[j])
				#lv1hist.Draw()
				maxlv1 = lv1hist.GetMaximumBin()-1
				p_nPixHits[0] = int(lv1hist.GetMaximum())
				p_euEvt[0] = tmpPixelTree.euEvt
				k = 0
				
				for j in range(tmpPixelTree.nPixHits):
					if tmpPixelTree.lv1[j] == maxlv1:
						##fill all branches
						p_col[k] = tmpPixelTree.col[j]
						p_row[k] = tmpPixelTree.row[j]
						p_tot[k] = tmpPixelTree.tot[j]
						p_lv1[k] = tmpPixelTree.lv1[j]
						p_iden[k] = tmpPixelTree.iden[j]
						k += 1
						
				pixelTree.Fill()
	
	
	outfile.cd()
	for i in range(len(treelist)):
		treelist[i].Write()
	pixelTree.Write()
	outfile.Close()
	
	infile.Close()

else:
	print "Your argument is invalid."
	exit()


print "Wall time: ", datetime.now() - startTime


#raw_input()
