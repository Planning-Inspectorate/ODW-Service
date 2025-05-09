import csv
import os


files = [x for x in os.listdir("pipelines/scripts/csvs") if x.endswith(".csv")]

files_to_ignore = [
    "prod_en010012_Extract_20250425_100947.csv"
]
rows_to_ignore = [
    #15369
]
for file in files:
    with open(f"pipelines/scripts/csvs/{file}", "r") as f:
        if file in files_to_ignore:
            csv_reader = csv.reader(f, quotechar='"', escapechar='\\')
            for i, row in enumerate(csv_reader):
                if i not in rows_to_ignore:
                    print("i: ", i)
                    a = str(row)
                    print(a)
