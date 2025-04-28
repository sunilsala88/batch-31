import pandas as pd
import numpy as np

a1=np.arange(25).reshape(5,5)
print(a1)

df1=pd.DataFrame(a1,columns=['c1','c2','c3','c4','c5'],index=['r1','r2','r3','r4','r5'])
print(df1)
