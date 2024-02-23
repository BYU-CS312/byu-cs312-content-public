import cProfile
from GeneSequencing import *

# You can use this script to profile your working implementation.
# Please reach out to Shiloh on Slack if you have any questions... 
# (or if you run into issues with the script.)

class Profiler:
    def __init__(self, banded: bool = False, alignLength: int = 1000) -> None:
        self.seqs = self.loadSequencesFromFile()
        self.processed_results = []
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
        
    # This could just be called via, Proj4GUI.loadSequencesFromFile(), 
    # but it would require the method to be declared static. I didn't want 
    # to change the GeneSequency.py code without Dr. Martinez's 
    # permission though.
    def loadSequencesFromFile(self) -> None:
        FILENAME = 'genomes.txt'
        raw = open(FILENAME,'r').readlines()
        sequences = {}

        i = 0
        cur_id	= ''
        cur_str = ''
        for liner in raw:
            line = liner.strip()
            if '#' in line:
                if len(cur_id) > 0:
                    sequences[i] = (i,cur_id,cur_str)
                    cur_id	= ''
                    cur_str = ''
                    i += 1
                parts = line.split('#')
                cur_id = parts[0]
                cur_str += parts[1]
            else:
                cur_str += line
        if len(cur_str) > 0 or len(cur_id) > 0:
            sequences[i] = (i,cur_id,cur_str)
        return sequences
                    
profiler = Profiler()
runString = "profiler.test()"
cProfile.run(runString)