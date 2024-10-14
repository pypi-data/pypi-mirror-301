import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import multivariate_normal

def opt_Bayes(userdata,space,n_seed,n_total,gamma,fmin_rmse,args):
    trial = opt_sample_priors(userdata,space,n_seed,fmin_rmse,args)
    for i in range(n_seed,n_total):
        new_discard,new_good = opt_divide(trial,space,gamma,fmin_rmse)
        new_good_rmse = fmin_rmse(userdata,parms=new_good,args=args)
        print(new_good,new_good_rmse)
        new_coef = np.append(new_good,new_good_rmse)
        trial.loc[len(trial)] = new_coef
    return trial

def opt_sample_priors(userdata,space,n_seed,fmin_rmse,args):
    mid_sample = [space[hp].sample(n_seed) for hp in space]
    mid_seed = np.array(mid_sample)
    par_rmse = []
    for i_sample in range(len(mid_seed.T)):
        mid_parms = mid_seed.T[i_sample]
        mid_rmse = fmin_rmse(userdata,parms=mid_parms,args=args)
        par_rmse.append(mid_rmse)
    insrt_num = mid_seed.shape[0]
    mid_df = np.insert(mid_seed.T,insrt_num,par_rmse,axis=1)
    res_trials = pd.DataFrame(mid_df)
    # change the last name of trial's columns to "rmse"
    last_column = res_trials.columns[-1]
    res_trials.rename(columns={last_column: 'rmse'}, inplace=True)
    return res_trials

def opt_divide(trial,space,gamma,fmin_rmse):

    # get the value of gamma
    mid_cut = trial.loc[:,'rmse'].tolist()
    mid_sort = sorted(mid_cut)
    mid_n_gamma = int(len(mid_sort) ** gamma)
    mid_n_value = mid_sort[mid_n_gamma]

    # cut the dataframe
    mid_good = trial[trial['rmse'] <= mid_n_value]
    mid_discard = trial[trial['rmse'] > mid_n_value]
    mid_good_coef,mid_good_prob = opt_improvement(good = mid_good,discard = mid_discard,space = space,fmin_rmse=fmin_rmse)
    mid_discard_coef,mid_discard_prob = opt_improvement(good = mid_good,discard = mid_discard,space = space,fmin_rmse=fmin_rmse) # 暂时不用，后续尝试将其作为探索空间使用
    if(mid_good_prob > mid_discard_prob):
        next_coef = mid_good_coef
        next_discard = mid_discard_coef
    else:
        next_coef = mid_discard_coef
        next_discard = mid_good_coef
    return next_discard, next_coef

def opt_improvement(good,discard,space,fmin_rmse):
    good_min_rmse = np.argmin(good['rmse'].tolist())
    good_mean_rmse = np.mean(good['rmse'].tolist())
    discard_min_rmse = np.argmin(discard['rmse'].tolist())
    discard_mean_rmse = np.mean(discard['rmse'].tolist())

    good_coef_data = good.copy()
    del good_coef_data['rmse']
    discard_coef_data = discard.copy()
    del discard_coef_data['rmse']

    good_coef_matrix = good_coef_data.values ## convert to matrix
    good_coef_cov = np.cov(good_coef_matrix.T) ## get the covariance matrix of coefficients.
    good_coef_diag = np.diag(good_coef_cov)
    discard_coef_matrix = discard_coef_data.values  ## convert to matrix
    discard_coef_cov = np.cov(discard_coef_matrix.T)  ## get the covariance matrix of coefficients.
    discard_coef_diag = np.diag(discard_coef_cov)

    good_best = good.iloc[good_min_rmse, :]
    del good_best['rmse']
    good_mean_coef = good_coef_data.mean(axis=0)
    discard_best = discard.iloc[discard_min_rmse, :]
    del discard_best['rmse']
    discard_mean_coef = discard_coef_data.mean(axis=0)
    next_good = opt_prob(good_best,good_mean_coef,good_coef_cov,space=space,fmin_rmse=fmin_rmse)
    next_discard = opt_prob(discard_best,discard_mean_coef,discard_coef_cov,space=space,fmin_rmse=fmin_rmse)

    return next_good[0],next_good[1]

def opt_prob(best_guess,mean,cov,space,fmin_rmse):
    new_guess = np.random.multivariate_normal(mean, cov, size=10)
    guess_removed_1 = opt_checkMultivariate_normal(new_guess, space)
    remove_len = len(guess_removed_1[1])
    # The second guess cov*2
    second_guess = np.random.multivariate_normal(mean, cov*2.5, size=(1 + remove_len * 2))
    guess_removed_2 = opt_checkMultivariate_normal(second_guess, space)
    guess_revise = pd.concat([guess_removed_1[0], guess_removed_2[0]], axis=0)
    guess_revise = guess_revise.reset_index(drop=True)
    mid_prob = []
    mid_ei = []
    for i in range(0,guess_revise.shape[0]):
        guess_prob = multivariate_normal.pdf(guess_revise.values[i],
                                             mean.values,
                                             cov,
                                             allow_singular=True)
        # ei_rmse = fmin_rmse(guess_revise.values[i]) # y值
        ei_z = (guess_revise.values[i] - best_guess) / np.sqrt(np.diag(cov))
        # ei_z = ei_z * 1.5 + 1/ei_z
        ei_improvemnt = guess_revise.values[i] - best_guess
        ei = ei_improvemnt * norm.cdf(ei_z) + np.sqrt(np.diag(cov)) * norm.pdf(ei_z)
        ei_sum = np.sum(ei)
        # print('guess_prob',guess_prob,'ei_sum',ei_sum)
        mid_ei.append(ei_sum)
        mid_prob.append(guess_prob)
    mid_prob_max = np.argmax(mid_prob)
    mid_ei_max = np.argmax(ei_sum)
    res_coef = guess_revise.values[mid_ei_max]
    return res_coef,max(mid_prob)

def opt_checkMultivariate_normal(new_guess,space):
    space_dict = {}
    for param_name, param_values in space.items():
        space_dict[param_name] = [param_values.min, param_values.max]
    space_list = list(space_dict.values())
    del_list = np.array([])
    new_guessT = new_guess.T
    for i_space in range(len(new_guessT)):
        mid_col = np.array(new_guess.T[i_space])
        mid_min = space_list[i_space][0]
        mid_max = space_list[i_space][1]
        if (any(mid_col < mid_min)):
            false_list = list(mid_col < mid_min)
            false_list = np.where(false_list)
            del_list = np.append(del_list, false_list)
        if (any(mid_col > mid_max)):
            false_list = list(mid_col > mid_max)
            false_list = np.where(false_list)
            del_list = np.append(del_list, false_list)
    del_list = np.unique(del_list)
    del_list = [int(x) for x in del_list]
    mid_guess_df = pd.DataFrame(new_guess)
    mid_guess_df.drop(del_list,inplace=True)
    return mid_guess_df,del_list