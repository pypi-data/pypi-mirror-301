import numpy as np
import pandas as pd
import math

def calcDerivatives(data,column,groupby,order=2,time='',window=5):
    """
        Calculating the Derivatives
        :param data: a DataFrame.
        :param column: names of variables in the long format that correspond to multiple variables in the wide format.
        :param groupby: Character vector. Only used if the data is in a data.frame.
        :param time: A variable name in the data frame containing sampling time information.
        :param order: integer scalar.
        :param window: integer scalar. Must be an odd number
        :return:  a DataFrame.

        Examples
        --------
    #     >>> from defit import calcDerivatives
    #     >>> example4 = defit.get_data('example3')
    #     >>> derivatives_1 = calcDerivatives(data = example4,column='current',groupby='year',order=2)
    #     >>> derivatives_2 = calcDerivatives(data = example4,column=['current','expected'],groupby='year',order=2)
    #     >>> derivatives_3 = calcDerivatives(data = example4,column=['current','expected'],groupby='year',time='myTime',order=2)
    #     >>> result1 = defit.defit(data=df,model=model)

         See Also
        ----------
        https://github.com/yueqinhu/defit
        """
    deltaT = 1
    interval = 1
    res_df = pd.DataFrame()
    if type(column) is str:
        column = [column]
    for i_group in data[groupby].unique():
        mid_df = pd.DataFrame()
        mid_group = data[data[groupby] == i_group].copy()
        for i_col in column:
            mid_x = mid_group[i_col].tolist()
            tEmbedded = gllaEmbed(mid_x, embed=window, tau=interval)
            if len(mid_df) == 0:
                wMatrix = gllaWMatrix(embed=window, tau=interval, deltaT=deltaT, order=order)
                glla_Matrix = np.dot(tEmbedded.values,wMatrix)
                glla_name = [i_col + "_" + str(i) for i in range(1, order + 1)]
                glla_names = [i_col]
                glla_names.extend(glla_name)
                glla_df = pd.DataFrame(glla_Matrix,columns=glla_names)
                mid_df = pd.concat([mid_df,glla_df])
                mid_df.reset_index(drop=True,inplace=True)
                if time == '':
                    mid_start_time = (window+1)/2
                    mid_end_time = (len(mid_group) + 1 - (window-1)/2)
                    mid_df.insert(0, 'time', list(range(int(mid_start_time),int(mid_end_time))))
                else:
                    time_li = mid_group[time]
                    mid_start_time = (window+1)/2
                    mid_end_time = (len(mid_group) + 1 - (window-1)/2)
                    list_time = list(time_li)
                    mid_df.insert(0, 'time', list_time[int(mid_start_time - 1):int(mid_end_time -1)])
                mid_df.insert(0,'ID',i_group)
            else:
                wMatrix = gllaWMatrix(embed=window, tau=interval, deltaT=deltaT, order=order)
                glla_Matrix = np.dot(tEmbedded.values, wMatrix)
                glla_name = [i_col + "_" + str(i) for i in range(1, order + 1)]
                glla_names = [i_col]
                glla_names.extend(glla_name)
                glla_df = pd.DataFrame(glla_Matrix, columns=glla_names)
                mid_df = pd.concat([mid_df, glla_df],axis=1)
        res_df = pd.concat([res_df,mid_df])
    #######################
    # merge data
    if time=='':
        mid_data = pd.DataFrame()
        for i_group in data[groupby].unique():
            mid_i_group_df = data[data[groupby] == i_group]
            mid_data_df = pd.DataFrame({'ID':i_group,'time':list(range(1,len(mid_i_group_df)+1))})
            mid_data_df[column] = mid_i_group_df[column]
            mid_data = pd.concat([mid_data,mid_data_df])
        res_df = pd.merge(mid_data,res_df,left_on=['ID','time'],right_on=['ID','time'],how='left',suffixes=('','_0'))
    else:
        mid_data = data[[groupby] + [time]].copy()
        mid_data[column] = data[column]
        res_df = pd.merge(mid_data, res_df, left_on=([groupby] + [time]), right_on=['ID', 'time'], how='left',suffixes=('','_0'))
    return res_df

def gllaEmbed(x, embed=2, tau=1, groupby=np.nan, label="_", idColumn=True):
    mid_df = pd.DataFrame()
    mid_df['x'] = x
    for i in range(1,embed):
        mid_df[f'_{i}'] = mid_df['x'].shift(-i)
    mid_df.dropna(inplace=True)
    return mid_df

def gllaWMatrix(embed=5, tau=1, deltaT=1, order=2):
    L = np.tile(1,embed)
    L = L[:, np.newaxis]
    for i in range(1,order+1):
        mid_L = (((np.arange(1,embed + 1) - np.mean(np.arange(1,embed + 1))) * tau * deltaT) ** i) / math.factorial(i)
        mid_L = mid_L[:, np.newaxis]
        L = np.concatenate((L, mid_L), axis=1)

    L_inv = np.linalg.inv(np.dot(L.T, L))
    res = np.dot(L,L_inv)
    return res
