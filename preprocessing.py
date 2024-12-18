import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("final_output.csv")

#imena svih kolona iz csv i njihovi tipovi
#print(df.info())

#procenat podataka koji fale
#print(df.isnull().sum()/df.shape[0]*100)

#broj dupliranih vrednosti
#print(df.duplicated().sum())

'''
for i in df.select_dtypes(include="object").columns:
    print(df[i].value_counts())
    print("***" * 10)
    '''

#informacije o podacima u svim kolonama
#print(df.describe().T.to_string())
