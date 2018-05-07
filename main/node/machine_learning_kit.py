import numpy

def correlation(e1, e2):
    '''take two random variables and return correlation coefficient'''
    return numpy.corrcoef(e1,e2)[1][0]

