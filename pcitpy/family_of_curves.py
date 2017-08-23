def family_of_curves(curve_type, info, *args)
# Input
# 
# --curve_type: Family of curves, string, e.g. 'horz_indpnt'
# --get_info: Cues for specific information / computation, string, e.g. 'get_nParams'
# --args Is either empty or has arguments depending on the computation
# 
# returns
# 
# --output: Holds the output of all computations

    if len(args) < 2:o
        raise ValueError('missing input parameters')

    if curve_type == 'horz_indpnt'
        output = horz_indpnt_curve(info, args)
    else:
        raise ValueError('invalid curve')

def horz_indpnt_curve(info, input_params):
 # Order of curve parameters y1, x1, x2, y2, y3 and y4
 # Note always x1 will need to precede x2 (both when passing in curve parameters as well as when plotting)
    nparam = 6
    curve_type = 'horz_indpnt'

    if info == 'get_nparam':
        out = nparam 

    elif info == 'get_bounds':
        out = np.array([[-1, 1], [0, 1], [0, 1], [-1, 1], [-1, 1], [-1, 1]])

    elif info == 'get_vertical_params':
        out = np.array([1, 4, 5, 6])

    elif info == 'get_horizontal_params':
        out = np.array([2, 3])

    elif info == 'compute_likelihood':
        if len(input_params) < 6:
            raise ValueError('missing input parameters, needs 6')

        net_effect_clusters = input_params[0]
        particles = input_params[1]
        y1 = input_params[2][:,1]
        x1 = input_params[2][:,2]
        x2 = input_params[2][:,3]
        y2 = input_params[2][:,4]
        y3 = input_params[2][:,5]
        y4 = input_params[2][:,6]
        b0 = input_params[3][1]
        b1 = input_params[3][2]
        data = input_params[4]
        distribution = input_params[5]
        dist_specific_params = input_params[6]

        data_matrix_cols = input_params[7]
        predictor_var_col = data_matrix_cols #predictor col
        dependent_var_col = data_matrix_cols #dependent col
        net_effect_col = data_matrix_cols #net_effect

        if not all(x1 < x2):
            raise ValueError('x1 is not <= x2')

        x = nans(len(net_effect_col),particles)
        y = []

        #In this loop we map the predictor variables to the associated y vals for all curves / particles simulataneously

        for i in range(len(net_effect_clusters)):
            cluster_ind = np.where(data[:,net_effect_col] == net_effect_clusters[i])

            X = np.zeros(len(cluster_ind), particles)
            for j in range(len(cluster_ind)):
                if all(np.isnan(data[cluster_ind[j],predictor_var_col])):
                    x[i,:] = 0
                else:
                    ind3 = np.where(data[cluster_ind[j], predictor_var_col] > x2)
                    # is this boolean indexing ?
                    x2[j,ind3] = (((y4[ind3] - y3[ind3]) / (1 - x2[ind3])) * (data[cluster_ind[j], predictor_var_col] - 1)) + y4[ind3]


                    # If an activation is falling in the second segment of the curve then get the associated y val
                    # segment #2

                    ind2 = ~ind3 & data[cluster_ind[j], predictor_var_col] > x1
                    X[j, ind2] = (((y3[ind2] - y2[ind2]) / (x2[ind2] - x1[ind2])) * (data[cluster[j], predictor_var_col] - x1[ind2])) - x1[ind2] + y2[ind2]
                   
                    # If an activation is falling in the first segment of the curve then get the associated y val
                    # segment #1

                    ind1 = ~ind3 & ~ind2 & data[cluster_ind[j], predictor_var_col] > 0
                    X[j, ind1] = (((y2[ind1] - y1[ind1]) / x1[ind1]) * data[cluster[j], predictor_var_col]) + y1[ind1]
                    
                    # If an activation is at the intercept of the curve then get the associated y val
                    # Intercept (Boundary condition)

                    ind0 = ~ind3 & ~ind2 & ~ind1 & data[cluster[j], predictor_var_col] == 0 
                    X[j, ind0 = y1[ind0]

                    # If an item has net effects then taking the sum below will compute the net effects.
                    # If an item has no net effect then this loop will be executed only once and the sum has no effect
                    x[i, :] = np.sum(X, axis = 0)
            # Our model enforces that the dependent variable will need to be unique 
            # for items within a net effect cluster i.e. all 1's or all 0's

            if len(np.unique(data[cluster_ind, dependent_var_col])) != 1:
                raise ValueError('Dependent var is not unique for net effect cluster %d', i)

            y.append(np.unique(data[cluster_ind, dependent_var_col]))

        if np.any(np.isnan(x)):
            raise ValueError('nans in trials x particles matrix')
        if np.any(np.isinf(x)):
            raise ValueError('Inf in trials x particles matrix')

        z = b1 * x + b0

        out = {}
        out['w'] = family_of_distributions()
        out['net_effects'] = x
        out['dependent_var'] = y

    elif info == 'count_particles':
    else: