# -*- coding: utf-8 -*-
"Created on Fri May  6 14:43:28 2022"
"@author: alexa"


# import necessary libraries
import pandas as pd
import os
import glob
import numpy as np
import datetime
from utils_data import extractl,verif_dataframe_mois
import copy 
  
#creation of the dataframe df_P1 and df_P2, they contain NaN values for M1:M27
#date and hours values otherwise. They use the concatenation of date and hours
#as a litteral index
l_cov=[]
l_P1=[];
l_P2=[];
l_P0_cov=[];
l_ASC_cov=[];
l_P1_cov=[];
l_P2_cov=[];
l_P3_cov=[];
l_P4_cov=[];
l_P5_cov=[];
l_P6_cov=[];
l_S1_cov=[];
l_S2_cov=[];
l_S3_cov=[];
l_S4_cov=[];
l_S5_cov=[];
l_UPS1_cov=[];
l_UPS2_cov=[];
l_UPS3_cov=[];
l_CUB1_cov=[];
l_CUB2_cov=[];
l_CUB_cov=[];
l_bombas_cov=[];
l_data_center_cov=[];
mesure=["Fecha","Hora"];
  
start = datetime.datetime.strptime("22-07-2015", "%d-%m-%Y")
end = datetime.datetime.strptime("31-12-2021", "%d-%m-%Y")
dates = list(pd.date_range(start, end).strftime("%d-%m-%Y"))
N=len(dates)

index_fin=24*30*N;#number of mesure in the data set(1990 days between 22-07-2015 and 31-12-2020 24 hours a day and 30 mesure in one hour)
tab_array_P1=np.empty((index_fin,29))
tab_array_P1[:]= np.nan

tab_array_P2=np.empty((index_fin,29))
tab_array_P2[:]= np.nan

dates_fin=[];
hour=[]
for i in range(24):
    for j in range(0,60,2):
        if j<10:
            hour.append(str(i) +":"+"0"+str(j))
        else:
           hour.append(str(i) +":"+str(j)) 
hour_final=hour*N   

#creation of the "date" datas
for i in range(len(dates)):
    dates_fin=dates_fin + 24*30*[dates[i]]
    
#creation of the litteral index by concatenating date and hour     
index_lit=[]
for j in range(24*30*N):
    index_lit.append(dates_fin[j] +"-"+ hour_final[j])


#creation of the columns names
mesure.append("Voltaje_(R)_[V]")	
mesure.append("Voltaje_(S)_[V]")	
mesure.append("Voltaje_(T)_[V]")	
mesure.append("Voltaje_(RS)_[V]")	
mesure.append("Voltaje_(ST)_[V]")	
mesure.append("Voltaje_(TR)_[V]")	
mesure.append("Corriente_R_[A]")	
mesure.append("Corriente_S_[A]")	
mesure.append("Corriente_T_[A]")	
mesure.append("Potencia_R_[VA]")	
mesure.append("Potencia_S_[VA]")	
mesure.append("Potencia_T_[VA]")	
mesure.append("Potencia_R_[W]")	
mesure.append("Potencia_S_[W]")	
mesure.append("Potencia_T_[W]")	
mesure.append("Potencia_R_[VAR]")	
mesure.append("Potencia_S_[VAR]")	
mesure.append("Potencia_T_[VAR]")	
mesure.append("Corriente_N_[A]")	
mesure.append("Frecuencia_[Hz]")	
mesure.append("not_sure_1")	
mesure.append("not_sure_2")	
mesure.append("not_sure_3")	
mesure.append("Potencia_3F_[KVA]")	
mesure.append("Potencia_3F_[W]")	
mesure.append("Potencia_3F_[VAR]")	
mesure.append("Factor de Potencia")

df_p1=pd.DataFrame(tab_array_P1, index = index_lit, columns = mesure)
df_p2=pd.DataFrame(tab_array_P2, index = index_lit, columns = mesure)

df_p1.astype(float)
df_p1.astype({'Fecha': str , 'Hora': str})
df_p1["Fecha"]=dates_fin
df_p1["Hora"]=hour_final

df_p2.astype(float)
df_p2.astype({'Fecha': str , 'Hora': str})
df_p2["Fecha"]=dates_fin
df_p2["Hora"]=hour_final

#%%



#extraction of the dataframe in two list l_P1 for the P1 datas, L_P2 for the P2 datas  
for i in os.scandir("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/OneDrive_2022-05-04/Demanda eléctrica UDLA"):
    if i.is_dir() and i.name[0]=='2':
        s=i.path;
        s = list(s)
        s[110]='/';
        s = "".join(s)
        # print the folder  being explored
        print('Folder: ' + s)
        for j in os.scandir(s):
            if j.is_dir():
                s=j.path;
                s = list(s)
                s[115]='/';
                s = "".join(s)
                csv_files = glob.glob(os.path.join(s, "*.txt"))
                for f in csv_files:
                    name=f.split("\\")[-1];
                    
                    if "P1" in name:
                        l_P1.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure,decimal=","or ".",))
                    else:
                        l_P2.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure,decimal="," or "."))
                    # print the filename
                    print('File Name:', name)    
    else:
         s=i.path;
         s = list(s)
         s[110]='/';
         s = "".join(s)
         # print the folder  being explored
         print('Folder: ' + s)
         csv_files = glob.glob(os.path.join(s, "*.txt"))
         for f in csv_files:
             name=f.split("\\")[-1];
             if "ASC" in name:
                 l_ASC_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "P0" in name:
                 l_P0_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "P1" in name:
                 l_P1_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "P2" in name:
                 l_P2_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))    
             elif "P3" in name:
                 l_P3_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "P4" in name:
                 l_P4_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))    
             elif "P5" in name:
                 l_P5_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "P6" in name:
                 l_P6_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))    
             elif "TDP-S1" in name:
                 l_S1_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "TDP-S2" in name:
                 l_S2_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "TDP-S3" in name:
                 l_S3_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "TDP-S4" in name:
                 l_S4_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "TDP-S5" in name:
                 l_S5_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "UPS1" in name:
                 l_UPS1_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))    
             elif "UPS2" in name:
                 l_UPS2_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "UPS3" in name:
                 l_UPS3_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))   
             elif "CUB1" in name:
                 l_CUB1_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "CUB2" in name:
                 l_CUB2_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))   
             elif "TV-CUB" in name:
                 l_CUB_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             elif "Bombas" in name:
                 l_bombas_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))   
             elif "Data Center" in name:
                 l_data_center_cov.append(pd.read_csv(f,sep=r"\s+",header=None,names=mesure))
             # print the filename
             print('File Name:', name)
l_cov.append(l_ASC_cov)
l_cov.append(l_P0_cov)
l_cov.append(l_P1_cov)
l_cov.append(l_P2_cov)
l_cov.append(l_P3_cov)
l_cov.append(l_P4_cov)
l_cov.append(l_P5_cov)
l_cov.append(l_P6_cov)
l_cov.append(l_S1_cov)
l_cov.append(l_S2_cov)
l_cov.append(l_S3_cov)
l_cov.append(l_S4_cov)
l_cov.append(l_S5_cov)
l_cov.append(l_UPS1_cov)
l_cov.append(l_UPS2_cov)
l_cov.append(l_UPS3_cov)
l_cov.append(l_CUB1_cov)
l_cov.append(l_CUB2_cov)
l_cov.append(l_CUB_cov)
l_cov.append(l_bombas_cov)
l_cov.append(l_data_center_cov)

#%%

l_P1=l_P1+l_P1_cov
l_P2=l_P2+l_P2_cov
             
              
index_int=[]
for i in range(len(l_P2)):
    df_int=l_P2[i];
    pr_date=list(df_int["Fecha"])
    pr_heure=list(df_int["Hora"])
    for j in range(len(pr_heure)):
        s=list(pr_heure[j])
        if (s[-1]=="1" or s[-1]=="3" or s[-1]=="5" or s[-1]=="7" or s[-1]=="9") and len(pr_heure[j])==5 and s[0]=="0":
            del s[0]
            u=int(s[-1])
            u=u-1
            s[-1]=str(u)
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        elif len(pr_heure[j])==5 and s[0]=="0":
            del s[0]
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        elif s[-1]=="1" or s[-1]=="3" or s[-1]=="5" or s[-1]=="7" or s[-1]=="9":
            u=int(s[-1])
            u=u-1
            s[-1]=str(u)
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        else:
            index_int.append(pr_date[j] +"-"+pr_heure[j])
    df_int.insert(29,"index2",index_int)        
    df_int.set_index("index2",inplace=True)
    df_p2.loc[index_int,"Voltaje_(R)_[V]":"Factor de Potencia"]= df_int.loc[index_int,"Voltaje_(R)_[V]":"Factor de Potencia"]
    index_int=[]
    f=str(len(l_P2)-i)
    print("dataset-suivant-P2"+" "+f)
    
for i in range(len(l_P1)):
    df_int=l_P1[i];
    pr_date=list(df_int["Fecha"])
    pr_heure=list(df_int["Hora"])
    for j in range(len(pr_heure)):
        s=list(pr_heure[j])
        if (s[-1]=="1" or s[-1]=="3" or s[-1]=="5" or s[-1]=="7" or s[-1]=="9") and len(pr_heure[j])==5 and s[0]=="0":
            del s[0]
            u=int(s[-1])
            u=u-1
            s[-1]=str(u)
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        elif len(pr_heure[j])==5 and s[0]=="0":
            del s[0]
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        elif s[-1]=="1" or s[-1]=="3" or s[-1]=="5" or s[-1]=="7" or s[-1]=="9":
            u=int(s[-1])
            u=u-1
            s[-1]=str(u)
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        else:
            index_int.append(pr_date[j] +"-"+pr_heure[j])
    df_int.insert(29,"index2",index_int)        
    df_int.set_index("index2",inplace=True)
    df_p1.loc[index_int,"Voltaje_(R)_[V]":"Factor de Potencia"]= df_int.loc[index_int,"Voltaje_(R)_[V]":"Factor de Potencia"]
    index_int=[]
    f=str(len(l_P1)-i)
    print("dataset-suivant-P1"+" "+f)
#%%
cols=mesure[2:29]
df_p1[cols]=df_p1[cols].replace(',','.',regex=True).astype(float)
df_p2[cols]=df_p2[cols].replace(',','.',regex=True).astype(float)
#%%
df_p1.to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_entier_année_mois/df_p1_full.txt",sep=',',columns=mesure,index=True)
df_p2.to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_entier_année_mois/df_p2_full.txt",sep=',',columns=mesure,index=True)    
print("Big dataframe written")        
#%%
L_annee_P1=[]
L_mois_P1=[]
start1 = datetime.datetime.strptime("07-2015", "%m-%Y")
end1=datetime.datetime.strptime("01-2022", "%m-%Y")
mois = list(pd.date_range(start1,end1,freq='M').strftime("%m-%Y"))
annee=["2015","2016","2017","2018","2019","2020","2021"]
booll=[]
for j in range(len(mois)):
    for i in range(len(index_lit)):
        booll.append(mois[j] in index_lit[i])
    L_mois_P1.append(df_p1.loc[booll,"Fecha":"Factor de Potencia"])
    L_mois_P1[j].to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_entier_année_mois/df_p1"+"-"+mois[j]+".txt",sep=',',columns=mesure,index=True)
    booll=[]
for j in range(len(annee)):
    for i in range(len(index_lit)):
        booll.append(annee[j] in index_lit[i])
    L_annee_P1.append(df_p1.loc[booll,"Fecha":"Factor de Potencia"])
    L_annee_P1[j].to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_entier_année_mois/df_p1"+"-"+annee[j]+".txt",sep=',',columns=mesure,index=True)
    booll=[]    
#%%
L_annee_P2=[]
L_mois_P2=[]
booll=[]
for j in range(len(mois)):
    for i in range(len(index_lit)):
        booll.append(mois[j] in index_lit[i])
    L_mois_P2.append(df_p2.loc[booll,"Fecha":"Factor de Potencia"])
    L_mois_P2[j].to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_entier_année_mois/df_p2"+"-"+mois[j]+".txt",sep=',',columns=mesure,index=True)
    booll=[]
for j in range(len(annee)):
    for i in range(len(index_lit)):
        booll.append(annee[j] in index_lit[i])
    L_annee_P2.append(df_p2.loc[booll,"Fecha":"Factor de Potencia"])
    L_annee_P2[j].to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_entier_année_mois/df_p2"+"-"+annee[j]+".txt",sep=',',columns=mesure,index=True)
    booll=[]      
print("Dataframe of month and years written")
#%%
start2 = datetime.datetime.strptime("01-01-2019", "%d-%m-%Y")
end2 = datetime.datetime.strptime("31-12-2022", "%d-%m-%Y")
dates2 = list(pd.date_range(start2, end2).strftime("%d-%m-%Y"))
N2=len(dates2)
index_fin_2=N2*24*30

tab_array_cov=np.empty((index_fin_2,29))
tab_array_cov[:]= np.nan

hour_final_2=hour*N2
dates_fin_2=[]
for i in range(len(dates2)):
    dates_fin_2=dates_fin_2 + 24*30*[dates2[i]]

index_lit2=[]
for j in range(24*30*N2):
    index_lit2.append(dates_fin_2[j] +"-"+ hour_final_2[j])
        
df_cov=pd.DataFrame(tab_array_cov, index = index_lit2, columns = mesure)  
df_cov.astype({'Fecha': str , 'Hora': str})
df_cov["Fecha"]=dates_fin_2
df_cov["Hora"]=hour_final_2
    
df_cov.iloc[:,2:29]=np.nan 
names=["ASC","P0","P1","P2","P3","P4","P5","P6","TDP-S1","TDP-S2","TDP-S3","TDP-S4","TDP-S5","UPS1","UPS2","UPS3","CUB1","CUB2","TV-CUB","Bombas","Data-center"]
l_cov_2=[]  
index_int=[]
for i in range(len(l_cov)):
    l_cov_2.append(pd.concat(l_cov[i], ignore_index=True))
for i in range(len(l_cov)):
    df_int=l_cov_2[i]
    df_int.sort_values(by=['Fecha','Hora'])
    pr_date=list(df_int["Fecha"])
    pr_heure=list(df_int["Hora"])
    for j in range(len(pr_heure)):
        if pd.isna(pr_heure[j])==True:
            pr_heure[j]=pr_heure[j-1]
        if pd.isna(pr_date[j])==True:
            pr_date[j]=pr_date[j-1]
    for j in range(len(pr_heure)):
        s=list(pr_heure[j])
        if (s[-1]=="1" or s[-1]=="3" or s[-1]=="5" or s[-1]=="7" or s[-1]=="9") and len(pr_heure[j])==5 and s[0]=="0":
            del s[0]
            u=int(s[-1])
            u=u-1
            s[-1]=str(u)
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        elif len(s)==5 and s[0]=="0":
            del s[0]
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        elif s[-1]=="1" or s[-1]=="3" or s[-1]=="5" or s[-1]=="7" or s[-1]=="9":
            u=int(s[-1])
            u=u-1
            s[-1]=str(u)
            pr_heure[j]="".join(s)
            index_int.append(pr_date[j] +"-"+pr_heure[j])
        else:
            if pd.isna(pr_date[j])==True:
                index_int.append(pr_date[j-1] +"-"+pr_heure[j])
            else:
                index_int.append(pr_date[j] +"-"+pr_heure[j])
    df_int.insert(29,"index2",index_int)        
    df_int.set_index("index2",inplace=True)
    print(df_int.index.is_unique)
    df_int=df_int[~df_int.index.duplicated()]
    print(df_int.index.is_unique)
    df_cov.loc[index_int,"Voltaje_(R)_[V]":"Factor de Potencia"]= df_int.loc[index_int,"Voltaje_(R)_[V]":"Factor de Potencia"]
    df_cov.to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_cov_(2019-2021)/df_cov-"+names[i]+".txt",sep=',',columns=mesure,index=True)
    df_cov.iloc[:,2:29]=np.nan    
    index_int=[]
    f=str(len(l_cov)-i)
    print("dataset-suivants-cov"+" "+f)
#%%        
indice_extrait_P1=[]
continu_mois_p1=[]

for j in range(len(L_mois_P1)):
    indice_extrait_P1.append(extractl(L_mois_P1[j]))
    if pd.isna(indice_extrait_P1[j][0])==False:
        continu_mois_p1.append(L_mois_P1[j].loc[indice_extrait_P1[j][0]:indice_extrait_P1[j][1],mesure])
print("ok P1")    
   
indice_extrait_P2=[]
continu_mois_p2=[]
    
for j in range(len(L_mois_P2)):
    indice_extrait_P2.append(extractl(L_mois_P2[j]))
    if pd.isna(indice_extrait_P2[j][0])==False:
        continu_mois_p2.append(L_mois_P2[j].loc[indice_extrait_P2[j][0]:indice_extrait_P2[j][1],mesure])
print("ok P2")  
for i in range(len(continu_mois_p1)):
    h=str(i)
    continu_mois_p1[i].to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_continu/df_cov_continu_1_"+h+".txt",sep=',',columns=mesure,index=True)    
for i in range(len(continu_mois_p2)):
    h=str(i)
    continu_mois_p2[i].to_csv("C:/Users/alexa/OneDrive/Documents/Code en tout genre/Python Scripts/df_continu/df_cov_continu_2_"+h+".txt",sep=',',columns=mesure,index=True)     

    
    
    