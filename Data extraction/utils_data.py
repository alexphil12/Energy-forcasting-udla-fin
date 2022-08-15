# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:53:49 2022

@author: alexa
"""
import pandas as pd
import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import scipy
def extractl(X):
    H=list(X["Voltaje_(R)_[V]"])
    h1=pd.DataFrame(cp.deepcopy(X["Voltaje_(R)_[V]"]))
    N=len(H)
    ind=0;
    index_util=[]
    long_nan=[]
    long=[]
    for j in range(N):
        if pd.isna(H[j])==False and ind==0:
            index_util.append(j)
            ind=1;
        elif pd.isna(H[j])==True and ind==1:
            index_util.append(j-1)
            ind=0
    if len(index_util)%2==1:
            index_util.append(N-1)
    k=0
    for k in range(0,len(index_util)-1,2):
        long.append(abs(index_util[k]-index_util[k+1]))
    if (long==[]):
        l=[]
        l.append(np.nan)
        l.append(np.nan)
        long.append(0)
        return(l)
    else:
        rang_max=long.index(max(long))
        h1["index1"]=h1.index
        h2=h1.reset_index(drop=True,inplace=True)
        l=[]
        l.append(h1.iloc[index_util[rang_max*2],1])
        l.append(h1.iloc[index_util[rang_max*2+1],1])
        return(l)
def verif_dataframe_mois(L):
    H=[]
    verif=2
    data=[]
    for k in range(len(L)):
        H.append(list(L[k]["Voltaje_(R)_[V]"]))
    for k in range(len(H)):
        verif=2
        for i in range(len(H[k])):
            if pd.isna(H[k][i])==True and verif!=1:
                verif=0
            if pd.isna(H[k][i])==False and verif==0:
                verif=1
        data.append(verif)
        verif=2
    return(data)     
def trace_data(dates,dataframe,mesure):
    serie=dataframe.loc[dates[0]:dates[1],mesure]
    serie.plot(kind='line',visible=True)
    plt.show()
    return(1)
def trace_histo_longueur_donnee(X,nombre_intervalle,dates,mesure):
    H=list(X.loc[dates[0]:dates[1],mesure])
    h1=pd.DataFrame(cp.deepcopy(X[mesure]))
    N=len(H)
    ind=0;
    index_util=[]
    long_nan=[]
    long=[]
    is_nan=[]
    for j in range(N):
        is_nan.append(pd.isna(H[j]))
        if pd.isna(H[j])==False and ind==0:
            index_util.append(j)
            ind=1;
        elif pd.isna(H[j])==True and ind==1:
            index_util.append(j-1)
            ind=0
    index_util.append(N-1)
    long_nan.append(index_util[0])
    
    for j in range(N):
        if is_nan[j]==True:
            is_nan[j]=0
        else:
            is_nan[j]=1
    if(index_util==[]):
      long_nan.append()
    for j in range(0,len(index_util)-1,2):
        long.append(abs(index_util[j]-index_util[j+1]))
    for j in range(0,len(index_util)-2,2):
        long_nan.append(abs(index_util[j+1]-index_util[j+2]))
    fig=plt.figure(figsize=(10,10))
    plt.subplot(2,2,2)
    index_plot=list(h1.index)
    plt.plot(range(len(H)),H,c="green")
    plt.xlabel("sample")
    plt.ylabel(mesure)
    plt.title("display of"+" "+mesure)
    plt.subplot(2,2,1)   
    plt.hist(long, range = (0, max(long)), bins = np.linspace(0,max(long),nombre_intervalle), color = 'blue',edgecolor = 'black')
    plt.xlabel('length of the interval')
    plt.ylabel('occurency')
    plt.title("Histogram continues data")
    plt.subplot(2,2,3)
    plt.hist(long_nan, range = (0, max(long_nan)), bins = np.linspace(0,max(long_nan),nombre_intervalle), color = 'red',edgecolor = 'black')
    plt.xlabel('length of the NaN')
    plt.ylabel('occurency')
    plt.title("Histogram continues NaN")
    plt.subplot(2,2,4)
    index3=list(h1.index)
    h1=index3.index(dates[0])
    h2=index3.index(dates[1])
    plt.scatter(range(len(is_nan)),is_nan,c="blue",s=0.1)
    plt.xlabel("sample")
    plt.ylabel("nan ou non")
    plt.title("event map")
    fig.show()
def data_frame_5max(X,dates,mesure):
    H=list(X.loc[dates[0]:dates[1],mesure])
    h1=pd.DataFrame(cp.deepcopy(X[mesure]))
    N=len(H)
    ind=0;
    index_util=[]
    long_nan=[]
    long=[]
    is_nan=[]
    for j in range(N):
        is_nan.append(pd.isna(H[j]))
        if pd.isna(H[j])==False and ind==0:
            index_util.append(j)
            ind=1;
        elif pd.isna(H[j])==True and ind==1:
            index_util.append(j-1)
            ind=0
    index_util.append(N-1)
    long_nan.append(index_util[0])
    
    for j in range(N):
        if is_nan[j]==True:
            is_nan[j]=0
        else:
            is_nan[j]=1
    if(index_util==[]):
      long_nan.append()
    for j in range(0,len(index_util)-1,2):
        long.append(abs(index_util[j]-index_util[j+1]))
    for u in range(0,len(index_util)-2,2):
        long_nan.append(abs(index_util[u+1]-index_util[u+2]))
    del_fin=[]
    for j in range(len(long_nan)-2):
        if long_nan[j]<=5:
            long[j]=long[j]+long[j+1]
            del_fin.append(j+1)
    rang_max=long.index(max(long))
    h1["index1"]=h1.index
    h2=h1.reset_index(drop=True,inplace=True)
    l=[]
    l.append(h1.iloc[index_util[rang_max*2],1])
    l.append(h1.iloc[index_util[rang_max*2+1],1])
    return(l)
def polynome_de_laplace(X,Y,x):
    L_laplace=[1]*len(X)
    for i in range(len(X)):
        for j in range(len(X)):
            if j!=i:
                
                L_laplace[i]=L_laplace[i]*(x-X[j])/(X[i]-X[j])
    poly_inter=sum([x*y for x,y in zip(L_laplace,Y)])
    return(poly_inter)
def remplie_interpolation(df,N):
    new_df=cp.deepcopy(df)
    H=list(df.iloc[:,3])
    new_df["index2"]=df.index
    index_i3=list(new_df["index2"])
    del(new_df["index2"])
    X=list(range(N))
    inv=list(reversed(list(range(1,N+1))))
    for j in range(len(H)):
        if np.isnan(H[j])==True:
            for i in range(2,29):
                Y=[new_df.iloc[j-x,i] for x in inv]
                new_df.iloc[j,i]=polynome_de_laplace(X, Y, N)
            print(index_i3[j])
    return(new_df)
    
def remplie_interpolation_V2(df,N):
    new_df=cp.deepcopy(df)
    H=list(df.iloc[:,3])
    new_df["index2"]=df.index
    index_i3=list(new_df["index2"])
    del(new_df["index2"])
    X=list(range(N))
    inv=list(reversed(list(range(1,N+1))))
    j=0
    while j<len(H)-round(N/2)-1:
        if np.isnan(H[j])==True:
            u=cp.deepcopy(j)
            while (np.isnan(H[j]) and j !=len(H)-round(N/2)-1)==True:
                j+=1
            ecart=abs(u-j)
            X1=list(range(u-round(N/2),u))
            X2=list(range(u+ecart,u+ecart+round(N/2)))
            X=X1+X2
            for i in range(2,29):
                for k in range(u,j):
                    Y=[new_df.iloc[x,i] for x in X]
                    new_df.iloc[k,i]=polynome_de_laplace(X, Y, k)
            print(index_i3[j])
        j+=1
        if(j==len(H)):
            break
    return(new_df)        
    
def data_frame_5max_V2(X,dates,mesure):
    H=list(X.loc[dates[0]:dates[1],mesure])
    h1=pd.DataFrame(cp.deepcopy(X[mesure]))
    N=len(H)
    ind=0;
    index_util=[]
    long_nan=[]
    long=[]
    is_nan=[]
    compteur=0
    for j in range(N):
        is_nan.append(pd.isna(H[j]))
        if pd.isna(H[j])==False and ind==0:
            index_util.append(j)
            ind=1;
        elif pd.isna(H[j])==True and ind==1 and compteur<5:
            compteur+=1
        elif pd.isna(H[j])==False and ind==1 and compteur>0:
            compteur=0
        elif pd.isna(H[j])==True and ind==1 and compteur==5:
            index_util.append(j-1)
            ind=0
    if len(index_util)%2==1:
            index_util.append(N-1)
    k=0
    for k in range(0,len(index_util)-1,2):
        long.append(abs(index_util[k]-index_util[k+1]))
    if (long==[]):
        l=[]
        l.append(np.nan)
        l.append(np.nan)
        long.append(0)
        return(l)
    else:
        rang_max=long.index(max(long))
        h1["index1"]=h1.index
        h2=h1.reset_index(drop=True,inplace=True)
        l=[]
        l.append(h1.iloc[index_util[rang_max*2],1])
        l.append(h1.iloc[index_util[rang_max*2+1],1])
        return(l)
    
    
    
    
    
    
    
    