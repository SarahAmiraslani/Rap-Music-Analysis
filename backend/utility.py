# utility
import os

def results_csv(df_hits):

    current_datetime_str = datetime.today().strftime("%m/%d/%Y")

    repo = os.getcwd()
    csv_path = "results_csv"

    if csv_path not in os.listdir():
        os.mkdir(repo + os.sep + csv_path)
    # file naming/ path convention:
    import datetime

    current_datetime_str = str(datetime.datetime.now())
    csv_path = "/results_csv/"
    df_hits_time = str(df_hits["Date"][0])
    csv_name = df_hits_time + current_datetime_str + ".csv"

    # export dataframe:
    df_hits.to_csv(csv_path + os.sep + csv_name, encoding="utf-8")


# TODO: we should get comments and page views
