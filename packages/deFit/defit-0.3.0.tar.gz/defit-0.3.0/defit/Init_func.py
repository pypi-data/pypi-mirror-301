import warnings

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None
import re

class opt_BO:
    def __init__(self, min_, max_):
        self.min = min_
        self.max = max_
    def sample(self, n_samples):
        return np.random.uniform(self.min, self.max, n_samples)

def Init_func(userdata,model,guess,method,plot):
    ############################
    # Model
    # --------------------------
    ## Judgement Model
    if model == None:
        warnings.warn('Model can not be None.',category='1')
        model = '''
            x =~ x
            y =~ y
            time =~ time
            x(1) ~ x + y
            y(1) ~ y + x
        '''
    # Model standardization
    # The model syntax: delete the useless \t\r\n and split field the by \n
    model_str = model
    model = model.split('\n')
    modelDF = pd.DataFrame()
    for i in range(len(model)):
        mid_row = model[i]
        mid_row = mid_row.replace(" ","")
        if '=~' in mid_row:
            modelDF.loc[i,'field'] = mid_row.split('=~')[0].strip()
            modelDF.loc[i,'order'] = None
            modelDF.loc[i,'operator'] = '=~'
            modelDF.loc[i,'variable'] = mid_row.split('=~')[1].strip()
            modelDF.loc[i, 'fixRand'] = None
            modelDF.loc[i, 'subject'] = None
        elif '~' in mid_row:
            modelDF.loc[i, 'field'] = mid_row.split('~')[0].strip()
            mid_order = mid_row.split('~')[0].strip()
            mid_order = mid_order.split(')')[0].strip()
            mid_order = mid_order.split('(')[1].strip()
            mid_variable = mid_row.split('~')[1].strip()
            if '|' in mid_variable:
                multi_model = True
                mid_fixRand = mid_variable.split('+(')[1].split('|')[0]
                mid_subject = mid_variable.split('+(')[1].split('|')[1]
                mid_subject = mid_subject.replace(")","")
            else:
                mid_fixRand = None
                mid_subject = None
            modelDF.loc[i, 'order'] = mid_order
            modelDF.loc[i, 'operator'] = '~'
            modelDF.loc[i, 'variable'] = mid_variable.split('+(')[0]
            modelDF.loc[i, 'fixRand'] = mid_fixRand
            modelDF.loc[i, 'subject'] = mid_subject
    modelDF['order'] = modelDF['order'].fillna(0)
    modelDF['order'] = modelDF['order'].astype(int)
    # Model information
    var_model = modelDF.loc[modelDF['operator'] == '=~']
    var_notime_model = var_model.loc[var_model['field'] != 'time']
    var_data = var_model.loc[:,'variable'].tolist()
    var_notime_data = var_notime_model.loc[:,'variable'].tolist()
    multi_model = modelDF['fixRand'].notna().any()
    field_model = var_notime_model.loc[:,'field'].tolist()
    order_model = modelDF['order'].max()
    subject_model = modelDF.loc[modelDF['operator'] == '~','subject'].tolist()

    ############################
    # userdata
    # --------------------------
    ## Judgement userdata
    colname_data = userdata.columns.tolist()
    if not all(elem in colname_data for elem in var_data):
        warnings.warn("Model variable must be included in your data.\n")
        raise Exception("Stopping")
    ## Judgement time
    # must be contain time variable
    mid_field = modelDF.loc[modelDF['operator'] == '=~', 'field'].tolist()
    if not 'time' in mid_field:
        warnings.warn("Model must contain 'time'")
        raise Exception("Stopping")

    ############################
    # guess
    # --------------------------
    ## guess values can be a list or a string. When it is a list, the model must be multilevel model.
    ## the guess values now is support string, list(multilevel), dict(bayesian).
    if guess is None:
        # if guess values is None, Then, we need to give guess values based on the model.
        if multi_model:
            # multi_model is True
            if len(field_model) == 2:
                # multilevel bivariate
                if order_model == 1:
                    # first-order
                    guess = [[0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006],
                             [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]]
            elif len(field_model) == 1:
                # multilevel univariate
                if order_model == 2:
                    # second-order
                    guess = [[0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006],
                             [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]]
        elif len(field_model) == 1:
            if order_model == 2:
                # second-order
                # univariate second-order
                guess = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]
        else:
            # multi_model is False.
            if len(field_model) == 2:
                # bivariate
                if order_model == 1:
                    # first-order
                    guess = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
                    # guess2 = None
            else:
                # univariate second-order
                guess = [0.01, 0.01, userdata[1][var_notime_model[0]], 0.01]
    else:
        if not isinstance(guess, list):
            if multi_model:
                # if is multilevel the guess must contain two steps
                guess = [guess, guess]
            guess = [guess]
    # if method == bayesian
    # --------------------------
    # obj_BO = opt_BO("deFit")
    if method == 'bayesian':
        if guess == None:
            space = {'beta1':opt_BO(-10,10),
                'beta2':opt_BO(-10,10),
               'beta3':opt_BO(-10,10),
               'beta4':opt_BO(-10,10),
               'init_x':opt_BO(-100,100),
               'init_y':opt_BO(-100,100),}
        else:
            guess = guess

    ############################
    # method
    # --------------------------
    if method is None:
        if multi_model:
            if len(field_model) == 2:
                if order_model == 1:
                    method = ['L-BFGS-B', 'L-BFGS-B']
            elif len(field_model) == 1:
                if order_model == 2:
                    method = ['L-BFGS-B', 'L-BFGS-B']
        else:
            if len(field_model) == 2:
                if order_model == 1:
                    method = ['L-BFGS-B']
            elif len(field_model) == 1:
                if order_model == 2:
                    method = ['L-BFGS-B']
    else:
        if not isinstance(method, list):
            if multi_model:
                method = [method, method]

    ############################
    # multilevel
    # --------------------------
    # multilevel
    if multi_model:
        # subject_model
        if len(list(set(subject_model))) == 1:
            subject_model = list(set(subject_model))[0]
        else:
            raise ValueError("ALL subject must be the same. Or there is no subject")

        name_subject = modelDF[modelDF['operator'] == '~']['subject']
        subject_row = userdata.loc[:,mid_subject].copy()
        userdata.loc[:, 'Subject'] = subject_row.copy()
        mid_time = var_model.loc[var_model['field'] == 'time'].values[0][3]
        time_row = userdata.loc[:,mid_time].copy()
        userdata.loc[:, 'time'] = time_row.copy()
        if not all(name in userdata.columns for name in set(name_subject)):
            raise ValueError("Subject must be contained in columns of your data.")
        # for index_X,key_X in enumerate(field_model):
        #     var_row = userdata.loc[:,var_notime_data[index_X]].copy()
        #     userdata[key_X] = var_row.copy()

    ############################
    # Model
    # --------------------------
    ## multi step or united

    res = {"userdata":userdata,
           "modelDF":modelDF,
           "field_model" : field_model,
           "multi_model" : multi_model,
           "order_model" : order_model,
           "var_model" : var_model,
           "guess" : guess,
           "method" : method,
           "subject_model" : subject_model,
           "bayesian_obj":opt_BO,
    }
    return res