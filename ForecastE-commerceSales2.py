import sys
import pandas as pd
import plotly.express as px
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from datetime import datetime
from collections import Counter

# Dataset
Data = pd.read_csv(r"F:\DataAnalysis\ForecastE-commerceSales\online+retail\Online Retail.csv")
Head = Data.head(5)
Tail = Data.tail(5)
Information = Data.info
Describe = Data.describe()

## Data Cleaning

# Null Values
NullCheck = Data.isnull().mean()
CustomerID_nulls = Data[Data['CustomerID'].isnull()]
Description_nulls = Data[Data['Description'].isnull()]

null = Data['CustomerID'].notnull()
count = 0
for i in null:
    if i == False:
        count += 1

#Data['CustomerID'] = Data['CustomerID'].fillna(15287)
#Data['Description'] = Data['Description'].fillna('Anything')
#Data['quantity_without_outliers'] = Data['quantity_without_outliers'].bfill()
#Data.to_csv("F:\DataAnalysis\ForecastE-commerceSales\online+retail\Online Retail.csv", index=False)

# Outlier Values
box1 = sb.boxplot(Data)
#plt.show()
scatter1 = sb.scatterplot(Data)
#plt.show()
box2 = sb.boxplot(Data['Quantity'])
#plt.show()
scatter2 = sb.scatterplot(Data['Quantity'])
#plt.show()

#Data['quantity_without_outliers'] = Data[Data['Quantity'] > Data['Quantity'].quantile(0.0001)]['Quantity']
#Data['quantity_without_outliers'] = Data[Data['Quantity'] < Data['Quantity'].quantile(0.9999)]['quantity_without_outliers']
#Data.to_csv("F:\DataAnalysis\ForecastE-commerceSales\online+retail\Online Retail.csv", index=False)

box3 = sb.boxplot(Data['quantity_without_outliers'])
#plt.show()
scatter3 = sb.scatterplot(Data['quantity_without_outliers'])
#plt.show()

## Statitics


class CountGood:

    def __init__(self, country_name='0', column_name='0'):
        self.country_name = country_name
        self.column_name = column_name

    def most_traded_good(self):
        group = []
        for i in Data['Description'].groupby(Data['Country']):
            group.append(i)
        for x in range(len(set(Data['Country']))):
            for j in group[x][1:]:
                if group[x][0] == self.country_name:
                    print(f'\nThe Most Traded Good In {group[x][0]}:')
                    item = []
                    for i in Counter(j).most_common()[0:1]:
                        item.append(i)
                    print(item[0][0], ':', item[0][1])

    def trades_per_good(self):
        group = []
        for i in Data['Description'].groupby(Data['Country']):
            group.append(i)
        for x in range(len(set(Data['Country']))):
            for j in group[x][1:]:
                if group[x][0] == self.country_name:
                    print(group[x][0])
                    for k, v in Counter(j).most_common(10):
                        print(k, ':', v)

    def sold_quantity_per_good(self):
        group = []
        for i in Data['Description'].groupby(Data['Country']):
            group.append(i)
        for x in range(len(set(Data['Country']))):
            for j in group[x][1:]:
                if group[x][0] == self.country_name:
                    print(group[x][0])
                    group2 = []
                    for n in Data['quantity_without_outliers'].groupby(j):
                        group2.append(n)
                    sum = 0
                    for r in range(10):
                        for d in group2[r][1]:
                            sum += d
                        print('\nThe Good Name:', group2[r][0])
                        print('The Sold Quantity: ', sum)

    def profit_per_good(self):
        group = []
        for i in Data['Description'].groupby(Data['Country']):
            group.append(i)
        for x in range(len(set(Data['Country']))):
            for j in group[x][1:]:
                if group[x][0] == self.country_name:
                    print(group[x][0])
                    group2 = []
                    for n in Data['quantity_without_outliers'].groupby(j):
                        group2.append(n)
                    sum = 0
                    count = 0
                    for k, v in Counter(j).items():
                        count += 1
#                    for r in range(count):
                    for r in range(10):
                        for d in group2[r][1]:
                            sum += d
                        unit_price = []
                        for q in Data['UnitPrice'].groupby(j):
                            unit_price.append(q)
                        total_sum = 0
                        for o in unit_price[r][1]:
                            total_sum += o*d
                        print(f'The Total Sell For {unit_price[r][0]} Is : ', total_sum)

    def total_profit(self):
        add = []
        for i in Data['quantity_without_outliers'].groupby(Data['Country']):
            add.append(i)

        add2 = []
        for i in Data['UnitPrice'].groupby(Data['Country']):
            add2.append(i)

        count = 0
        for i in add:
            count += 1

        for i in range(count):
            if add[i][0] == self.country_name:
                print(f'Total profit for {self.country_name}: ', sum(add[i][1] * add2[i][1]))

    def counter(self):
        for k, v in Counter(Data[self.column_name]).most_common():
            print(k, ':', v)


country = CountGood('United Kingdom', 'Country')
#print(country.trades_per_good())
#print(country.most_traded_good())
#print(country.profit_per_good())
#print(country.sold_quantity_per_good())
#print(country.total_profit())
#print(country.counter())



## Charts

kd = sb.kdeplot(Data['quantity_without_outliers'], color='blue')
plt.title('Probability distribution of quantity')
plt.xlabel('Quantity')
#plt.show()

line = sb.lineplot(Data['quantity_without_outliers'], color='red')
plt.ylabel('Quantity')
plt.title('Quantity Changes')
#plt.show()

scatter = sb.scatterplot(Data['quantity_without_outliers'], color='orange')
plt.ylabel('Quantity')
plt.title('Quantity Scatter Plot')
#plt.show()


## Run To Text File
with open("F:\DataAnalysis\ForecastE-commerceSales\ForecastE-commerceSales.txt", 'w') as file:
    sys.stdout = file
    print('First 5 Rows:\n', Head)
    print('\nLast 5 Rows:\n', Tail)
    print('\nData Information:\n', Information)
    print('\nData Description:\n', Describe)
    print('\nThe Number of Trades for each Country')
    print('\n', country.counter())
    print('\nThe Total Trades for each Good')
    print(country.trades_per_good())
    print(country.most_traded_good())
    print(country.sold_quantity_per_good())
    print(country.profit_per_good())
    print(country.total_profit())
