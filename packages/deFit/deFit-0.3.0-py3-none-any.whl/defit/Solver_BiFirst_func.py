from scipy.integrate import solve_ivp
import numpy as np
from scipy.optimize import minimize
import pandas as pd
from .opt_Bayes import opt_Bayes

def Solver_BiFirst_func(init_dict):
    ## messages
    print('Program will fit the data with a bivariate first-order differential equation.')
    print('The differential equations are:')
    print('dx/dt = beta1 * x + beta2 * y')
    print('dy/dt = beta3 * x + beta4 * y')
    print('Optimizing...')

    ## identify variables and information
    userdata = init_dict["userdata"]
    modelDF = init_dict["modelDF"]
    field_model = init_dict["field_model"]
    multi_model = init_dict["multi_model"]
    order_model = init_dict["order_model"]
    var_model = init_dict["var_model"]
    guess = init_dict["guess"]
    method = init_dict["method"]
    subject_model = init_dict["subject_model"]
    bayes_obj = init_dict["bayesian_obj"]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_notime_variable = var_model.loc[var_model['field'] != 'time', 'variable'].values
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]

    userdata['time'] = userdata[mid_var_t]
    userdata[mid_notime_field[0]] = userdata[mid_notime_variable[0]]
    userdata[mid_notime_field[1]] = userdata[mid_notime_variable[1]]

    space = {'beta1': bayes_obj(-3, 3),
             'beta2': bayes_obj(-3, 3),
             'beta3': bayes_obj(-3, 3),
             'beta4': bayes_obj(-3, 3),
             'init_x': bayes_obj(-5, 5),
             'init_y': bayes_obj(-15, 15), }
    n_seed = 30
    n_total = 2000
    gamma = 0.8
    ############################
    # optimization
    # --------------------------
    if method == "bayesian":
        print('Estimating parameters by bayesian')
        calc_data = calcBayes_BiFirst_func(userdata,
                                                var_model,
                                                method,
                                                subject_model,
                                                modelDF,
                                                space,
                                                n_seed,
                                                n_total,
                                                gamma,
                                                bayes_obj)
        predict_data = calc_data['predict_data']
        beta1 = calc_data['fixed_effects'][0]
        beta2 = calc_data['fixed_effects'][1]
        beta3 = calc_data['fixed_effects'][2]
        beta4 = calc_data['fixed_effects'][3]
        init_x = calc_data['fixed_effects'][4]
        init_y = calc_data['fixed_effects'][5]
    else:
        calc_data = calc_BiFirst_func(userdata, var_model, guess, method, subject_model, modelDF)
        predict_data = calc_data['predict_data']
        beta1 = calc_data['fixed_effects'].x[0]
        beta2 = calc_data['fixed_effects'].x[1]
        beta3 = calc_data['fixed_effects'].x[2]
        beta4 = calc_data['fixed_effects'].x[3]
        init_x = calc_data['fixed_effects'].x[4]
        init_y = calc_data['fixed_effects'].x[5]

    ## equation
    equation1 = f"{mid_notime_field[0]}(1) = {beta1} * {mid_notime_field[0]} + {beta2} * {mid_notime_field[1]} \n"
    equation2 = f"{mid_notime_field[1]}(1) = {beta3} * {mid_notime_field[0]} + {beta4} * {mid_notime_field[0]} \n"
    equation3 = f"Init t0_{mid_notime_field[0]}:{init_x}; Init t0_{mid_notime_field[1]}:{init_y} \n"
    ## table
    table = pd.DataFrame({"parameter":[f"{mid_notime_field[0]}(0) to {mid_notime_field[0]}(1)",
                                       f"{mid_notime_field[1]}(0) to {mid_notime_field[0]}(1)",
                                       f"{mid_notime_field[0]}(0) to {mid_notime_field[1]}(1)",
                                       f"{mid_notime_field[1]}(0) to {mid_notime_field[1]}(1)"],
                          "value":[beta1,
                                   beta2,
                                   beta3,
                                   beta4]})
    res_dict = {"solve_data":calc_data['fixed_effects'],
                "userdata":userdata,
                "predict_data":predict_data,
                "table":table,
                "equation":[equation1,equation2,equation3],
                "random_effects":None,
                "Neg2LL":calc_data['Neg2LL']}
    return res_dict

def calc_BiFirst_func(userdata,var_model,guess,method,subject_model, modelDF):
    ## fix effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    fix_model = modelDF.loc[modelDF['operator'] == '~', 'fixRand'].tolist()
    guess_e = guess + [0.1,0.1]

    args = [userdata, mid_var_t, mid_num_t, mid_notime_field]
    calcFix_data = minimize(min_BiFirst_func,
                            x0=guess_e,
                            method=method[0],
                            tol=1e-8,
                            options={'disp': False},
                            args=args)
    Neg2LL = calcFix_data.fun + 3.67
    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                 "time": [],
                                 mid_notime_field[0] + "_hat": [],
                                 mid_notime_field[1] + "_hat": []
                                 })
    mid_predict_data = solve_ivp(solve_BiFirst_func,
                                 [0, max(mid_num_t)],
                                 y0=calcFix_data.x[4:6],
                                 t_eval=mid_num_t,
                                 args=[calcFix_data.x[0:4]])
    mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
    mid_predictDF_data.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"}, inplace=True)
    mid_predictDF_data['time'] = np.array(mid_num_t)
    mid_predictDF_data['Subject'] = None
    predict_data = pd.concat([predict_data, mid_predictDF_data], axis=0)
    res_dict = {"fixed_effects": calcFix_data,
                "predict_data": predict_data,
                "Neg2LL":Neg2LL}
    return res_dict

def min_BiFirst_func(x0, args):
    userdata = args[0]
    times = args[2]
    mid_notime_field = args[3]

    mid_solve_data = solve_ivp(solve_BiFirst_func,
                             [0, max(times)],
                             y0=x0[4:6],
                             t_eval=times,
                             args=[x0[0:4]])
    mid_df_res = pd.DataFrame(np.array(mid_solve_data.y).T)
    mid_df_res.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"}, inplace=True)
    mid_df_res['time'] = np.array(mid_solve_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    # fill nan
    res_df.fillna(0,inplace=True)

    # estimating residual in loss function
    guess_xy = [x0[6],x0[7]]
    if x0[6] == 0:
        guess_xy[0] = 0.00001
    if x0[7] == 0:
        guess_xy[1] = 0.00001

    log_ex = np.log(guess_xy[0] ** 2)
    log_ey = np.log(guess_xy[1] ** 2)
    inverse_ex = 1 / (guess_xy[0] ** 2)
    inverse_ey = 1 / (guess_xy[1] ** 2)
    mid_var_x = mid_notime_field[0]
    mid_var_y = mid_notime_field[1]
    res_df[mid_var_x + '_err'] = log_ex + ((res_df[mid_var_x] - res_df[mid_var_x + "_hat"]) ** 2) * inverse_ex
    res_df[mid_var_y + '_err'] = log_ey + ((res_df[mid_var_y] - res_df[mid_var_y + "_hat"]) ** 2) * inverse_ey
    res_sum = [res_df[mid_var_x + '_err'].sum() , res_df[mid_var_y + '_err'].sum()]

    # res_sum = []
    # num_i = 0
    # for i in mid_notime_field:
    #     # reset the data
    #     res_df.loc[res_df[i + "_hat"] > 1e+50,i + "_hat"] = 0
    #     res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
    #     res_df = res_df.replace([np.inf, -np.inf], 0)
    #     # calcate the MSE
    #     log_e = np.log(guess_xy[num_i]**2)
    #     inverse_e = 1/(guess_xy[num_i]**2)
    #     res_df[i + "_err"] = log_e + ((res_df[i] - res_df[i + "_hat"]) ** 2) * inverse_e
    #     # res_df[i + "_err"] =  (res_df[i] - res_df[i + "_hat"]) ** 2
    #     num_i = num_i + 1
    #     res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)

def solve_BiFirst_func(t, y0, args):
    mid_args_list = list(args)
    dxdt = mid_args_list[0] * y0[0] + mid_args_list[1] * y0[1]
    dydt = mid_args_list[2] * y0[0] + mid_args_list[3] * y0[1]
    return [dxdt, dydt]

############################
# Bayesian optimization
# --------------------------
def calcBayes_BiFirst_func(userdata,var_model,
                                method,
                                subject_model,
                                modelDF,
                                space,
                                n_seed,
                                n_total,
                                gamma,
                                bayes_obj):
    ## fix effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    fix_model = modelDF.loc[modelDF['operator'] == '~', 'fixRand'].tolist()
    args = {"mid_notime_field": mid_notime_field,
            "subject_model": subject_model}
    calcFix_data = opt_Bayes(userdata,
                             space,
                             n_seed,
                             n_total,
                             gamma,
                             fmin_rmse=fmin_BiFirst_rmse,
                             args=args)
    bayesFix_data = calcFix_data[calcFix_data['rmse'] == calcFix_data['rmse'].min()]
    bayesFix_best_data = bayesFix_data.iloc[0, :].values
    print('bayesFix_data', bayesFix_data)
    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                 "time": [],
                                 mid_notime_field[0] + "_hat": [],
                                 mid_notime_field[1] + "_hat": []
                                 })
    mid_predict_data = solve_ivp(solve_BiFirst_func,
                                 [0, max(mid_num_t)],
                                 y0=bayesFix_best_data[4:6],
                                 t_eval=mid_num_t,
                                 args=[bayesFix_best_data[0:4]])
    mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
    mid_predictDF_data.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"}, inplace=True)
    mid_predictDF_data['time'] = np.array(mid_num_t)
    mid_predictDF_data['Subject'] = None
    predict_data = pd.concat([predict_data, mid_predictDF_data], axis=0)
    res_dict = {"fixed_effects": bayesFix_data,
                "predict_data": predict_data}
    print(res_dict)
    return res_dict

def fmin_BiFirst_rmse(userdata,parms,args):
    times = userdata.loc[:, 'time'].sort_values(ascending=True).unique().tolist()
    mid_y0 = [parms[4], parms[5]]
    mid_args = [parms[0], parms[1], parms[2], parms[3]]
    mid_min_data = solve_ivp(solve_BiFirst_func,
                             [0, 1000],
                             y0=mid_y0,
                             args=[mid_args],
                             t_eval=times
                             )
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: args["mid_notime_field"][0] + "_hat", 1: args["mid_notime_field"][1] + "_hat"},
                      inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time", how="outer")
    res_df.fillna(0, inplace=True)
    res_sum = []
    for i in args["mid_notime_field"]:
        res_df.loc[res_df[i + "_hat"] > 1e+50, i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)