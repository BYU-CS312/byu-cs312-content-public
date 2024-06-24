import cProfile
from GeneSequencing import *
from Proj4GUI import Proj4GUI

# You can use this script to profile your working implementation.
# Please reach out to Shiloh on Slack if you have any questions... 
# (or if you run into issues with the script.)

class Proj4Profiler:
    def __init__(self, banded: bool = False, alignLength: int = 1000) -> None:
        self.seqs = Proj4GUI.loadSequencesFromFile()
        self.banded = banded
        self.solver = GeneSequencing()
        self.alignLength = alignLength

    def test(self) -> None:
        sequences = [ self.seqs[i][2] for i in sorted(self.seqs.keys()) ]

        for i in range(len(sequences)):
            for j in range(len(sequences)):
                if(i <= j):
                    self.solver.align(sequences[i], \
                                      sequences[j], \
                                      banded=self.banded, \
                                      align_length=self.alignLength)
                    
profiler = Proj4Profiler()
runString = "profiler.test()"
cProfile.run(runString)