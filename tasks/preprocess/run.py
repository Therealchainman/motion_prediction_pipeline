# import re
# import io
import os
# from glob import glob
import pandas as pd


# def read_file(path):
#     result = ""
#     with io.open(path, "r", encoding="utf-8") as file:
#         result = file.read()
#     return result

# def prune_front_matter(text):
#     lines = text.split("\n")
#     seen = 0

#     for ix, line in enumerate(lines):
#         if line == '---':
#             if seen == 1:
#                 return "\n".join(lines[(ix+1):]).strip()
#             else:
#                 seen += 1

# def remove_code(text):
#     return re.sub(r'==##==', "\n", re.sub(r'```.*```', '' , re.sub(r'\n', '==##==', text)))

# def build_dataframe():
#     files = glob('/data/blog/**/**/**/*.md')
#     contents = [read_file(path) for path in files]
#     texts = [remove_code(prune_front_matter(text)).lower() for text in contents]

#     articles = pd.DataFrame({ 'file': ["/".join(p.split("/")[3:]) for p in files], 'text': texts })
#     articles.to_parquet('/data/articles.parquet')

#     print(f"Wrote data frame for paths (showing 10): {articles.head(10)['file'].tolist()}")

def loadData(file):
    return pd.read_csv(f"/data/projects/car-insurance/data/{file}")


def dropColumns(df):
    df.drop(inplace=True, columns=["default_or_not", "last_contact_month", "no_of_contacts", "days_passed", "last_contact_day",
            "communication", "car_loan", "balance_amt", "education_level", "marital_status", "job_type", "prev_attempts"])


def getSeconds(time):
    return 3600*int(time[0])+60*int(time[1])+int(time[2])


def duration(start, end):
    slst = start.split(':')
    elst = end.split(':')
    ss = getSeconds(slst)
    ee = getSeconds(elst)
    dur = ee-ss
    if dur < 0:
        return dur+3600*24
    return dur

# Inserts the call duration into the dataframe inplace


def insertCallDur(df):
    call_duration = [duration(row['call_start'], row['call_end'])
                     for _, row in df.iterrows()]
    df.drop(inplace=True, columns=['call_start', 'call_end'])
    df.insert(3, 'duration', call_duration)


def dataProcess(df):
    df.loc[(df.Outcome == "success"), "Outcome"] = 1
    df.loc[(df.Outcome == "other") | (df.Outcome.isna()), "Outcome"] = 0
    df.loc[(df.Outcome == "failure"), "Outcome"] = -1


def saveDataFrame(df, file):
    df.to_csv(f'/data/projects/car-insurance/data/{file}')


def createDataFrame(file):
    df = loadData(file)
    # Part of the data cleanup, removing columns
    dropColumns(df)
    # Part of preprocessing the data, finding the duration
    insertCallDur(df)
    # More data processing, this time setting outcome from string to numerical values.
    dataProcess(df)
    if file == 'Train_data.csv':
        saveDataFrame(df, 'df_train.csv')
    else:
        saveDataFrame(df, 'df_test.csv')
    return df


if __name__ == '__main__':
    if os.path.isfile('/data/projects/car-insurance/data/df_train.csv') and os.path.isfile('/data/projects/car-insurance/data/df_test.csv'):
        print("Skipping as the data frame file already exsists")
    else:
        createDataFrame('Train_data.csv')
        createDataFrame('Test_data.csv')
