import os
import glob
import pandas as pd

os.chdir("C:/Users/hp/Desktop/석승훈/Coding/.vscode/아파트 매매")

extension = "csv"

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

print(all_filenames)

combined = pd.concat([pd.read_csv(f, encoding='cp949') for f in all_filenames])

combined.to_csv("TEST_maymay.csv", index=False, encoding="utf-8-sig")

