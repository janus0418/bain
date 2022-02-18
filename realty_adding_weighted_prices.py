import os
import glob
import pandas as pd

# os.chdir("C:\Users\hp\Desktop\석승훈\Coding\.vscode\아파트전월세\TEST.csv")

# extension = "csv"

# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# print(all_filenames)

# combined = pd.concat([pd.read_csv(f, encoding='cp949') for f in all_filenames])

# combined.to_csv("TEST_maymay.csv", index=False, encoding="utf-8-sig")

df = pd.read_csv("C:/Users/hp/Desktop/석승훈/Coding/.vscode/아파트전월세/TEST.csv", encoding ='utf-8-sig')

# df['weighted'] = df['보증금(만원)'].astype(int)*100 + df['월세(만원)'].astype(int)

df['보증금(만원)'] = df['보증금(만원)'].replace(',','',regex = True)

df['보증금(만원)'] = df['보증금(만원)'].apply(pd.to_numeric, errors='coerce')

df['월세(만원)'] = df['월세(만원)'].replace(',','',regex = True)

df['월세(만원)'] = df['월세(만원)'].apply(pd.to_numeric, errors='coerce')

df['weighted'] = df['보증금(만원)'] + df['월세(만원)']*100

df['year'] = df['계약년월'].astype(str).str[:4]

print(df['보증금(만원)'].dtypes)
print(df['월세(만원)'].dtypes)
print(df['weighted'].dtypes)

df.to_csv('TEST_weighted.csv',index=False, encoding="utf-8-sig")