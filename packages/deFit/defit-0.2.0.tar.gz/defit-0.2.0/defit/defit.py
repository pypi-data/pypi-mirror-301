from .Solver_MultiBiFirst_func import Solver_MultiBiFirst_func
from .Solver_MultiUniSecond_func import Solver_MultiUniSecond_func
from .Solver_BiFirst_func import Solver_BiFirst_func
from .Solver_UniSecond_func import Solver_UniSecond_func
from .Init_func import Init_func
from .Scale_within import Scale_within
from .calcDerivatives import calcDerivatives
from .Info_func import Info_func
from .Plot_func import Plot_func
from pathlib import Path
import pandas as pd

def defit(data,model,guess=None,method=None,plot=False,fixed_first=True):
    """
        Fitting Differential Equations to Time Series Data
        :param data: a DataFrame containing all model variables. The "time" column must be included.
        :param model: a string specifying the model to be used. The "=~" operator is used to define variables, with the name of the variable user defined on the left and the name of the variable in the data on the right. The '~' operator specifies a differential equation, with the dependent variable on the left and the independent variables on the right. See also ‘Details’.
        :param guess: an optional vector that allows the user to give starting values for the model parameters, including the model coefficients and variable initial states.
        :param method: an optional string indicating which optimizer to use. The default method is subject to the specific model. The available options are 'Nelder-Mead','L-BFGS-B','SLSQP' and 'BFGS'.
        :param plot: True or False
        :param fixed_first: an optional True or False that True will estimate the multilevel model parameters using a two-step approach.
        :return:  the dict type
        dict[userdata | parameter | predict | r_squared | RMSE | SE | equation | table | convergence]

        Examples
        --------
    #     >>> import defit
    #     >>> import pandas as pd
    #     >>> df = defit.get_data('example1')
    #     >>> model = '''
    # ...             x =~ myX
    # ...             time =~ myTime
    # ...             x(2) ~ x + x(1)
    # ...         '''
    #     >>> result1 = defit.defit(data=df,model=model)

         See Also
        ----------
        https://github.com/yueqinhu/defit
        """
    init_dict = Init_func(userdata = data,model=model,guess=guess,method=method,plot=plot)
    if init_dict['multi_model']:
        if len(init_dict['field_model']) == 2:
            if init_dict['order_model'] == 1:
                init_dict['fixed_first'] = fixed_first
                out_solve = Solver_MultiBiFirst_func(init_dict)
            else:
                raise ValueError("Your model is not supported")
        elif len(init_dict['field_model']) == 1:
            if init_dict['order_model'] == 2:
                init_dict['fixed_first'] = fixed_first
                out_solve = Solver_MultiUniSecond_func(init_dict)
            else:
                raise ValueError("Your model is not supported")
        else:
            raise ValueError("**")
    else:
        if len(init_dict['field_model']) == 2:
            if init_dict['order_model'] == 1:
                out_solve = Solver_BiFirst_func(init_dict)
            else:
                raise ValueError("*")
        elif len(init_dict['field_model']) == 1:
            if init_dict['order_model'] == 2:
                out_solve = Solver_UniSecond_func(init_dict)
            else:
                raise ValueError("")
        else:
            raise ValueError("**")
    var_model = init_dict["var_model"]
    var_notime_field = var_model.loc[var_model['field'] != 'time', 'field'].values
    out_info = Info_func(userdata = out_solve['userdata'],
                       predict = out_solve['predict_data'],
                       var_notime_field = var_notime_field,
                       table = out_solve['table'],
                         field_model=init_dict['field_model'],
                         order_model=init_dict['order_model'],
                         multi_model=init_dict['multi_model'],
                             subject_model=init_dict['subject_model'])
    if plot:
        out_plot = Plot_func(userdata = out_solve["userdata"],
                         predict = out_solve['predict_data'],
                         var_notime_field=var_notime_field,
                         var_model= var_model,
                         field_model= init_dict['field_model'],
                         order_model=init_dict['order_model'],
                         multi_model=init_dict['multi_model'],
                             subject_model=init_dict['subject_model'])
    return out_solve

def get_data(filename):
    file_path = Path(__file__).resolve().parent
    mid_path = file_path / 'data' / f'{filename}.csv'
    df = pd.read_csv(mid_path)
    return df
# import pandas as pd
# example1 = pd.read_csv('data/example3.csv')
# model3 = '''
#    X =~ current
#    Y =~ expected
#    time =~ myTime
#    X(1) ~ X + Y + ( 1 + x + Y | year)
#    Y(1) ~ X + Y + ( x + Y | year)
#    '''
# example3_use = example1[(example1["year"] >= 1978) & (example1["year"] <= 2022)] # Note: select a subset of the data as an example.
# # from defit import Scale_within
# example3_c = Scale_within(example3_use, model3) # note: centering X variable by year
# result1 = defit(data = example3_c, model = model3,plot=True)