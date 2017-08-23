# MAKE SURE THAT IF YOU'RE GOING FROM MATLAB TO PYTHON YOU REMEMBER TO DECREASE YOUR DIMENSION SPECIFICATION BY 1
# FOR EXAMPLE, the Matlab default dimension is 1, and for this Python script it's 0

import numpy as np
import scipy
from scipy import misc

def logsumexp(a, dim=0):

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #% Note: This a third party file written by Tom Minka
    #% Url: http://code.google.com/searchframe#ZEPi4rAjpWE/trunk/toolbox/util/stats/logsumexp.m
    #% The MIT License
    #%
    #% Copyright (2010) Kevin Murphy and Matt Dunham
    #%
    #% Permission is hereby granted, free of charge, to any person obtaining a copy
    #% of this software and associated documentation files (the "Software"), to deal
    #% in the Software without restriction, including without limitation the rights
    #% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    #% copies of the Software, and to permit persons to whom the Software is
    #% furnished to do so, subject to the following conditions:
    #%
    #% The above copyright notice and this permission notice shall be included in
    #% all copies or substantial portions of the Software.
    #%
    #% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    #% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    #% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    #% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    #% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    #% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    #% THE SOFTWARE.
    #% Return log(sum(exp(a), dim)) while avoiding numerical underflow
    #% Default is dim = 1 (rows) returns a row vector
    #% logsumexp(a, 2) will sum across columns and return a column vector.
    #% Unlike matlab's "sum", it will not switch the summing direction
    #% if you provide a row vector.
    #%
    #PMTKauthor Tom Minka
    # (c) Microsoft Corporation. All rights reserved.
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # subtract the largest in each column
    # have to add another dimension
    if np.ndim(a) == 1:
        a = np.reshape(a,(1,len(a)))

    y = np.amax(a,axis=dim)
    i = np.argmax(a,axis=dim)
    dims = np.ones(np.ndim(a))
    dims[dim] = np.size(a,axis=dim)
    a = a - y
    s = y + np.log(np.sum(np.exp(a),axis=dim))
    isFin = np.isfinite(y)
    i = np.where(~isFin)
    if ~np.all(isFin):
        s[i] = y[i]


    return s