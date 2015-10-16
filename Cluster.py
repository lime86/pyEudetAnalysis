'''
author: Anne-Laure pequegnot
'''

from math import fsum
from Constant import *
from ROOT import TMath
from ToolBox import *



#
# Compute the shift in the hit position due to the charge sharing (eta correction) when neighbour pixels are on the same row or the same column
# first parameter: sigma of the eta correction (charge sharing)
# second parameter: relative charge Qrel = (charge of the pixel with the highest energy)/(total charge of the cluster)
#
def shiftLat(sigma_tmp,Qrel_tmp):
    return sigma_tmp*TMath.ErfInverse(2.*Qrel_tmp-1.)

#
# Compute the shift in the hit position due to the charge sharing (eta correction) when neighbour pixels are on a diadonal
# first parameter: sigma of the eta correction (charge sharing)
# second parameter: relative charge Qrel = (charge of the pixel with the highest energy)/(total charge of the cluster)
#
def shiftDiag(sigma_tmp,Qrel_tmp):
    return sigma_tmp*TMath.ErfInverse(2.*Qrel_tmp-1.)*1./sqrt(2.),sigma_tmp*TMath.ErfInverse(2.*Qrel_tmp-1.)*1./sqrt(2.)



###############################################################################################################################
#
#        Class for the clusters and their properties
#
###############################################################################################################################

class Cluster:

    col = []
    row = []
    tot = []
    energyGC = []
    energyPbPC = []
    sizeX = 0
    sizeY = 0
    size  = 0
    totalTOT =0
    aspectRatio = 0

    # local coordinates
    relX = 0.
    relY = 0.
    relZ = 0.
    relX_energyGC = 0.
    relY_energyGC = 0.
    relZ_energyGC = 0.
    relX_energyPbPC = 0.
    relY_energyPbPC = 0.
    relZ_energyPbPC = 0.

    # telescope coordinates
    absX =-10000.
    absY =-10000.
    absZ =-10000.
    absX_energyGC =-10000.
    absY_energyGC =-10000.
    absZ_energyGC =-10000.
    absX_energyPbPC =-10000.
    absY_energyPbPC =-10000.
    absZ_energyPbPC =-10000.

    resX = -10000.
    resY = -10000.
    resX_energyGC = -10000.
    resY_energyGC = -10000.
    resX_energyPbPC = -10000.
    resY_energyPbPC = -10000.

    id = 0

    # track number
    tracknum = -1

    def __init__(self):
        self.sizeX = 0
        self.sizeY = 0
        self.size  = 0
        self.col = []
        self.row = []
        self.tot = []
        self.energyGC = []
        self.energyPbPC = []

    def addPixel(self,col,row,tot,energyGC,energyPbPC):
        self.col.append(col)
        self.row.append(row)
        self.tot.append(tot)
        self.energyGC.append(energyGC)
        self.energyPbPC.append(energyPbPC)

    def Print(self):
        for i in range(len(self.col)):
            print "x:%d y%d tot:%.3f"%(self.col[i],self.row[i],self.tot[i])
        print "Cluster Total size = %d , in X = %d Y = %d , Aspect Ratio = %.3f , Total Energy (keV) = %.1f ID = %i"%(self.size,self.sizeX,self.sizeY,self.aspectRatio,self.totalTOT,self.id)
        print "Position in sensor X = %.3f Y = %.3f"%(self.absX,self.absY)

    def Statistics(self) :
        self.totalTOT=fsum(self.tot)
        self.size=len(self.col)
        self.sizeX=max(self.col)-min(self.col)+1
        self.sizeY=max(self.row)-min(self.row)+1
        self.aspectRatio=float(self.sizeY)/self.sizeX
        self.totalEnergyGC = fsum(self.energyGC)
        self.totalEnergyPbPC = fsum(self.energyPbPC)

#
#compute the hit position as the mean of the fired pixels positions weighted by their deposited energy
#
    def GetQWeightedCentroid(self) :
        self.relX=0.
        self.relY=0.
        self.relX_energyGC=0.
        self.relY_energyGC=0.
        self.relX_energyPbPC=0.
        self.relY_energyPbPC=0.

        if(self.totalTOT==0):
            self.GetDigitalCentroid()
        else :
            for index,tot_tmp in enumerate(self.tot) :
                self.relX+=(self.col[index]*pitchX)*tot_tmp
                self.relY+=(self.row[index]*pitchY)*tot_tmp

            self.relX = self.relX/self.totalTOT + pitchX/2.
            self.relY = self.relY/self.totalTOT + pitchY/2.

            self.absX=self.relX - halfChip_X
            self.absY=self.relY - halfChip_Y
            self.absZ=0

        if ((self.totalEnergyGC > 0) and (0 not in self.energyGC)):
            for index,energyGC_tmp in enumerate(self.energyGC) :
                self.relX_energyGC+=(self.col[index]*pitchX)*energyGC_tmp
                self.relY_energyGC+=(self.row[index]*pitchY)*energyGC_tmp

            self.relX_energyGC = self.relX_energyGC/self.totalEnergyGC + pitchX/2.
            self.relY_energyGC = self.relY_energyGC/self.totalEnergyGC + pitchY/2.

            self.absX_energyGC=self.relX_energyGC - halfChip_X
            self.absY_energyGC=self.relY_energyGC - halfChip_Y
            self.absZ_energyGC=0

        if ((self.totalEnergyPbPC > 0) and (0 not in self.energyPbPC)):
            for index,energyPbPC_tmp in enumerate(self.energyPbPC) :
                self.relX_energyPbPC+=(self.col[index]*pitchX)*energyPbPC_tmp
                self.relY_energyPbPC+=(self.row[index]*pitchY)*energyPbPC_tmp

            self.relX_energyPbPC = self.relX_energyPbPC/self.totalEnergyPbPC + pitchX/2.
            self.relY_energyPbPC = self.relY_energyPbPC/self.totalEnergyPbPC + pitchY/2.

            self.absX_energyPbPC=self.relX_energyPbPC - halfChip_X
            self.absY_energyPbPC=self.relY_energyPbPC - halfChip_Y
            self.absZ_energyPbPC=0

#
#compute the hit position as the mean of the fired pixels positions (digital method)
#
    def GetDigitalCentroid(self) :
        self.relX=0.
        self.relY=0.
        for index,col_tmp in enumerate(self.col) :
            self.relX+=(self.col[index]*pitchX)
            self.relY+=(self.row[index]*pitchY)

        self.relX = self.relX/len(self.col) + pitchX/2.
        self.relY = self.relY/len(self.row) + pitchY/2.

        self.absX=self.relX - halfChip_X
        self.absY=self.relY - halfChip_Y
        self.absZ=0

#
#compute the hit position as the center of the fired pixel with the highest energy
#
    def GetMaxTOTCentroid(self) :
        maxTOTindex_tmp=0
        maxTOT_tmp=self.tot[0]
        for index,tot_tmp in enumerate(self.tot) :
            if self.tot[index]>maxTOT_tmp:
                maxTOT_tmp=self.tot[index]
                maxTOTindex_tmp=index

        self.relX=self.col[maxTOTindex_tmp]*pitchX + pitchX/2.
        self.relY=self.row[maxTOTindex_tmp]*pitchY + pitchY/2.

        self.absX=self.relX - halfChip_X
        self.absY=self.relY - halfChip_Y
        self.absZ=0

#
#compute the hit position as the Qweighted method but adding an eta correction du to the charge sharing between the fired pixels
#
    def GetEtaCorrectedQWeightedCentroid(self,sigma=0.003,sigmaGC=0.003,sigmaPbPC=0.003) :

        self.relX = -1000
        self.relY = -1000
        self.absX = -1000
        self.absY = -1000
        self.relX_energyGC = -1000
        self.relY_energyGC = -1000
        self.absX_energyGC = -1000
        self.absY_energyGC = -1000
        self.relX_energyPbPC = -1000
        self.relY_energyPbPC = -1000
        self.absX_energyPbPC = -1000
        self.absY_energyPbPC = -1000


        if(self.size==2) :
            if(self.sizeX==2 and self.sizeY==1) :
                # cluster size 2x1
                Qrel = self.tot[self.col.index(min(self.col))] / self.totalTOT
                self.relX = max(self.col)*pitchX - shiftLat(sigma,Qrel)
                self.relY = self.row[0]*pitchY + pitchY/2.

                if ((self.totalEnergyGC > 0) and (0 not in self.energyGC)):
                    Qrel_energyGC = self.energyGC[self.col.index(min(self.col))] / self.totalEnergyGC
                    self.relX_energyGC = max(self.col)*pitchX - shiftLat(sigmaGC,Qrel_energyGC)
                    self.relY_energyGC = self.row[0]*pitchY + pitchY/2.

                if ((self.totalEnergyPbPC > 0) and (0 not in self.energyPbPC)):
                    Qrel_energyPbPC = self.energyPbPC[self.col.index(min(self.col))] / self.totalEnergyPbPC
                    self.relX_energyPbPC = max(self.col)*pitchX - shiftLat(sigmaPbPC,Qrel_energyPbPC)
                    self.relY_energyPbPC = self.row[0]*pitchY + pitchY/2.

            elif(self.sizeX==1 and self.sizeY==2) :
                # cluster size 1x2
                Qrel = self.tot[self.row.index(min(self.row))] / self.totalTOT
                self.relX = self.col[0]*pitchX + pitchX/2.
                self.relY = max(self.row)*pitchY - shiftLat(sigma,Qrel)
                
                if ((self.totalEnergyGC > 0) and (0 not in self.energyGC)):
                    Qrel_energyGC = self.energyGC[self.row.index(min(self.row))] / self.totalEnergyGC
                    self.relX_energyGC = self.col[0]*pitchX + pitchX/2.
                    self.relY_energyGC = max(self.row)*pitchY - shiftLat(sigmaGC,Qrel_energyGC)

                if ((self.totalEnergyPbPC > 0) and (0 not in self.energyPbPC)):
                    Qrel_energyPbPC = self.energyPbPC[self.row.index(min(self.row))] / self.totalEnergyPbPC
                    self.relX_energyPbPC = self.col[0]*pitchX + pitchX/2.
                    self.relY_energyPbPC = max(self.row)*pitchY - shiftLat(sigmaPbPC,Qrel_energyPbPC)

            elif(self.sizeX==2 and self.sizeY==2) :
                # cluster size 2 with sizeX = 2 and sizeY = 2 i.e. 2 pixels on a diagonal
                self.GetMaxTOTCentroid()


        elif(self.size==4) :
            if(self.sizeX==2 and self.sizeY==2) :
                for i in xrange(len(self.row)):
                    if self.row[i] == min(self.row) and self.col[i] == min(self.col):
                        bottomlefti = i
                    if self.row[i] == max(self.row) and self.col[i] == max(self.col):
                        toprighti = i
                    if self.row[i] == min(self.row) and self.col[i] == max(self.col):
                        toplefti = i
                    if self.row[i] == max(self.row) and self.col[i] == min(self.col):
                        bottomrighti = i
                Qrel1 = self.tot[bottomlefti] / (self.tot[bottomlefti] + self.tot[toprighti])
                Qrel2 = self.tot[bottomrighti] / (self.tot[bottomrighti] + self.tot[toplefti])

                shift1X,shift1Y = shiftDiag(sigma,Qrel1)
                shift2X,shift2Y = shiftDiag(sigma,Qrel2)

                self.relX = max(self.col)*pitchX - shift1X - shift2X
                self.relY = max(self.row)*pitchY - shift1Y + shift2Y

                if ((self.totalEnergyGC > 0) and (0 not in self.energyGC)):
                    Qrel1_energyGC = self.energyGC[bottomlefti] / (self.energyGC[bottomlefti] + self.energyGC[toprighti])
                    Qrel2_energyGC = self.energyGC[bottomrighti] / (self.energyGC[bottomrighti] + self.energyGC[toplefti])

                    shift1X_GC,shift1Y_GC = shiftDiag(sigmaGC,Qrel1_energyGC)
                    shift2X_GC,shift2Y_GC = shiftDiag(sigmaGC,Qrel2_energyGC)

                    self.relX_energyGC = max(self.col)*pitchX - shift1X_GC - shift2X_GC
                    self.relY_energyGC = max(self.row)*pitchY - shift1Y_GC + shift2Y_GC

                if ((self.totalEnergyPbPC > 0) and (0 not in self.energyPbPC)):
                    Qrel1_energyPbPC = self.energyPbPC[bottomlefti] / (self.energyPbPC[bottomlefti] + self.energyPbPC[toprighti])
                    Qrel2_energyPbPC = self.energyPbPC[bottomrighti] / (self.energyPbPC[bottomrighti] + self.energyPbPC[toplefti])

                    shift1X_PbPC,shift1Y_PbPC = shiftDiag(sigmaPbPC,Qrel1_energyPbPC)
                    shift2X_PbPC,shift2Y_PbPC = shiftDiag(sigmaPbPC,Qrel2_energyPbPC)

                    self.relX_energyPbPC = max(self.col)*pitchX - shift1X_PbPC - shift2X_PbPC
                    self.relY_energyPbPC = max(self.row)*pitchY - shift1Y_PbPC + shift2Y_PbPC

            else : # not 2x2 -> using the simple Qweighted centroid
                self.GetQWeightedCentroid()


        elif(self.size==3) :
            if(self.sizeX==2 and self.sizeY==2) :
                # copy original row, col, tot to keep safe
                orig_row = list(self.row)
                orig_col = list(self.col)
                orig_tot = list(self.tot)
                orig_energyGC = list(self.energyGC)
                orig_energyPbPC = list(self.energyPbPC)

                # calculate and add missing pixel
                for i in xrange(len(self.row)):
                    if self.row.count(self.row[i]) == 1:
                        self.row.append(self.row[i])
                    if self.col.count(self.col[i]) == 1:
                        self.col.append(self.col[i])
                        self.tot.append(1.0)
                        self.energyGC.append(1.0)
                        self.energyPbPC.append(1.0)

                # proceed as 4 cluster case
                for i in xrange(len(self.row)):
                    if self.row[i] == min(self.row) and self.col[i] == min(self.col):
                        bottomlefti = i
                    if self.row[i] == max(self.row) and self.col[i] == max(self.col):
                        toprighti = i
                    if self.row[i] == min(self.row) and self.col[i] == max(self.col):
                        toplefti = i
                    if self.row[i] == max(self.row) and self.col[i] == min(self.col):
                        bottomrighti = i
                Qrel1 = self.tot[bottomlefti] / (self.tot[bottomlefti] + self.tot[toprighti])
                Qrel2 = self.tot[bottomrighti] / (self.tot[bottomrighti] + self.tot[toplefti])

                shift1X,shift1Y = shiftDiag(sigma,Qrel1)
                shift2X,shift2Y = shiftDiag(sigma,Qrel2)

                self.relX = max(self.col)*pitchX - shift1X - shift2X
                self.relY = max(self.row)*pitchY - shift1Y + shift2Y

                if ((self.totalEnergyGC > 0) and (0 not in self.energyGC)):
                    Qrel1_energyGC = self.energyGC[bottomlefti] / (self.energyGC[bottomlefti] + self.energyGC[toprighti])
                    Qrel2_energyGC = self.energyGC[bottomrighti] / (self.energyGC[bottomrighti] + self.energyGC[toplefti])

                    shift1X_GC,shift1Y_GC = shiftDiag(sigmaGC,Qrel1_energyGC)
                    shift2X_GC,shift2Y_GC = shiftDiag(sigmaGC,Qrel2_energyGC)

                    self.relX_energyGC = max(self.col)*pitchX - shift1X_GC - shift2X_GC
                    self.relY_energyGC = max(self.row)*pitchY - shift1Y_GC + shift2Y_GC

                if ((self.totalEnergyPbPC > 0) and (0 not in self.energyPbPC)):
                    Qrel1_energyPbPC = self.energyPbPC[bottomlefti] / (self.energyPbPC[bottomlefti] + self.energyPbPC[toprighti])
                    Qrel2_energyPbPC = self.energyPbPC[bottomrighti] / (self.energyPbPC[bottomrighti] + self.energyPbPC[toplefti])

                    shift1X_PbPC,shift1Y_PbPC = shiftDiag(sigmaPbPC,Qrel1_energyPbPC)
                    shift2X_PbPC,shift2Y_PbPC = shiftDiag(sigmaPbPC,Qrel2_energyPbPC)

                    self.relX_energyPbPC = max(self.col)*pitchX - shift1X_PbPC - shift2X_PbPC
                    self.relY_energyPbPC = max(self.row)*pitchY - shift1Y_PbPC + shift2Y_PbPC

                # put back original row, col, tot
                self.row = orig_row
                self.col = orig_col
                self.tot = orig_tot
                self.energyGC = orig_energyGC
                self.energyPbPC = orig_energyPbPC

            else : # not 2x2 -> using the simple Qweighted centroid
                self.GetQWeightedCentroid()


        else : # other cluster sizes -> using the simple Qweighted centroid
            self.GetQWeightedCentroid()


        self.absX = self.relX - halfChip_X
        self.absY = self.relY - halfChip_Y
        self.absZ = 0
        self.absX_energyGC = self.relX_energyGC - halfChip_X
        self.absY_energyGC = self.relY_energyGC - halfChip_Y
        self.absZ_energyGC = 0
        self.absX_energyPbPC = self.relX_energyPbPC - halfChip_X
        self.absY_energyPbPC = self.relY_energyPbPC - halfChip_Y
        self.absZ_energyPbPC = 0


        if (self.relX == -1000 or self.relY == -1000 or self.absX == -1000 or self.absY == -1000):
            print "WARNING GetEtaCorrectedQWeightedCentroid didn't calculate centroid for some cluster"
            print "WARNING This should never happen - review code"



    def GetResiduals(self,x,y) :
        self.resX = self.absX-(x)
        self.resY = self.absY-(y)
        self.resX_energyGC = self.absX_energyGC-(x)
        self.resY_energyGC = self.absY_energyGC-(y)
        self.resX_energyPbPC = self.absX_energyPbPC-(x)
        self.resY_energyPbPC = self.absY_energyPbPC-(y)


    def GetPixelResiduals(self,trackx,tracky) :
        # compute the x, y distances between a track 
        # and the centre of each pixel in the cluster
        # return the smallest combined

        dr = []
        dx = []
        dy = []
        for i in xrange(self.size):
            resX = self.col[i]*pitchX + pitchX/2. - halfChip_X - trackx
            resY = self.row[i]*pitchY + pitchY/2. - halfChip_Y - tracky

            dr.append(sqrt(resX**2 + resY**2))
            dx.append(resX)
            dy.append(resY)

        return min(dr), dx[dr.index(min(dr))], dy[dr.index(min(dr))]
