# distanceEuclidienne.pyx claude B
# distutils: language = c++
# distutils: sources = distanceEuclidienne.cpp

cimport cython
from libcpp.vector cimport vector

cdef extern from "distanceEuclidienne.cpp":
    cdef cppclass DistanceCalculator:
        @staticmethod
        double distanceEuclidienne(const vector[double]& point1, const vector[double]& point2) except +

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def distance_euclidienne(list point1, list point2):
    cdef vector[double] cpp_point1 = point1
    cdef vector[double] cpp_point2 = point2
    return DistanceCalculator.distanceEuclidienne(cpp_point1, cpp_point2)
