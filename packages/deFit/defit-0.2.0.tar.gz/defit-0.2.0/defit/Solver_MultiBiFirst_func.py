import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from .opt_Bayes import opt_Bayes
import re
import math

def Solver_MultiBiFirst_func(init_dict):
    print('Program will fit the data with multilevel bivariate first-order differential equations.')
    print('The multilevel differential equations are:')
    print('dx/dt = (beta1 + etaI1) * x + (beta2 + etaI2) * y')
    print('dy/dt = (beta3 + etaI3) * x + (beta4 + etaI4) * y')
    print('Optimizing...')

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

    space = {'beta1':bayes_obj(-3,3),
                'beta2':bayes_obj(-3,3),
               'beta3':bayes_obj(-3,3),
               'beta4':bayes_obj(-3,3),
               'init_x':bayes_obj(-20,20),
               'init_y':bayes_obj(-20,20),}
    n_seed = 30
    n_total = 2000
    gamma = 0.8
    ############################
    # optimization
    # --------------------------
    if method[0]=="bayesian":
        calc_data = calcBayes_MultiBiFirst_func(userdata,
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
        random_effects = calc_data["random_effects"]
        fixed_effects = calc_data['fixed_effects']
        bayesFix_data = fixed_effects[fixed_effects['rmse'] == fixed_effects['rmse'].min()]
        bayesFix_best_data = bayesFix_data.iloc[0, :].values
        beta1 = bayesFix_best_data[0]
        beta2 = bayesFix_best_data[1]
        beta3 = bayesFix_best_data[2]
        beta4 = bayesFix_best_data[3]
        init_x = bayesFix_best_data[4]
        init_y = bayesFix_best_data[5]
    elif init_dict['fixed_first'] == False:
        calc_data = calc_MultiBiFirst_United_func(userdata, var_model, guess, method, subject_model, modelDF)
        predict_data = calc_data['predict_data']
        random_effects = calc_data["random_effects"]
        beta1 = calc_data['fixed_effects']['fixed_beta1'].values[0]
        beta2 = calc_data['fixed_effects']['fixed_beta2'].values[0]
        beta3 = calc_data['fixed_effects']['fixed_beta3'].values[0]
        beta4 = calc_data['fixed_effects']['fixed_beta4'].values[0]
        init_x = calc_data['fixed_effects']['fixed_init1'].values[0]
        init_y = calc_data['fixed_effects']['fixed_init2'].values[0]
    else:
        calc_data = calc_MultiBiFirst_func(userdata, var_model, guess, method, subject_model, modelDF)
        predict_data = calc_data['predict_data']
        random_effects = calc_data["random_effects"]
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
                "random_effects":random_effects,
                "Neg2LL":calc_data['Neg2LL']}
    return res_dict

def calc_MultiBiFirst_func(userdata,var_model,guess,method,subject_model, modelDF):
    ## identify variables and information

    ## fixed effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    mid_num_t = [x for x in mid_num_t if not math.isnan(x)]
    fix_model = modelDF.loc[modelDF['operator'] == '~','fixRand'].tolist()
    # mid_userdata = userdata.loc[:,var_model.loc[:,'variable'].tolist()]
    # rename_key = {k: v for k, v in zip(var_model.loc[:,'variable'].tolist(), var_model.loc[:,'field'].tolist())}
    # mid_userdata.rename(columns=rename_key,inplace=True)
    # mid_userdata["subject"] = userdata.loc[:,subject_model]
    args= [userdata,mid_var_t,mid_num_t,mid_notime_field]
    calcFix_data = minimize(calcFix_MultiBiFirst_func,
                                    x0=guess[0]+[0.1,0.1], # [1,1] estimating residual in loss function
                                    method=method[0],
                                    tol=1e-8,
                                    options={'disp': False},
                                    args=args)
    Neg2LL = calcFix_data.fun + 3.67
    randEffect_data = pd.DataFrame({"Subject":[],
                               "EtaI_1":[],
                               "EtaI_2":[],
                               "EtaI_3":[],
                               "EtaI_4":[],
                               "EtaI_x":[],
                               "EtaI_y":[]})

    # subject_guess
    # --------------------------
    subject_guess = guess[1]
    if not re.search('1', fix_model[0]):
        subject_guess[4] = False
    if not re.search('1', fix_model[1]):
        subject_guess[5] = False
    if not re.search(mid_notime_field[0], fix_model[0]):
        subject_guess[0] = False
    if not re.search(mid_notime_field[1], fix_model[0]):
        subject_guess[1] = False
    if not re.search(mid_notime_field[0], fix_model[1]):
        subject_guess[2] = False
    if not re.search(mid_notime_field[1], fix_model[1]):
        subject_guess[3] = False

    uni_subject_list = userdata[subject_model].unique().tolist()
    uni_subject_list = [x for x in uni_subject_list if not math.isnan(x)]
    for index,i_subject in enumerate(uni_subject_list):
        print(f'Estimating random effects {i_subject}')
        mid_userdata = userdata.loc[userdata[subject_model] == i_subject]
        sub_args = [mid_userdata, mid_var_t, mid_num_t, mid_notime_field, guess[1], subject_guess, calcFix_data.x]
        mid_calcRandom_data = minimize(calcRand_MultiBiFirst_func,
                                    x0=guess[1] + [0.1,0.1],# [1,1] estimating residual in loss function
                                    method=method[1],
                                    tol=1e-8,
                                    options={'disp': False},
                                    args=sub_args)
        new_row = [i_subject] + mid_calcRandom_data.x.tolist()[0:6]
        new_row_df = pd.DataFrame([new_row],columns=randEffect_data.columns)
        randEffect_data = pd.concat([randEffect_data, new_row_df], ignore_index=True)
    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                    "time": [],
                                    mid_notime_field[0]+"_hat": [],
                                    mid_notime_field[1]+"_hat": []
                                 })
    times = mid_num_t
    for index,i_subject in enumerate(uni_subject_list):
        randEffect_parms = randEffect_data.loc[randEffect_data['Subject'] == i_subject,:]
        mid_predict_y0 = [calcFix_data.x[4] + randEffect_parms.loc[index,'EtaI_x'],
                          calcFix_data.x[5] + randEffect_parms.loc[index,'EtaI_y']]

        mid_predict_parms = [calcFix_data.x[0] + randEffect_parms.loc[index,'EtaI_1'],
                          calcFix_data.x[1] + randEffect_parms.loc[index,'EtaI_2'],
                          calcFix_data.x[2] + randEffect_parms.loc[index,'EtaI_3'],
                          calcFix_data.x[3] + randEffect_parms.loc[index,'EtaI_4']]
        mid_predict_data = solve_ivp(solve_MultiBiFirst_func,
                                 [0, max(mid_num_t)],
                                 y0=mid_predict_y0,
                                 t_eval=mid_num_t,
                                 args=[mid_predict_parms])
        mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
        mid_predictDF_data.rename(columns={0:mid_notime_field[0]+"_hat",1:mid_notime_field[1]+"_hat"},inplace=True)
        mid_predictDF_data['time'] = np.array(mid_num_t)
        mid_predictDF_data['Subject'] = i_subject
        predict_data = pd.concat([predict_data,mid_predictDF_data],axis=0)
    res_dict = {"fixed_effects":calcFix_data,
                "random_effects":randEffect_data,
                "predict_data":predict_data,
                "Neg2LL":Neg2LL}
    return res_dict

def calcFix_MultiBiFirst_func(x0, args):
    userdata = args[0]
    mid_var_t = args[1]
    mid_num_t = args[2]
    mid_notime_field = args[3]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                             [0, max(mid_num_t)],
                             y0=x0[4:6],
                             t_eval=mid_num_t,
                             args=[x0[0:4]])
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0:mid_notime_field[0]+"_hat",1:mid_notime_field[1]+"_hat"},inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata,mid_df_res,on="time")
    # estimating residual in loss function
    guess_xy = [x0[6], x0[7]]
    if x0[6] == 0:
        guess_xy[0] = 0.01
    if x0[7] == 0:
        guess_xy[1] = 0.01
    i_num = 0
    res_sum = []
    for i in mid_notime_field:
        log_e = np.log(guess_xy[i_num] ** 2)
        inverse_e = 1 / (guess_xy[i_num] ** 2)
        res_df[i+"_err"] = log_e + ((res_df[i] - res_df[i+"_hat"]) **2) * inverse_e
        i_num = i_num + 1
        res_sum.append(res_df[i+"_err"].sum())
    return np.sum(res_sum)

def calcRand_MultiBiFirst_func(x0, args):
    userdata = args[0]
    mid_num_t = args[2]
    mid_notime_field = args[3]
    subject_guess = args[5]
    false_indices = [index for index, value in enumerate(subject_guess) if value is False]
    for index in false_indices:
        x0[index] = 0

    fixed_parms = args[6]
    mid_y0 = x0[4:6] + fixed_parms[4:6]
    mid_args = [x0[0:4] + fixed_parms[0:4]]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                             [0, max(mid_num_t)],
                             y0=mid_y0,
                             t_eval=mid_num_t,
                             args=mid_args)
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"}, inplace=True)
    if f'{mid_notime_field[1]}_hat' not in mid_df_res.columns.tolist(): #fix bug
        mid_df_res[f'{mid_notime_field[1]}_hat'] = 0
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    res_df.fillna(0,inplace=True)

    # estimating residual in loss function
    guess_xy = [x0[6], x0[7]]
    if x0[6] == 0:
        guess_xy[0] = 0.01
    if x0[7] == 0:
        guess_xy[1] = 0.01
    i_num = 0
    res_sum = []
    for i in mid_notime_field:
        res_df.loc[res_df[i + "_hat"] > 1e+50,i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        log_e = np.log(guess_xy[i_num] ** 2)
        inverse_e = 1 / (guess_xy[i_num] ** 2)
        res_df[i+"_err"] = log_e + ((res_df[i] - res_df[i+"_hat"]) **2) * inverse_e
        # res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)

def solve_MultiBiFirst_func(t, y0, args):
    mid_args_list = list(args)
    dxdt = mid_args_list[0] * y0[0] + mid_args_list[1] * y0[1]
    dydt = mid_args_list[2] * y0[0] + mid_args_list[3] * y0[1]
    return [dxdt, dydt]

############################
    # Bayesian optimization
    # --------------------------
def calcBayes_MultiBiFirst_func(userdata,var_model,
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
    args = {"mid_notime_field":mid_notime_field,
            "subject_model":subject_model}
    calcFix_data = opt_Bayes(userdata,
                             space,
                             n_seed,
                             n_total,
                             gamma,
                             fmin_rmse = fmin_rmse,
                             args=args)
    print('calcFix_data',calcFix_data)
    bayesFix_data = calcFix_data[calcFix_data['rmse'] == calcFix_data['rmse'].min()]
    print('bayesFix_data',bayesFix_data)

    randEffect_data = pd.DataFrame({"Subject": [],
                                    "EtaI_1": [],
                                    "EtaI_2": [],
                                    "EtaI_3": [],
                                    "EtaI_4": [],
                                    "EtaI_x": [],
                                    "EtaI_y": [],
                                    "RMSE": []})

    # subject_guess
    # --------------------------
    fixed = [0,0,0,0,0,0]
    if not re.search('1', fix_model[0]):
        fixed[5] = False
    if not re.search('1', fix_model[1]):
        fixed[6] = False
    if not re.search(mid_notime_field[0], fix_model[0]):
        fixed[0] = False
    if not re.search(mid_notime_field[1], fix_model[0]):
        fixed[1] = False
    if not re.search(mid_notime_field[0], fix_model[1]):
        fixed[2] = False
    if not re.search(mid_notime_field[1], fix_model[1]):
        fixed[3] = False
    args_rand = {"mid_notime_field": mid_notime_field,
                "subject_model": subject_model,
                 "fixed":fixed,
                 "bayesFix_data":bayesFix_data}
    space_rand = {'beta1': bayes_obj(-3, 3),
             'beta2': bayes_obj(-3, 3),
             'beta3': bayes_obj(-3, 3),
             'beta4': bayes_obj(-3, 3),
             'init_x': bayes_obj(-20, 20),
             'init_y': bayes_obj(-20, 20), }
    n_seed_rand = 30
    n_total_rand = 2000
    gamma_rand = 0.8

    for index, i_subject in enumerate(userdata[subject_model].unique().tolist()):
        print(f'Estimating random effects {i_subject}')
        mid_userdata = userdata.loc[userdata[subject_model] == i_subject]
        mid_calcRandom_data = opt_Bayes(mid_userdata,
                                     space_rand,
                                     n_seed_rand,
                                     n_total_rand,
                                     gamma_rand,
                                     fmin_rmse = fmin_rmse_rand,
                                     args=args_rand)
        bayesRand_data = mid_calcRandom_data[mid_calcRandom_data['rmse'] == mid_calcRandom_data['rmse'].min()]
        print(bayesRand_data)
        new_row = [i_subject]
        new_row.extend(bayesRand_data.iloc[0,:].values)
        print(bayesRand_data.iloc[0,:].values)
        new_row_df = pd.DataFrame([new_row], columns=randEffect_data.columns)
        randEffect_data = pd.concat([randEffect_data, new_row_df], ignore_index=True)
        print(f"Estimating Random effects: \n {randEffect_data}")

    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                 "time": [],
                                 mid_notime_field[0] + "_hat": [],
                                 mid_notime_field[1] + "_hat": []
                                 })
    bayesFix_best_data = bayesFix_data.iloc[0, :].values
    times = mid_num_t
    for index, i_subject in enumerate(userdata[subject_model].unique().tolist()):
        randEffect_parms = randEffect_data.loc[randEffect_data['Subject'] == i_subject, :]
        mid_predict_y0 = [bayesFix_best_data[4] + randEffect_parms.loc[index, 'EtaI_x'],
                          bayesFix_best_data[5] + randEffect_parms.loc[index, 'EtaI_y']]

        mid_predict_parms = [bayesFix_best_data[0] + randEffect_parms.loc[index, 'EtaI_1'],
                             bayesFix_best_data[1] + randEffect_parms.loc[index, 'EtaI_2'],
                             bayesFix_best_data[2] + randEffect_parms.loc[index, 'EtaI_3'],
                             bayesFix_best_data[3] + randEffect_parms.loc[index, 'EtaI_4']]
        mid_predict_data = solve_ivp(solve_MultiBiFirst_func,
                                     [0, max(mid_num_t)],
                                     y0=mid_predict_y0,
                                     t_eval=mid_num_t,
                                     args=[mid_predict_parms])
        mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
        mid_predictDF_data.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"},
                                  inplace=True)
        mid_predictDF_data['time'] = np.array(mid_num_t)
        mid_predictDF_data['Subject'] = i_subject
        predict_data = pd.concat([predict_data, mid_predictDF_data], axis=0)
    res_dict = {"fixed_effects": calcFix_data,
                "random_effects": randEffect_data,
                "predict_data": predict_data}
    return res_dict
def fmin_rmse(userdata,parms,args):
    times = userdata.loc[:, 'time'].sort_values(ascending=True).unique().tolist()
    mid_y0 = [parms[4],parms[5]]
    mid_args = [parms[0],parms[1],parms[2],parms[3]]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                          [0, 1000],
                          y0=mid_y0,
                          args=[mid_args],
                          t_eval=times
                          )
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: args["mid_notime_field"][0] + "_hat", 1: args["mid_notime_field"][1] + "_hat"}, inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    res_df.fillna(0, inplace=True)
    res_sum = []
    for i in args["mid_notime_field"]:
        res_df.loc[res_df[i + "_hat"] > 1e+50, i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)

def fmin_rmse_rand(userdata,parms,args):
    fixed= args["fixed"]
    bayesFix_data = args["bayesFix_data"]
    bayesFix_data = bayesFix_data.iloc[0,:].values

    false_indices = [index for index, value in enumerate(fixed) if value is False]
    for index in false_indices:
        parms[index] = 0
        fixed[index] = 0

    times = userdata.loc[:, 'time'].sort_values(ascending=True).unique().tolist()
    mid_y0 = [parms[4] + bayesFix_data[4],
              parms[5] + bayesFix_data[5]]
    mid_args = [parms[0] + bayesFix_data[0],
                parms[1] + bayesFix_data[1],
                parms[2] + bayesFix_data[2],
                parms[3] + bayesFix_data[3]]
    mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                          [0, 1000],
                          y0=mid_y0,
                          args=[mid_args],
                          t_eval=times
                          )
    mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
    mid_df_res.rename(columns={0: args["mid_notime_field"][0] + "_hat", 1: args["mid_notime_field"][1] + "_hat"}, inplace=True)
    mid_df_res['time'] = np.array(mid_min_data.t)

    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    res_df.fillna(0, inplace=True)
    res_sum = []
    for i in args["mid_notime_field"]:
        res_df.loc[res_df[i + "_hat"] > 1e+50, i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)
##############################
#
# --------------------------
def calc_MultiBiFirst_United_func(userdata,var_model,guess,method,subject_model, modelDF):
    ## identify variables and information
    ## fixed effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    mid_num_t = [x for x in mid_num_t if not math.isnan(x)]
    fix_model = modelDF.loc[modelDF['operator'] == '~', 'fixRand'].tolist()
    # mid_userdata = userdata.loc[:,var_model.loc[:,'variable'].tolist()]
    # rename_key = {k: v for k, v in zip(var_model.loc[:,'variable'].tolist(), var_model.loc[:,'field'].tolist())}
    # mid_userdata.rename(columns=rename_key,inplace=True)
    # mid_userdata["subject"] = userdata.loc[:,subject_model]
    fix_rand_guess = guess[0]
    fix_rand_guess += [0] * len(userdata['Subject'].unique()) * 6
    fix_rand_guess += [0.1] * len(userdata['Subject'].unique()) * 2 # [1,1] estimating residual in loss function
    args = [userdata, mid_var_t, mid_num_t, mid_notime_field]
    calcFixRand_data = minimize(calcFixRand_MultiBiFirst_United_func,
                            x0=fix_rand_guess,
                            method=method[0],
                            tol=1e-8,
                            options={'disp': False},
                            args=args)
    Neg2LL = calcFixRand_data.fun + 3.67
    res_fixed = calcFixRand_data.x.tolist()
    fixed_coef = res_fixed[0:4]
    fixed_init = res_fixed[4:6]
    rand_coefinit = res_fixed[6:]
    fixedrandEffect_data = pd.DataFrame()
    for idx,key in enumerate(userdata['Subject'].unique()):
        mid_idx =  idx * 6
        mid_randEffect_data = pd.DataFrame({'Subject':[key],
                                            'rand_beta1':[rand_coefinit[idx + 0]],
                                            'rand_beta2':[rand_coefinit[idx + 1]],
                                            'rand_beta3':[rand_coefinit[idx + 2]],
                                            'rand_beta4':[rand_coefinit[idx + 3]],
                                            'rand_init1':[rand_coefinit[idx + 4]],
                                            'rand_init2':[rand_coefinit[idx + 5]],
                                            })
        fixedrandEffect_data = pd.concat([fixedrandEffect_data,mid_randEffect_data])
    fixedrandEffect_data['fixed_beta1'] = fixed_coef[0]
    fixedrandEffect_data['fixed_beta2'] = fixed_coef[1]
    fixedrandEffect_data['fixed_beta3'] = fixed_coef[2]
    fixedrandEffect_data['fixed_beta4'] = fixed_coef[3]
    fixedrandEffect_data['fixed_init1'] = fixed_init[0]
    fixedrandEffect_data['fixed_init2'] = fixed_init[1]
    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                 "time": [],
                                 mid_notime_field[0] + "_hat": [],
                                 mid_notime_field[1] + "_hat": []
                                 })
    times = mid_num_t
    uni_subject_list = userdata['Subject'].unique()
    for index, i_subject in enumerate(uni_subject_list):
        randEffect_parms = fixedrandEffect_data.loc[fixedrandEffect_data['Subject'] == i_subject, :]
        mid_predict_y0 = [randEffect_parms['fixed_init1'].values[0] + randEffect_parms['rand_init1'].values[0],
                          randEffect_parms['fixed_init2'].values[0] + randEffect_parms['rand_init2'].values[0],
                          ]
        mid_predict_parms = [randEffect_parms['fixed_beta1'].values[0] + randEffect_parms['rand_beta1'].values[0],
                             randEffect_parms['fixed_beta2'].values[0] + randEffect_parms['rand_beta2'].values[0],
                             randEffect_parms['fixed_beta3'].values[0] + randEffect_parms['rand_beta3'].values[0],
                             randEffect_parms['fixed_beta4'].values[0] + randEffect_parms['rand_beta4'].values[0],]
        mid_predict_data = solve_ivp(solve_MultiBiFirst_func,
                                     [0, max(mid_num_t)],
                                     y0=mid_predict_y0,
                                     t_eval=mid_num_t,
                                     args=[mid_predict_parms])
        mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
        mid_predictDF_data.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"},
                                  inplace=True)
        mid_predictDF_data['time'] = np.array(mid_num_t)
        mid_predictDF_data['Subject'] = i_subject
        predict_data = pd.concat([predict_data, mid_predictDF_data], axis=0)
    res_dict = {"fixed_effects": fixedrandEffect_data[['Subject','fixed_beta1','fixed_beta2','fixed_beta3','fixed_beta4','fixed_init1','fixed_init2']],
                "random_effects": fixedrandEffect_data[['Subject','rand_beta1','rand_beta2','rand_beta3','rand_beta4','rand_init1','rand_init2']],
                "predict_data": predict_data,
                "Neg2LL":Neg2LL}
    return res_dict
def calcFixRand_MultiBiFirst_United_func(x0, args):
    userdata = args[0]
    mid_var_t = args[1]
    mid_num_t = args[2]
    mid_notime_field = args[3]
    mid_fixed_coef = x0[0:4]
    mid_fixed_inital = x0[4:6]
    mid_all_rand = x0[6:]
    mid_fixed_rand_df = pd.DataFrame()
    num_unique = len(userdata['Subject'].unique())
    num_unique_start = 6 + num_unique * 6
    e_guess = x0[num_unique_start:]
    e_guess_two = 0
    for idx, key in enumerate(userdata['Subject'].unique()):
        mid_idx = idx * 6
        mid_i_key = pd.DataFrame({'rand_beta1':[mid_all_rand[mid_idx + 0]],
                                  'rand_beta2':[mid_all_rand[mid_idx + 1]],
                                  'rand_beta3':[mid_all_rand[mid_idx + 2]],
                                  'rand_beta4':[mid_all_rand[mid_idx + 3]],
                                  'rand_init1':[mid_all_rand[mid_idx + 4]],
                                  'rand_init2':[mid_all_rand[mid_idx + 5]],
                                  })
        mid_fixed_rand_df = pd.concat([mid_fixed_rand_df,mid_i_key])
    mid_fixed_rand_df['fixed_beta1'] = mid_fixed_coef[0]
    mid_fixed_rand_df['fixed_beta2'] = mid_fixed_coef[1]
    mid_fixed_rand_df['fixed_beta3'] = mid_fixed_coef[2]
    mid_fixed_rand_df['fixed_beta4'] = mid_fixed_coef[3]
    mid_fixed_rand_df['fixed_init1'] = mid_fixed_inital[0]
    mid_fixed_rand_df['fixed_init2'] = mid_fixed_inital[1]
    mid_fixed_rand_df['fixed_rand_beta1'] = mid_fixed_rand_df['fixed_beta1'] + mid_fixed_rand_df['rand_beta1']
    mid_fixed_rand_df['fixed_rand_beta2'] = mid_fixed_rand_df['fixed_beta2'] + mid_fixed_rand_df['rand_beta2']
    mid_fixed_rand_df['fixed_rand_beta3'] = mid_fixed_rand_df['fixed_beta3'] + mid_fixed_rand_df['rand_beta3']
    mid_fixed_rand_df['fixed_rand_beta4'] = mid_fixed_rand_df['fixed_beta4'] + mid_fixed_rand_df['rand_beta4']
    mid_fixed_rand_df['fixed_rand_init1'] = mid_fixed_rand_df['fixed_init1'] + mid_fixed_rand_df['rand_init1']
    mid_fixed_rand_df['fixed_rand_init2'] = mid_fixed_rand_df['fixed_init2'] + mid_fixed_rand_df['rand_init2']
    end_sum = []
    for idx, key in enumerate(userdata['Subject'].unique()):
        mid_min_data = solve_ivp(solve_MultiBiFirst_func,
                                 [0, max(mid_num_t)],
                                 y0=[mid_fixed_rand_df['fixed_rand_init1'].values[idx],
                                     mid_fixed_rand_df['fixed_rand_init2'].values[idx]],
                                 t_eval=mid_num_t,
                                 args=[[mid_fixed_rand_df['fixed_rand_beta1'].values[idx],
                                       mid_fixed_rand_df['fixed_rand_beta2'].values[idx],
                                       mid_fixed_rand_df['fixed_rand_beta3'].values[idx],
                                       mid_fixed_rand_df['fixed_rand_beta4'].values[idx]]])
        mid_df_res = pd.DataFrame(np.array(mid_min_data.y).T)
        mid_df_res.rename(columns={0: mid_notime_field[0] + "_hat", 1: mid_notime_field[1] + "_hat"}, inplace=True)
        mid_df_res['time'] = np.array(mid_min_data.t)
        mid_userdata = userdata[userdata['Subject'] == key].copy()
        mid_res_df = pd.merge(mid_userdata, mid_df_res, on="time",how='left')
        # estimating residual in loss function
        guess_xy = [e_guess[e_guess_two],e_guess[e_guess_two + 1]]
        if guess_xy[0] == 0:
            guess_xy[0] = 0.01
        if guess_xy[1] == 0:
            guess_xy[1] = 0.01
        res_sum = []
        i_num = 0
        for i_field in mid_notime_field:
            log_e = np.log(guess_xy[i_num] ** 2)
            inverse_e = 1 / (guess_xy[i_num] ** 2)
            try: # The solve_ivp without all values
                mid_res_df[i_field + "_err"] = log_e + ((mid_res_df[i_field] - mid_res_df[i_field + "_hat"]) ** 2) * inverse_e
                # mid_res_df[i_field + "_err"] = (mid_res_df[i_field] - mid_res_df[i_field + "_hat"]) ** 2
                res_sum.append(mid_res_df[i_field + "_err"].sum())
            except:
                mid_res_df['_err'] = mid_res_df[i_field] * mid_res_df[i_field]
                res_sum.append(mid_res_df['_err'].sum())
            i_num = i_num + 1
        e_guess_two = e_guess_two + 2
        end_sum.append(res_sum)
    sum_out = np.sum(end_sum)
    return sum_out
