import numpy as np
import pandas as pd
def Info_func(userdata,predict,var_notime_field,table,field_model,order_model,multi_model,subject_model):
    # Implement Hessian_BiFirst_func here (you need to define this function)
    rsquared_data = Rsquared_func(userdata, predict,var_notime_field,order_model,multi_model)
    RMSE_data = RMSE_func(userdata, predict,var_notime_field)
    # Hessian_BiFirst_data = Hessian_BiFirst_func(solve_data.hess_inv)
    # SE_vector = np.diagonal(Hessian_BiFirst_data)
    # if len(var_notime_field) == 1:
    #     SE_vector = np.array([SE_vector[0], SE_vector[1], SE_vector[2], SE_vector[3]])
    table = {}  # Initialize your table as a dictionary
    # table['SE'] = SE_vector
    return {
        'rsquared_data': rsquared_data,
        'RMSE': RMSE_data,
        # 'SE': SE_vector.tolist(),  # Convert to list for compatibility
        'table': table
    }
def Rsquared_func(userdata, predict, var_notime_field,order_model,multi_model):
    print('Estimating R_squared')
    cor_list = []
    # if there is multilevel model we should merge the data by subject and time
    if not multi_model:
        combine_data = pd.merge(userdata, predict, on=['time'],how="outer")
    else:
        combine_data = pd.merge(userdata, predict, on=['Subject','time'], how="outer")
    for i in range(len(var_notime_field)):
        mid_cor = np.corrcoef(combine_data[var_notime_field[i]], combine_data[var_notime_field[i] + "_hat"])[0, 1]
        cor_list.append(mid_cor)
    cor_list = np.array(cor_list) ** 2
    return cor_list

def RMSE_func(userdata, predict ,var_notime_field):
    print('Estimating RMSE')
    RMSE_res = []

    for i in range(len(var_notime_field)):
        SSxe = np.sum((userdata.loc[:,var_notime_field[i]] - predict.loc[:,var_notime_field[i]+"_hat"])**2)
        RMSEx = np.sqrt(SSxe / len(userdata['time']))
        RMSE_res.append(RMSEx)

    return RMSE_res

def Hessian_BiFirst_func(hessian):
    print('Estimating Hessian')
    print(hessian.toarray())
    hessian[hessian < 0] = np.nan
    mid_SE = np.sqrt(1 / hessian)
    return mid_SE