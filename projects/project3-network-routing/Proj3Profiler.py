import cProfile
import random
import math

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

from Proj3GUI import Proj3GUI
from NetworkRoutingSolver import *
from CS312Graph import *


class Proj3Profiler:
    def __init__(self, doArray: bool = True, \
                 doHeap: bool = True, \
                nPoints: int = 10000, \
                sourceNode: int = 1, \
                targetNode: int = 2) -> None:
        

        SCALE: float = 1.0
        self.data_range = {'x': [-2*SCALE, 2*SCALE], 'y': [-SCALE, SCALE]}
        self.doArray: bool = doArray
        self.doHeap: bool = doHeap
        self.graph = None
        self.nPoints: int = nPoints
        self.sourceNode = sourceNode
        self.targetNode = targetNode
        
    def generateNetwork(self):
        nodes = self.newPoints()
        OUT_DEGREE = 3
        size = len(nodes)
        edgeList = {}
        for u in range(size):
            edgeList[u] = []
            pt_u = nodes[u]
            chosen = []
            for i in range(OUT_DEGREE):
                v = random.randint(0, size-1)
                while v in chosen or v == u:
                    v = random.randint(0, size-1)
                chosen.append(v)
                pt_v = nodes[v]
                uv_len = math.sqrt((pt_v.x()-pt_u.x())**2 +
                                    (pt_v.y()-pt_u.y())**2)
                edgeList[u].append((v, 100.0*uv_len))
            edgeList[u] = sorted(edgeList[u], key=lambda n: n[0])
        self.graph = CS312Graph(nodes, edgeList)
        self.genParams = (1, int(10000))
        self.view.clearEdges()
        self.view.clearPoints()
        self.sourceNode.setText('')
        self.targetNode.setText('')

    def newPoints(self):
        seed = 1
        random.seed(seed)
        ptlist = []
        xr = self.data_range['x']
        yr = self.data_range['y']
        npoints = self.nPoints
        while len(ptlist) < npoints:
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            if True:
                xval = xr[0] + (xr[1]-xr[0])*x
                yval = yr[0] + (yr[1]-yr[0])*y
                ptlist.append(QPointF(xval, yval))
        return ptlist
    
    def generateNetwork(self):
        nodes = self.newPoints()
        OUT_DEGREE = 3
        size = len(nodes)
        edgeList = {}
        for u in range(size):
            edgeList[u] = []
            pt_u = nodes[u]
            chosen = []
            for _ in range(OUT_DEGREE):
                v = random.randint(0, size-1)
                while v in chosen or v == u:
                    v = random.randint(0, size-1)
                chosen.append(v)
                pt_v = nodes[v]
                uv_len = math.sqrt((pt_v.x()-pt_u.x())**2 +
                                   (pt_v.y()-pt_u.y())**2)
                edgeList[u].append((v, 100.0*uv_len))
            edgeList[u] = sorted(edgeList[u], key=lambda n: n[0])
        self.graph = CS312Graph(nodes, edgeList)
    
    def test(self):
        self.generateNetwork()
        solver = NetworkRoutingSolver()
        solver.initializeNetwork(self.graph)

        if self.doArray:
            solver.computeShortestPaths(self.sourceNode - 1, use_heap=False)
            solver.getShortestPath(self.targetNode - 1)
        if self.doHeap:
            solver.computeShortestPaths(self.sourceNode - 1, use_heap=True)
            solver.getShortestPath(self.targetNode - 1)
        
profiler = Proj3Profiler()
runString = "profiler.test()"
cProfile.run(runString)
