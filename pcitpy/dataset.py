def import_mat_data(file):
    import scipy.io
    import pandas as pd
    
    mat = scipy.io.loadmat(file)['data']
    data = {}
    data['subject_id'] = mat[:,0]
    data['trials'] = mat[:,1]
    data['category'] = mat[:,2]
    data['predictor_var'] = mat[:,3]
    data['dependent_var'] = mat[:,4]
    data['net_effect_clusters'] = mat[:,5]

    return pd.DataFrame(data)
