import pandas as pd

sheets = ["2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011",
         "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001",
         "2000", "1999", "1998", "1997", "1996", "1995", "1994", "1993", "1992"]

c = {'Unnamed: 1': 'Kind of Business'}

def preprocess(year):
    df = pd.read_excel("mrtssales92-present.xls", sheet_name = year, skiprows = 4, skipfooter = 47)
    df.drop(df.columns[[0,14]], axis = 1, inplace = True)
    df.rename(columns = c, inplace = True)
    df_melted = df.melt(id_vars = "Kind of Business", value_vars = df.columns[1:])
    df_melted.replace("(S)", 0, inplace = True)
    df_melted.replace("(NA)", 0, inplace = True)
    df_melted.dropna(axis = 0, inplace = True)
    df_melted['value'] = df_melted['value'].astype(float)
    df_melted = df_melted.astype({'variable': 'datetime64[ns]'})
    df_melted.rename({'variable':'Period', 'value': 'Sales'}, axis = 1, inplace = True)
    return df_melted

df_final = preprocess(sheets[0])

for year in sheets[1:]:
    df_temp = preprocess(year)
    df_final = pd.concat([df_final, df_temp])

df_final.to_csv('final_data.csv')