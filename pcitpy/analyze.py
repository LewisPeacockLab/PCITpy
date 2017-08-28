import matplotlib.pyplot as plt
plt.close("all")

import sys
import numpy as np

def analyze_outputs(analysis_id,my_bootstrap_id=None,my_scramble_id=None,nRuns=None,my_original_id=None):
	# ANALYZE_OUTPUTS(...)
	#
	# Purpose:
	#
	# Analyse the expectation maximization plus importance sampling results
	#
	# Inputs:
	#
	# analysis_id: Valid analysis Id
	# varargin: If 'bootstrap' then it also expects the total number of bootstrap runs; optional - original run analysis id
	# 	    If 'scramble' then it also expects the total number of scramble runs; optional - original run analysis id
	# 	-- Example 1: analyze_outputs('my_bootstrap_id', 'bootstrap', 100, 'my_original_id')
	# 	-- Example 2: analyze_outputs('my_bootstrap_id', 'bootstrap', 100)
	# 	-- Example 3: analyze_outputs('my_scramble_id', 'scramble', 100, 'my_original_id')
	# 	-- Example 4: analyze_outputs('my_scramble_id', 'scramble', 100)
	#
	# Outputs:
	#
	# Bunch of plots
	#
	# Example usage:
	#
	# analyze_outputs('my_analysis_id')
	# analyze_outputs('my_bootstrap_id', 'bootstrap', 100, 'my_original_id')
	# analyze_outputs('my_bootstrap_id', 'bootstrap', 100)
	# analyze_outputs('my_scramble_id', 'scramble', 100, 'my_original_id')
	# analyze_outputs('my_scramble_id', 'scramble', 100)
	#
	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# This is part of the P-CIT toolbox released under the BSD license.
	# Copyright (c) 2012, Princeton University
	# All rights reserved.
	#
	# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
	#
	# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
	# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in %the documentation and/or other materials provided with the distribution.
	# Neither the name of the Princeton University nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
	# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT %NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	#
	#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	# Set paths
	# Setting the target directory
	root_dir = pwd
	results_dir = root_dir + '/'  + 'results'
	read_dir = results_dir + '/' + analysis_id
	write_dir = results_dir + '/' + analysis_id

	resolution = 2
	credible_interval = 0.9 # credible interval a 0.9 implies that 90% of samples should lie in that interval
	n_bins = 10 # number of bins to plot histgrams
	image_format = 'png'
	alpha = 0.05
	visible_off = True # control whether or not the generated figures pop up on screen or not before being saved to disk.

	# Check length of varargin to determine the type of analysis we're plotting, either one of the following: { regular, bootstrap, scrambled}
	if nRuns is not None:
		x = np.arange(0,1+(1/10**resolution),1/10**resolution)
		y_all_runs = np.full((nRuns,len(x)),np.nan)
		weight_all_runs = np.full((nRuns,1),np.nan)
		if my_bootstrap_id is not None:
			# Individually generate figures for each run, accumulating particle weights and y values for each run
			for b in np.arange(nRuns):
				print('Bootstrap run %i' % b)
				weight_all_runs[b, :], y_all_runs[b, :] = plot_figures('%s_b%d' % (analysis_id, b), read_dir, write_dir, resolution,
													credible_interval, n_bins, image_format, visible_off)
			# Generate a bootstrap specific plot
			if (np.any(np.isnan(y_all_runs)) or np.any(np.isnan(weight_all_runs))):
				raise ValueError('Nan''s in output!')

			plot_boot_results(analysis_id, write_dir, x, y_all_runs, weight_all_runs, alpha, resolution, credible_interval,
													image_format, n_bins, my_bootstrap_id,nRuns,my_original_id)
		elif my_scramble_id is not None:
			# Individually generate figures for each run, accumulating particle weights and y values for each run
			for s in np.arange(nRuns):
				print('Scramble run %i' % s)
				weight_all_runs[s, :] = plot_figures('%s_s%i' % (analysis_id, s), read_dir, write_dir, resolution,
													credible_interval, n_bins, image_format, visible_off)
			# Generate a scramble specific plot
			plot_scram_results(analysis_id, write_dir, weight_all_runs, resolution, image_format, n_bins, my_scramble_id,nRuns,my_original_id)
	else:
		plot_figures(analysis_id, read_dir, write_dir, resolution, credible_interval, n_bins, image_format, visible_off)




