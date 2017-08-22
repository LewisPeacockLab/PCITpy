
def default_opt():
    analysis_settings = {} # Creating a dictionary
    analysis_settings['analysis_id'] = 'my_analysis_id' # analysis_id: specifies the target directory
    analysis_settings['em_iterations'] = 20 # Number of expectation maximization iterations
    analysis_settings['particles'] = 100000 # Number of particles to be used in the importance sampling algorithm
    analysis_settings['curve_type'] = 'horz_indpnt' # Name of the family of curves to be used. Refer to the family_of_curves.m file for more info
    analysis_settings['distribution'] = 'bernoulli' # Name of the distribution (and the default canonical link function which maps the predictor variable to the dependent variable)
    analysis_settings['dist_sigma'] = 1

    analysis_settings['beta_0'] = 0 # Initializing beta_0 for linear predictor
    analysis_settings['beta_1'] = 1 # Initializing beta_1 for linear predictor
    analysis_settings['tau'] = 0.05 # Specifies the radius to sample curves in the curve space
    analysis_settings['category'] = None # Specifies if the analyses will need to run on a specific category. Vector length Should be greater than 0. For instance [2] will cause the analyses to be run only on the second category; [] will run the analyses on all categories

    analysis_settings['drop_outliers'] = 3 # specifies how many std dev away from group mean will the predictor variable outliers need to be dropped
    analysis_settings['zscore_within_subjects'] = False # if TRUE, the independednt variables will be zscored within each suibject

    analysis_settings['resolution'] = 4 # Denotes the resolution in which the data will be processed
    analysis_settings['particle_chunks'] = 2 # Denotes the number of chunks you plan to partition the trials x particles matrix. An example chunk size will be 2 for a 3000 x 50,000 matrix

    analysis_settings['bootstrap'] = False # indicates that this run is a bootstrap run
    analysis_settings['bootstrap_run'] = -1 # will need to specify a bootstrap sample number. This will need to be unique for each sample

    analysis_settings['scramble'] = False # indicates that this run is a scramble run
    analysis_settings['scramble_run'] = -1 # will need to specify a scramble sample number. This will need to be unique for each sample
    analysis_settings['scramble_style'] = -1 # choosing the appropriate scramble option from three options below
    return analysis_settings

def setup(data, opt):

    if not opt.has_key('em_iteractions') or opt['em_iterations'] <= 0:
        opt['em_iterations'] = 20
        
    if not opt.has_key('particles') or opt['particles'] <= 0:
        opt['particles'] = 100000

    if not opt.has_key('curve_type') or not opt['curve_type']:
        opt['curve_type'] = 'horz_indpnt'

    # TODO: Check if the family of curves exist by fetching the
    # number of curve parameters. This is just a sanity check
