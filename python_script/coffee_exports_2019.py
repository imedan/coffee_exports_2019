import pandas as pd
import numpy as np
from chord import Chord 

df=pd.read_csv('coffee_data_2019_top_5.csv')

top=['USA','Germany','Italy','Japan','Belgium']

totals={}
countries={}

for name in top:
    df_slice=df[(df['Partner']==name) & ~np.isnan(df['Qty'])].reset_index()
    totals[name]=[]
    countries[name]=[]
    for i in np.argsort(df_slice['Qty'])[::-1]:
        if df_slice.loc[i,'Qty']>17000000:
            totals[name].append(float(df_slice.loc[i,'Qty']))
            countries[name].append(str(df_slice.loc[i,'Reporter']))
        elif countries[name][-1]=='Other':
            totals[name][-1]=totals[name][-1]+float(df_slice.loc[i,'Qty'])
        else:
            totals[name].append(float(df_slice.loc[i,'Qty']))
            countries[name].append('Other')
            
all_countries=[]

for name in top:
    all_countries+=countries[name]
    
all_countries=sorted(np.unique(all_countries))

all_countries += [all_countries.pop(0)]

import_tots=np.zeros(len(all_countries))

for name,j in zip(top,range(len(top))):
    for i in range(len(all_countries)):
        idx=np.where(np.array(countries[name])==all_countries[i])[0]
        if len(idx)>0:
            import_tots[i]+=totals[name][idx[0]]/1000000.
            
idx=import_tots.argsort()[::-1]

all_countries=np.array(all_countries)[idx]
idx=np.where(all_countries=='Other')[0][0]
all_countries=list(all_countries)
all_countries += [all_countries.pop(idx)]

matrix=np.zeros((len(all_countries)+len(top),len(all_countries)+len(top)))

for name,j in zip(top,range(len(top))):
    for i in range(len(top),len(top)+len(all_countries)):
        if i>j:
            idx=np.where(np.array(countries[name])==all_countries[i-len(top)])[0]
            if len(idx)>0:
                matrix[j][i]=totals[name][idx[0]]*0.001*0.001
                matrix[i][j]=totals[name][idx[0]]*0.001*0.001
                
                
import_tots=np.zeros(len(all_countries))

for name,j in zip(top,range(len(top))):
    for i in range(len(all_countries)):
        idx=np.where(np.array(countries[name])==all_countries[i])[0]
        if len(idx)>0:
            import_tots[i]+=totals[name][idx[0]]*0.001*0.001
            

matrix[np.isnan(matrix)]=0.
matrix=np.round(matrix,4)


matrix = matrix.tolist()
Chord(matrix, list(top)+list(all_countries), wrap_labels=False,colors=['#49040E']*len(top)+['#179B15']*len(all_countries),margin=65).to_html()




