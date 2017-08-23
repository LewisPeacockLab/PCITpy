
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
    
    import numpy as np
    import random

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

def setup(data, opt):

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
        raise ValueError('Bootstrap field must be boolean.')

    if not 'scramble' in opt:
        opt['scramble'] = False
    elif not isinstance(opt['scramble'], bool):
        raise ValueError('Scramble field must be boolean.')

    if opt['bootstrap'] and opt['scramble']:
        raise ValueError('Cannot run scramble and bootstrap analysis at the same time.')
    
    return data, opt
    
