#Scale data function

# [SCALED] = SCALE_DATA(DATA, LOWER, UPPER)
# 
# Purpose:
#
# Scale the elements of all the column vectors in Data within the range of [Lower Upper]; default range is [-1 1]
#
# Inputs:
#
# --Data: data, numeric vector e.g. [8.3256, 1000, 23, 564]
# --Lower: lower range, numeric e.g. 0
# --Upper: upper range, numeric e.g. 1
#
# Outputs:
#
# --scaled: scaled data
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This is part of the P-CIT toolbox released under the BSD license.
# Copyright (c) 2012, Princeton University
# 2017, UT Austin, Princeton, Intel
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in %the documentation and/or other materials provided with the distribution.
# Neither the name of the Princeton University nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT %NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#takes number of input arguments
import sys
import numpy as np 

def setup(data):

	if len(sys.argv) < 3:
		lower = -1
		upper = 1
	elif lower > upper:
		print ("Wrong Lower or Upper Values!")

	maxv = np.amax(data)
	minv = np.amin(data)

	r,c = data.shape

	scaled = (data - np.ones((r,1), dtype=int) * minv) .* np.ones((r,1), dtype=int) * ((upper - lower) * np.ones((1,c), dtype=int) ./ (maxv - minv))) + lower;

	return(data,scaled)
