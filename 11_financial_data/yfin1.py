
#https://colab.research.google.com/drive/1rspCrN8NEsEjeYmmN1pG0gDmvP8WswE3?usp=sharing

#pip install yfinance
import yfinance as yf
data=yf.download('TSLA')
print(data)
print(data.columns)
l1=[]
for i in data.columns:
    l1.append(i[0])
data.columns=l1
print(data)