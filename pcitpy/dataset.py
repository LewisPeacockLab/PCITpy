"""Functions for importing and working with datasets."""

def import_mat_data(file):
    """Load a dataset from a MAT-file with standard format.

    Parameters
    ----------
    file : str
        Path to MAT-file with data for P-CIT. Must contain one matrix
        named 'data', with the following columns:
            1. subject_id
            2. trials
            3. category
            4. predictor_var
            5. dependent_var
            6. net_effect_clusters

    Returns
    -------
    data : DataFrame
        Dataset in standard format.
    """
    
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
