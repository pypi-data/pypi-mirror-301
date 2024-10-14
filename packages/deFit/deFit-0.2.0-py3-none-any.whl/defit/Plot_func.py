import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
def Plot_func(userdata,predict,var_notime_field,var_model,field_model,order_model,multi_model,subject_model):
    if not multi_model:
        if len(field_model) == 2:
            combine_data = pd.merge(userdata, predict, on=['time'])
            outplot = plt.figure()
            color = ["red","green"]
            linestyle = ["dashed","solid"]
            for index,i_color in enumerate(var_notime_field):
                plt.plot(combine_data['time'], combine_data[var_notime_field[index]], color=color[index], linestyle="dashed")
                plt.plot(combine_data['time'], combine_data[var_notime_field[index] + "_hat"], color=color[index])
                plt.title(f'Plotting')
            plt.xlabel('time')
            plt.ylabel('values')
            plt.title('Bivariate First order differential equation')
            # plt.suptitle('Raw data (Dashed Lines)  & Predict values (Solid Lines)')
            plt.show()
        if len(field_model) == 1:
            combine_data = pd.merge(userdata, predict, on=['time'])
            outplot = plt.figure()
            var_notime_model = var_notime_field
            plt.plot(combine_data['time'], combine_data[var_notime_model[0]], color='red', linestyle='dashed')
            plt.plot(combine_data['time'], combine_data[var_notime_model[0] + "_hat"], color='red')
            plt.xlabel('time')
            plt.ylabel('values')
            plt.title('Univariate Second order differential equation')
            # plt.suptitle('Raw data (Dashed Lines)  & Predict values (Solid Lines)')
            plt.show()
    else:
        combine_data = pd.merge(userdata, predict, on=['Subject', 'time'])
        var_notime_model = var_notime_field
        if len(field_model) == 2:
            if order_model == 1:
                if multi_model:
                    outplot = plt.figure()
                    index_subject = 0
                    for subject, data in combine_data.groupby('Subject'):
                        plt.subplot(math.ceil(np.sqrt(len(combine_data['Subject'].unique()))), # ceil of sqrt subject
                                    math.ceil(np.sqrt(len(combine_data['Subject'].unique()))),
                                    index_subject+1)
                        plt.plot(data['time'], data[var_notime_model[0]], color='red', linestyle='dashed')
                        plt.plot(data['time'], data[var_notime_model[1]], color='green', linestyle='dashed')
                        plt.plot(data['time'], data[var_notime_model[0] + "_hat"], color='red')
                        plt.plot(data['time'], data[var_notime_model[1] + "_hat"], color='green')
                        plt.title(f'Subplot {subject}')
                        index_subject = index_subject +1
                    plt.xlabel('time')
                    plt.ylabel('values')
                    plt.title('Multilevel Bivariate first-order differential equation')
                    plt.suptitle(
                        'Raw data (Dashed Lines)  & Predict values (Solid Lines)\n' + var_notime_field[0] + '(Red) & ' +
                        var_notime_field[1] + '(Green)')
                    plt.show()
                else:
                    outplot = plt.figure()
                    for subject, data in combine_data.groupby('Subject'):
                        plt.plot(data['time'], data[var_notime_model[0]], color='red', linestyle='dashed')
                        plt.plot(data['time'], data[var_notime_model[1]], color='green', linestyle='dashed')
                        plt.plot(data['time'], data[var_notime_model[0] + "_hat"], color='red')
                        plt.plot(data['time'], data[var_notime_model[1] + "_hat"], color='green')
                    plt.xlabel('time')
                    plt.ylabel('values')
                    plt.title('Bivariate first-order differential equation')
                    plt.suptitle(
                        'Raw data (Dashed Lines)  & Predict values (Solid Lines)\n' + var_notime_field[0]+ '(Red) & ' +
                        var_notime_field[1] + '(Green)')
                    plt.show()
        elif len(field_model) == 1:
            if order_model == 2:
                if multi_model:
                    print('Plotting')
                    outplot = plt.figure()
                    index_subject = 0
                    for subject, data in combine_data.groupby('Subject'):
                        plt.subplot(math.ceil(np.sqrt(len(combine_data['Subject'].unique()))),  # ceil of sqrt subject
                                    math.ceil(np.sqrt(len(combine_data['Subject'].unique()))),
                                    index_subject + 1)
                        plt.plot(data['time'], data[var_notime_model[0]], color='blue', linestyle='dashed')
                        plt.plot(data['time'], data[var_notime_model[0] + "_hat"], color='blue')
                        plt.title(f'Subplot {subject}')
                        index_subject = index_subject + 1
                    plt.xlabel('time')
                    plt.ylabel('values')
                    plt.title('Multilevel Univariate Second order differential equation')
                    plt.suptitle('Raw Data (Dashed Lines)  & Predict Values (Solid Lines)\n' + var_notime_model[0])
                    plt.show()
                else:
                    outplot = plt.figure()
                    for subject, data in combine_data.groupby('Subject'):
                        plt.plot(data['time'], data[var_notime_model[0]], color='red', linestyle='dashed')
                        plt.plot(data['time'], data[var_notime_model[0] + "_hat"], color='red')
                    plt.xlabel('time')
                    plt.ylabel('values')
                    plt.title('Univariate Second order differential equation')
                    plt.suptitle('Raw data (Dashed Lines)  & Predict values (Solid Lines)\n' + var_model[0]['field'])
                    plt.show()
        else:
            raise ValueError("Something error. Contact us.")