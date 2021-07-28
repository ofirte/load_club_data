import sys
import pandas as pd
import numpy as np
import argparse


def open_excel(path, sheet=0, status=""):
    try:
        if status == "r":
            xl = pd.read_excel(path, sheet)
        else:
            xl = pd.ExcelFile(path)
        return xl
    except Exception as e:
        print("Error while opening Excel file")
        print(e)


def parse_headers(xl):
    return np.array2string(xl.columns.values, formatter={'int': lambda x: chr(x).encode()}, separator=',').strip('[]')


def get_next_id(header, table):
    ids = table[header].unique()
    return ids[len(ids)-1]+1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path", help="Path to Database Excel Sheet")
    parser.add_argument("data_path", help="Path to the Data Excel Sheet that you wish to insert into the Database")
    parser.add_argument("club_id", help="Id of the club.",
                        type=int)
    return parser.parse_args()


def insert_data_to_user_table(data_table, club_id, user_table):
    user_headers = parse_headers(user_table)
    user_id = get_next_id('id', user_table)
    x = data_table["email"].unique()
    y = data_table["email"]
    if len(data_table["email"].unique()) != len(data_table["email"]):
        sys.exit("There are duplicated email address in the data file!\nNo info was added to the DB")
    for index, row in data_table.iterrows():
        values = "({},{},{},{},{},{},{})".format(user_id+index, row['first_name'], row['last_name'], row['phone'],
                                                 row['email'], row['membershp_start_date'].date(), club_id)
        print("INSERT INTO USERS ({})\nVALUES({})".format(user_headers, values))


def insert_data_to_membership_table(xl, membership_table, user_table):
    memberships_headers = parse_headers(membership_table)
    membership_id = get_next_id('id', membership_table)
    user_id = get_next_id('id', user_table)
    for index, row in xl.iterrows():
        values = "({},{},{},{},{})".format(membership_id+index, user_id+index, row['membershp_start_date'].date(),
                                                 row['membership_end_date'].date(), row['membership_name'])
        print("INSERT INTO MEMBERSHIPS ({})\nVALUES{};".format(memberships_headers, values))


def main(args):
    db_tables = open_excel(args.db_path)
    user_table = open_excel(args.db_path, db_tables.sheet_names[0], "r")
    membership_table = open_excel(args.db_path, db_tables.sheet_names[1], "r")
    data_table = open_excel(args.data_path, status="r")
    insert_data_to_user_table(data_table, args.club_id, user_table)
    insert_data_to_membership_table(data_table, membership_table, user_table)


if __name__ == '__main__':
    main(parse_args())
