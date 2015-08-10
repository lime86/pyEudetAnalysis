# pyEudetAnalysis
Python framework for analysis of EUDET telescope reconstructed data.

This readme assumes you already have a tbtrack.root file.

##### Setting up the environment
Do:
```
source setup_CERN.sh
```

##### Getting access to the calibration data
Do:
```
export EOS_MGM_URL="root://eospublic.cern.ch"
source /afs/cern.ch/project/eos/installation/client/etc/setup.sh
eosmount $HOME/eos
```

For each run (in this example 1189), you need to perform the following steps:

##### Find hot pixels
Do:
```
python FindHotPixels.py -r 1189 -n -1 -d /path/to/tbtrack/file -o /path/to/toplevel/reco/data -e 0. -s Timepix
```

##### Compute alignment
Do:
```
python ComputeAlignment.py -r 1189 -n -1 -m EtaCorrection -d /path/to/tbtrack/file -o /path/to/toplevel/reco/data -e 0. -s Timepix -i 6 -b L04-W0125
```

##### Reconstruction
Do:
```
python pyEudetReconstructionOnly.py -r 1189 -n -1 -m EtaCorrection -d /path/to/tbtrack/file -o /path/to/toplevel/reco/data -a /path/to/alignment/file -e 0. -s Timepix -i 6 -b L04-W0125 
```

##### Analysis
Do:
```
python pyEudetAnalysisOnly.py -r 1189 -n -1 -m EtaCorrection -d /path/to/toplevel/reco/data -o /path/to/toplevel/reco/data -a /path/to/alignment/file -e 0. -s Timepix -i 6 -b L04-W0125
```