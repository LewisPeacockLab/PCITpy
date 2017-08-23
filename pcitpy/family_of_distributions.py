limport numpy as np

def nans(*args):
    #nan array of arbitrary dimension
    a = np.empty(args, float)*np.nan
    return a

def family_of_distributions(dist, info, *args):
    num_args = len(args)
    if num_args < 2:
        raise ValueError('missing input parameters')

    if dist == 'bernouli':
        output = bernouli_distribution(info, args)
    elif dist == 'normal':
        output = normal_distribution(info, args)
    else:
        raise ValueError('invalid distribution')

def bernouli_distribution(info, input_params)
    if info == 'compute_densities':
        if len(input_params) <= 1:
            raise ValueError('missing input parameters')

        z = input_params[0]
        y = input_params[1]

        #Compute fz = 1 / (1 + exp(-z) - Logistic function
        fz = 1.0 / (1.0 + np.exp(-z))
        fz = max(fz, np.spacing(1))
        fz = min(fz, 1 - np.spacing(1))
        # Compute bern_log_pmf = p ^ k + (1 - p) ^ (1 - k).
        # http://en.wikipedia.org/wiki/Bernoulli_distribution
        # Here p = fz and k = y. Taking the log results in y x log(fz) + (1 - y) x log(1 - fz). 
        out = y * log(fz) + (1 - y) * log(1 - fz)

    elif info == 'fminunc_both_betas':
        if len(input_params) < 3:
            raise ValueError('missing input parameters')
        out = fminunc_bernoulli_both(betas, input_params)

    else:
        raise ValueError('Invalid operation!')

    






        






