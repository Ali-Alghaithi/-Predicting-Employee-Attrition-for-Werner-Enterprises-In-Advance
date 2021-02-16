#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This file prepares the data for analysis.


# In[34]:


# import necessary libraries
import numpy as np
import pandas as pd


# In[35]:


# read in data
data = pd.read_csv("finalProjectSample.csv").drop(['Unnamed: 0'], axis=1)


# In[36]:


# convert termination_process_ts to datetime, then extract only the date (ignore the time)
data['FiredDate'] = pd.to_datetime(data.TERMINATION_PROCESS_TS, infer_datetime_format=True).dt.date
data = data.drop('TERMINATION_PROCESS_TS', axis = 1)


# In[37]:


# do the same for report_dt and hire_process_ts
data['ReportDate'] = pd.to_datetime(data.REPORT_DT, infer_datetime_format=True).dt.date
data = data.drop('REPORT_DT', axis = 1)
data['hiredDate'] = pd.to_datetime(data.HIRE_PROCESS_TS, infer_datetime_format=True).dt.date
data = data.drop('HIRE_PROCESS_TS', axis = 1)


# In[38]:


# generate a dummy determining if individual was fired today
# changed to inequality from equality, since reporting only occurs every 2 days
#     and some individuals quit on the day between reports
data['FiredToday'] = [int(data.FiredDate[x]<=data.ReportDate[x]) for x in range(len(data))]


# In[39]:


# process veteran_flg
data['Vet'] = [int(data.VETERAN_FLG[x]=='Y') for x in range(len(data))]
data = data.drop('VETERAN_FLG', axis = 1)


# In[40]:


# process tenure variable as timedelta type
data['daysWorked'] = (data.ReportDate - data.hiredDate).astype('timedelta64[D]')


# In[41]:


data['daysLeft'] = (data.FiredDate - data.ReportDate).astype('timedelta64[D]')


# In[42]:


data['quitIn30Days'] = np.where(data['daysLeft'] < 30, 1, 0)


# In[43]:


# process report date as datetime in order to extract day, month, and year info
data['ReportDate'] = data['ReportDate'] .astype('datetime64[ns]')
data['rDay'] = data.ReportDate.dt.dayofweek
data['rMonth'] = data.ReportDate.dt.month
data['rYear'] = data.ReportDate.dt.year


# In[45]:


# generate dummy variables based on available categorical variables
data = pd.concat([data, pd.get_dummies(data.Max_Students, prefix='hireType', drop_first = True)], axis=1)
data = pd.concat([data, pd.get_dummies(data.STATE_CD, prefix='state', drop_first = True)], axis=1)
data = pd.concat([data, pd.get_dummies(data.Driver_type, prefix='driver', drop_first = True)], axis=1)
data = pd.concat([data, pd.get_dummies(data.rDay, prefix='day', drop_first = True)], axis=1)
data = pd.concat([data, pd.get_dummies(data.rMonth, prefix='month', drop_first = True)], axis=1)
data = pd.concat([data, pd.get_dummies(data.rYear, prefix='year', drop_first = True)], axis=1)


# In[47]:


# Remove observations where daysLeft is negative
data = data[data.daysLeft >= 0]


# In[48]:


# Wrtie data to csv

#data.to_csv('finalData.csv')

