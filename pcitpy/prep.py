"""Functions for preparing P-CIT analysis."""

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
    opt['bootstrap_run'] = None # will need to specify a bootstrap sample number. This will need to be unique for each sample

    opt['scramble'] = False # indicates that this run is a scramble run
    opt['scramble_run'] = None # will need to specify a scramble sample number. This will need to be unique for each sample
    opt['scramble_style'] = None # choosing the appropriate scramble option from three options below
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
    dep = np.asarray(dep)
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

    # randomly sample subjects with replacement
    subjects = data['subject_id'].unique()
    boot_subjects = random.choices(subjects, k=len(subjects))

    # copy so the original data will not be modified
    boot_data = data.copy()
    new_subject_count = 0
    new_cluster_count = 0
    for i, subj in enumerate(boot_subjects):
        # source subject indices and boot subject indices
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
        boot_data.loc[boot_subj_ind,copy_fields] = data.loc[boot_subj_ind,copy_fields].values
        
    return boot_data, boot_subjects

def prep_scramble(data, scramble):
    """Create scrambled data set.
    
    Parameters
    ----------
    data : DataFrame
        Standard DataFrame with data.
    scramble : str
        Type of scrambling to use:
            'within_subjects_within_categories'
            'within_subjects_across_categories'
            'across_subjects_across_categories'
    
    Returns
    -------
    sdata : DataFrame
        Scrambled data.
    """
    
    sdata = data.copy()
    dep = data['dependent_var']
    clust = data['net_effect_clusters']
    if scramble == 'within_subjects_within_categories':
        for subject in data['subject_id'].unique():
            for category in data['category'].unique():
                ind = np.logical_and(data['subject_id'] == subject,
                                     data['category'] == category)
                sdata.loc[ind,'dependent_var'] = scramble_dep_var(dep[ind],
                                                                  clust[ind])

    elif scramble == 'within_subjects_across_categories':
        for subject in data['subject_id'].unique():
            ind = data['subject_id'] == subject
            sdata.loc[ind,'dependent_var'] = scramble_dep_var(dep[ind],
                                                              clust[ind])

    elif scramble == 'across_subjects_across_categories':
        sdata['dependent_var'] = scramble_dep_var(dep, clust)

    else:
        raise ValueError('Invalid scramble style: {}'.format(scramble))
    return sdata

def setup(data_in, opt):
    """Run basic setup of data and analysis settings.

    Parameters
    ----------
    data_in : DataFrame
        Input DataFrame with all data.
    opt : dict
        Dictionary with analysis settings.
    
    Returns
    -------
    data_in : DataFrame
        Output DataFrame with bootstrap sampling and scrambling applied.
    opt : dict
        Dictionary with updated analysis settings.
    """    
    
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
        if opt['distribution'] == 'bernoulli':
            opt['dist_specific_params'] = {}
        elif opt['distribution'] == 'normal':
            dpar = {}
            dpar['sigma'] = 1
            opt['dist_specific_params'] = dpar
        # original code had prompt at this point to check for parameters

    if opt['distribution'] == 'normal' and opt['dist_specific_params']['sigma'] <= 0:
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
        
    if opt['drop_outliers'] is not None:
        pred = data['predictor_var']
        pred_std = pred.std()
        pred_mean = pred.mean()
        lower = pred_mean - (pred_std * opt['drop_outliers'])
        upper = pred_mean + (pred_std * opt['drop_outliers'])
        data = data.loc[pred.between(lower, upper),:]

    if np.shape(data)[0] == 0:
        raise ValueError('No trials in input data.')

    if not 'zscore_within_subjects' in opt:
        opt['zscore_within_subjects'] = 0
    elif not isinstance(opt['zscore_within_subjects'], bool):
        raise ValueError('zscore_within_subjects setting must be boolean.')
    
    if opt['zscore_within_subjects']:
        pred = data['predictor_var']
        data['predictor_var'] = (pred - pred.mean()) / pred.std()

    if not 'resolution' in opt:
        opt['resolution'] = 4

    if opt['distribution'] == 'normal':
        # If normally distributed data, want to z-score the dependent
        # variable
        dep = data['dependent_var']
        data['dependent_var'] = (dep - dep.mean()) / dep.std()

    # scale predictor between 0 and 1
    pred = data['predictor_var']
    data['predictor_var'] = (pred - pred.min()) / (pred.max() - pred.min())

    # set predictor resolution
    data['predictor_var'] = np.round(data['predictor_var'], opt['resolution'])

    if opt['scramble'] and not opt['bootstrap']:
        if not 'scramble_run' in opt:
            raise IOError('scramble_run not set.')
        if not 'scramble_style' in opt:
            opt['scramble_style'] = 'within_subjects_within_categories'

        data = prep_scramble(data, opt['scramble_style'])

    # verify that the subject ID and dependent variable are unique
    # within each cluster
    uclusters = data['net_effect_clusters'].unique()
    if len(uclusters) < data.shape[0]:
        for cluster in uclusters:
            ind = data['net_effect_clusters'] == cluster
            if len(data.loc[ind,'subject_id'].unique()) > 1:
                raise ValueError('Subject ID is not unique for all net effect clusters.')
            if len(data.loc[ind,'dependent_var'].unique()) > 1:
                raise ValueError('Dependent variable is not unique for all net effect clusters.')
    
    return data, opt
    
