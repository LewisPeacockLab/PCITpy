#!/bin/bash
export LM_LICENSE_FILE=~/.tacc_matlab_license
command=$1

opt="-nodesktop -nodisplay -nosplash"

max_attempts=20
n_attempt=0
echo "Matlab command: $command"
echo "Attempting to launch Matlab..."
cd /work/03034/twang04/lonestar/software/imdif/analysis/P-CIT
cmd="module load matlab; matlab $opt -r \"$command; exit\""
until bash -l -c "$cmd"; do
    echo "Launch attempt failed. Will try again in 30 seconds..."
    sleep 30
    let n_attempt++
    if [ $n_attempt -gt $max_attempts ]; then
	echo "Attempted to start Matlab $n_attempt times. Quitting..."
    fi
done
