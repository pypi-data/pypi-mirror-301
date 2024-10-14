from scipy.integrate import solve_ivp
import numpy as np
from scipy.optimize import minimize
import pandas as pd

def Solver_UniSecond_func(init_dict):
    ## messages
    print('Program will fit the data with a univariate second-order differential equation.')
    print('The differential equations are:')
    print('x(2) = beta1 * x + beta2 * x(1)')
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

    if method[0] == "bayesian":
        print('Bayesian Not supported')
    else:
        calc_data = calc_UniSecond_func(userdata, var_model, guess, method, subject_model, modelDF)
        predict_data = calc_data['predict_data']
        beta1 = calc_data['fixed_effects'].x[0]
        beta2 = calc_data['fixed_effects'].x[1]
        beta3 = calc_data['fixed_effects'].x[2]
        beta4 = calc_data['fixed_effects'].x[3]
        init_x = calc_data['fixed_effects'].x[4]
        init_y = calc_data['fixed_effects'].x[5]

        ## equation
    equation1 = f"{mid_notime_field[0]}(2) = {beta1} * {mid_notime_field[0]} + {beta2} * {mid_notime_field[0]} \n"
    equation2 = f"Init t0_{mid_notime_field[0]}:{init_x} \n"
    ## table
    table = pd.DataFrame({"parameter": [f"{mid_notime_field[0]}(0) to {mid_notime_field[0]}(2)",
                                        f"{mid_notime_field[0]}(1) to {mid_notime_field[0]}(2)"],
                          "value": [beta1,
                                    beta2]})
    res_dict = {"solve_data": calc_data['fixed_effects'],
                "userdata": userdata,
                "predict_data": predict_data,
                "table": table,
                "equation": [equation1, equation2],
                "random_effects": None}
    return res_dict

def calc_UniSecond_func(userdata,var_model,guess,method,subject_model, modelDF):
    ## fix effect
    mid_var_t = var_model.loc[var_model['field'] == 'time', 'variable'].values[0]
    mid_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    mid_num_t = userdata[mid_var_t].sort_values(ascending=True).unique().tolist()
    fix_model = modelDF.loc[modelDF['operator'] == '~', 'fixRand'].tolist()

    args = [userdata, mid_var_t, mid_num_t, mid_notime_field]
    calcFix_data = minimize(min_UniSecond_func,
                            x0=guess,
                            method=method[0],
                            tol=1e-8,
                            options={'disp': False},
                            args=args)
    # --------------------------
    ## predict data
    predict_data = pd.DataFrame({"Subject": [],
                                 "time": [],
                                 mid_notime_field[0] + "_hat": []
                                 })
    mid_predict_data = solve_ivp(solve_UniSecond_func,
                                 [0, max(mid_num_t)],
                                 y0=calcFix_data.x[4:6],
                                 t_eval=mid_num_t,
                                 args=[calcFix_data.x[0:4]])
    mid_predictDF_data = pd.DataFrame(np.array(mid_predict_data.y).T)
    mid_predictDF_data.rename(columns={0: mid_notime_field[0] + "_hat"}, inplace=True)
    mid_predictDF_data['time'] = np.array(mid_num_t)
    mid_predictDF_data['Subject'] = None
    predict_data = pd.concat([predict_data, mid_predictDF_data], axis=0)
    res_dict = {"fixed_effects": calcFix_data,
                "predict_data": predict_data}
    return res_dict

def min_UniSecond_func(x0, args):
    userdata = args[0]
    times = args[2]
    mid_notime_field = args[3]
    mid_solve_data = solve_ivp(solve_UniSecond_func,
                             [0, max(times)],
                             y0=x0[4:6],
                             t_eval=times,
                             args=[x0[0:4]])
    mid_df_res = pd.DataFrame(np.array(mid_solve_data.y).T)
    mid_df_res.rename(columns={0: mid_notime_field[0] + "_hat"}, inplace=True)
    mid_df_res['time'] = np.array(mid_solve_data.t)
    res_df = pd.merge(userdata, mid_df_res, on="time",how="outer")
    # fill nan
    res_df.fillna(0,inplace=True)

    res_sum = []
    for i in mid_notime_field:
        # reset the data
        res_df.loc[res_df[i + "_hat"] > 1e+50,i + "_hat"] = 0
        res_df.loc[res_df[i + "_hat"] < -1e+50, i + "_hat"] = 0
        res_df = res_df.replace([np.inf, -np.inf], 0)
        # calcate the MSE
        res_df[i + "_err"] = (res_df[i] - res_df[i + "_hat"]) ** 2
        res_sum.append(res_df[i + "_err"].sum())
    return np.sum(res_sum)
def solve_UniSecond_func(t, y0, args):
    mid_args = args
    mid_args_list = list(mid_args)
    first = y0[1]
    second = mid_args_list[0] * y0[0] + mid_args_list[1] * y0[1]
    # os.system("pause")
    return [first, second]