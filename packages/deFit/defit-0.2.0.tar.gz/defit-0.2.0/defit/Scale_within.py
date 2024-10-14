import pandas as pd
from .Init_func import Init_func

def Scale_within(userdata, model=None, center=False, scale=False):
    # Get the variables of the model
    init_list = Init_func(userdata = userdata,model=model,guess=None,method=None,plot=False)
    subject_model = init_list['subject_model']
    var_userdata = init_list['var_model']
    var_model_new = init_list['var_model']
    var_notime_model = var_model_new.loc[var_model_new['field'] != 'time',"field"].tolist()
    var_model = var_model_new.loc[:, "field"].tolist()
    var_notime_userdata = var_model_new.loc[var_model_new['field'] != 'time',"variable"].tolist()
    var_userdata = var_model_new.loc[:, "variable"].tolist()

    # Add the columns of model in userdata
    for i in range(len(var_model)):
        userdata = userdata.copy()
        userdata.loc[:,var_model[i]] = userdata.loc[:,var_userdata[i]]

    # Subtract the means of same subject from subject data
    uni_subject = userdata[subject_model].unique()
    for i_subject in uni_subject:
        for i_var in var_notime_model:
            mid_mean = userdata.loc[userdata[subject_model] == i_subject, i_var].mean()
            mid_center_data = userdata.loc[userdata[subject_model] == i_subject, i_var] - mid_mean
            userdata.loc[userdata[subject_model] == i_subject, i_var] = mid_center_data

    return userdata
