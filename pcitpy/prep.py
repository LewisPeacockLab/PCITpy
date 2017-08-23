
import pandas as pd
import numpy as np
import random

def default_opt():
    opt = {} # Creating a dictionary
    opt['analysis_id'] = 'my_analysis_id' # analysis_id: specifies the target directory
    opt['em_iterations'] = 20 # Number of expectation maximization iterations
    opt['particles'] = 100000 # Number of particles to be used in the importance sampling algorithm
    opt['curve_type'] = 'horz_indpnt' # Name of the family of curves to be used. Refer to the family_of_curves.m file for more info
    opt['distribution'] = 'bernoulli' # Name of the distribution (and the default canonical link function which maps the predictor variable to the dependent variable)
    opt['dist_sigma'] = 1

    opt['beta_0'] = 0 # Initializing beta_0 for linear predictor
    opt['beta_1'] = 1 # Initializing beta_1 for linear predictor
    opt['tau'] = 0.05 # Specifies the radius to sample curves in the curve space
    opt['category'] = None # Specifies if the analyses will need to run on a specific category. Vector length Should be greater than 0. For instance [2] will cause the analyses to be run only on the second category; [] will run the analyses on all categories

    opt['drop_outliers'] = 3 # specifies how many std dev away from group mean will the predictor variable outliers need to be dropped
    opt['zscore_within_subjects'] = False # if TRUE, the independednt variables will be zscored within each suibject

    opt['resolution'] = 4 # Denotes the resolution in which the data will be processed
    opt['particle_chunks'] = 2 # Denotes the number of chunks you plan to partition the trials x particles matrix. An example chunk size will be 2 for a 3000 x 50,000 matrix

    opt['bootstrap'] = False # indicates that this run is a bootstrap run
    opt['bootstrap_run'] = -1 # will need to specify a bootstrap sample number. This will need to be unique for each sample

    opt['scramble'] = False # indicates that this run is a scramble run
    opt['scramble_run'] = -1 # will need to specify a scramble sample number. This will need to be unique for each sample
    opt['scramble_style'] = -1 # choosing the appropriate scramble option from three options below
    return opt

def scramble_dep_var(dep, clust):
    """Scramble dependent variable across clusters.
    
    Parameters
    ----------
    dep : array_like
        Array of dependent variables.
    clust : array_like
        Array of cluster labels.

    Returns
    -------
    dep_rand : array
        Array of dependent variables scrambled across clusters.
    """

    if not dep.shape == clust.shape:
        raise ValueError('Size of input vectors must be the same.')

    # get all clusters and corresponding dependent variables
    clust_all = np.unique(clust)
    clust_dep = [dep[clust==i][0] for i in clust_all]

    # randomize across clusters
    clust_dep_rand = random.sample(clust_dep, len(clust_dep))

    # assign randomized dependent variables to sorted cluster vector
    dep_rand = np.zeros(np.shape(dep))
    for i, c in enumerate(clust_all):
        dep_rand[clust==c] = clust_dep_rand[i]
    return dep_rand

def prep_bootstrap(data):
    """Create a data set for bootstrap analysis.
    
    Parameters
    ----------
    data : DataFrame
        Standard DataFrame with data.

    Returns
    -------
    boot_data : DataFrame
        Data with subjects sampled with replacement.
    """
    
    subjects = np.unique(data['subject_id'])
    boot_subjects = random.choices(subjects, k=len(subjects))
    boot_data = data.copy()
    new_subject_count = 0
    new_cluster_count = 0
    for i, subj in enumerate(boot_subjects):
        new_subject_count += 1
        subj_ind = np.nonzero(data['subject_id'] == subj)[0]
        start = (new_subject_count - 1) * len(subj_ind)
        boot_subj_ind = np.arange(start, start + len(subj_ind))

        # set new subject index
        subj_clust = data.loc[subj_ind,'net_effect_clusters']
        boot_data.loc[boot_subj_ind,'subject_id'] = new_subject_count
        for clust in np.unique(subj_clust):
            new_cluster_count += 1
            clust_ind = boot_subj_ind[np.nonzero(subj_clust == clust)[0]]
            boot_data.loc[clust_ind,'net_effect_clusters'] = new_cluster_count
        
        # copy information from the original subject to the bootstrap
        # subject
        copy_fields = ['category', 'dependent_var',
                       'predictor_var', 'trials']
        for f in copy_fields:
            boot_data.loc[boot_subj_ind,f] = data.loc[subj_ind,f].values
        
    return boot_data, boot_subjects

def setup(data_in, opt):

    # make a copy of the data, for easy comparison of input data and
    # output data; could remove this when initial development is
    # finished
    data = data_in.copy()
    
    # TODO: print warnings if options not defined
    if not 'em_iteractions' in opt or opt['em_iterations'] <= 0:
        opt['em_iterations'] = 20
        
    if not 'particles' in opt or opt['particles'] <= 0:
        opt['particles'] = 100000

    if not 'curve_type' in opt or not opt['curve_type']:
        opt['curve_type'] = 'horz_indpnt'

    # TODO: Check if the family of curves exist by fetching the
    # number of curve parameters. This is just a sanity check

    if not 'distribution' in opt or not opt['distribution']:
        if len(np.unique(data['dependent_var'])) == 2:
            opt['distribution'] = 'bernoulli'
        else:
            opt['distribution'] = 'normal'

    if not 'dist_specific_params' in opt or not opt['dist_specific_params']:
        if opt['distribution'] is 'bernoulli':
            opt['dist_specific_params'] = {}
        elif opt['distribution'] is 'normal':
            dpar = {}
            dpar['sigma'] = 1
            opt['dist_specific_params'] = dpar
        # original code had prompt at this point to check for parameters

    if opt['distribution'] is 'normal' and opt['dist_specific_params']['sigma'] <= 0:
        raise ValueError('Normal distribution sigma must be greater than 0.')

    if not 'beta_0' in opt:
        opt['beta_0'] = 0

    if not 'beta_1' in opt:
        opt['beta_1'] = 1

    if not 'tau' in opt or opt['tau'] <= 0:
        opt['tau'] = 0.05
        
    if not 'bootstrap' in opt:
        opt['bootstrap'] = False
    elif not isinstance(opt['bootstrap'], bool):
        raise ValueError('bootstrap setting must be boolean.')

    if not 'scramble' in opt:
        opt['scramble'] = False
    elif not isinstance(opt['scramble'], bool):
        raise ValueError('scramble setting must be boolean.')

    if opt['bootstrap'] and opt['scramble']:
        raise ValueError('Cannot run scramble and bootstrap analysis at the same time.')

    # get only categories of interest
    if not 'category' in opt:
        opt['category'] = None
    elif opt['category'] is not None:
        data = data.loc[np.in1d(data['category'].values, opt['category'])]

    if not 'drop_outliers' in opt:
        opt['drop_outliers'] = 3
        
    if opt['drop_outliers'] > 0:
        nan_free_idx = np.nonzero(np.logical_not(np.isnan(data['predictor_var'].values)))
        nan_idx = np.nonzero(np.isnan(data['predictor_var'].values))
        nan_free_data = data.loc[nan_free_idx]
        std_pred = np.std(nan_free_data['predictor_var']) * opt['drop_outliers']
        mean_pred = np.mean(nan_free_data['predictor_var'])
        include = np.logical_and(nan_free_data['predictor_var'] > (mean_pred - std_pred), nan_free_data['predictor_var'] < (mean_pred + std_pred))
        data = pd.concat((nan_free_data, data.loc[nan_idx]))

    if np.shape(data)[0] == 0:
        raise ValueError('No trials in input data.')

    if not 'zscore_within_subjects' in opt:
        opt['zscore_within_subjects'] = 0
    elif not isinstance(opt['zscore_within_subjects'], bool):
        raise ValueError('zscore_within_subjects setting must be boolean.')

    return data, opt
    
