from pathlib import Path
import pandas as pd
import csv
from pandas import read_csv
import logging
import sqlite3

directory_in_str = 'etl_script/input'
output_csv = 'etl_script/output/consolidated_output.1.csv'
material_reference_csv = 'etl_script/input/data_source_2/material_reference.csv'
database = "../db.sqlite3"

logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d :: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

cnx = sqlite3.connect(database)

li = []

path_list = Path(directory_in_str).glob('**/sample_data.*.*')


def get_delimiter(path_in_str):
    with open(path_in_str) as f:
        first_line = f.readline()
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(first_line, delimiters=',|')
    delimiter = dialect.delimiter
    return delimiter


def bonus_1_1(df, path_in_str):
    """The sample_data.1 file has a number of products we do not want in our output.
    Filter this data so that the only products that remain are products with a worth of MORE than 1.00"""
    if "sample_data.1" in path_in_str:
        logger.info("solving bonus_1_1")
        df = df[df.worth > 1.00]
    return df

def bonus_1_2(df, path_in_str):
    """The true worth of products in sample_data.3 is based on the listed worth TIMES the material_id,
    recalculate the worth for this file to show that."""
    if "sample_data.3" in path_in_str:
        logger.info("solving bonus_1_2")
        df['worth'] = df['worth'] * df['material_id']
    return df

def bonus_1_3(df, path_in_str):
    """The true worth of products in sample_data.3 is based on the listed worth TIMES the material_id,
    recalculate the worth for this file to show that."""
    if "sample_data.2" in path_in_str:
        logger.info("solving bonus_1_3")
        df = df.groupby(['product_name']).agg(quality=('quality', 'first'),
                                                  material_id=('material_id', 'max'),
                                                  worth=('worth', 'sum')
                                                  ).reset_index()
    return df


def bonus_1_4(df):
    """Load and use the material_reference data file to get the material name for each product in the final dataframe"""

    df2 = pd.read_csv(material_reference_csv, index_col=None, header=0, sep=",")
    merged_dfs=pd.merge(df,df2, how='left', left_on=['material_id'], right_on=['id'])
    merged_dfs.pop('id')
    merged_dfs.pop('material_id')
    return merged_dfs


def main():
    for path in path_list:
        path_in_str = str(path)
        delimiter = get_delimiter(path_in_str)
        df = pd.read_csv(path_in_str, index_col=None, header=0, sep=delimiter)

        df = bonus_1_1(df, path_in_str)

        df = bonus_1_2(df, path_in_str)

        df = bonus_1_3(df, path_in_str)
        df['file_source'] = path_in_str.lstrip("input/")
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    logger.info("solving bonus_1_4")
    frame = bonus_1_4(frame)
    frame.to_csv(output_csv, sep=',', encoding='utf-8')

    # BONUS_1_5
    logger.info("solving bonus_1_5")
    frame.to_sql(name='etl_app_sampledata', con=cnx, if_exists='append', index=False)

def run():
    main()

if __name__ == "__main__":
    main()
