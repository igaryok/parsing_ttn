import string
import re
import time


import google_api
import novaposhta_api
import db
from log import log


def get_var(var, file):
    """
    return value of variable from settings file
    :param var: string with variable which value we want to get know
    :param file: string with path to settings file
    :return: string with value
    """
    value = None
    with open(file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            if re.match(var, line):
                value = line.split("=")[1].strip()
                break

    return value


def convert_label(label):
    """
    convert label of column to number of column
    :param label: string with label
    :return: string with number
    """
    return string.ascii_uppercase.index(label)


def main(settings):
    """
    main function
    :param settings: string with folders name which includes files with settings
    alter.ini - main text-file with settings
    code.ini - text-file with TTN's status-code from API Nova Poshta
    :return: None
    """
    log.info("START parsing")
    path_alter = settings+"/alter.ini"
    auth_var = (settings+"/"+get_var("CREDENTIAL", path_alter),
                get_var("SHEET", path_alter),
                get_var("WORKSHEET", path_alter))

    # initialization google sheet
    sheet = google_api.GoogleAPI(*auth_var)

    ttn_var = (convert_label(get_var("COL_TTN", path_alter)),
               convert_label(get_var("COL_WRITESYMBOL", path_alter)),
               int(get_var("START_ROW", path_alter)))

    # get numbers of TTN from sheet, received dictionary(
    # key - TTN as string, value - list of two values (number row and status-symbol from sheet))
    data_sheet = sheet.get_all_ttn(*ttn_var)
    for key, item in data_sheet.items():
        log.info(f"check for {key} old status {item[1]}")

    # check status for TTN from Nova POshta api, return list of tuples(
    # first item - string with ttn, second - string status ttn, third - string with code-status ttn)
    current_status = novaposhta_api.check_ttn(get_var("API_KEY", path_alter), data_sheet.keys())

    symbols_var = settings+"/code.ini"
    for item in current_status:
        db.write_status_db(item[0], item[1], item[2], int(data_sheet[item[0]][0]))
        set_symbol, set_color = list(item.strip() for item in get_var(item[2], symbols_var).split(","))
        if not(set_symbol == data_sheet[item[0]][1]):
            row = sheet.find_by_col(convert_label(get_var("COL_TTN", path_alter)), item[0])
            sheet.write_value(get_var("COL_WRITESYMBOL", path_alter), str(row), set_symbol)
            log.info(f"write new status for {item[0]} in {row} row")

            if get_var("COLORED_TTN", path_alter) == "1" and set_color:
                sheet.color_cell(get_var("COL_TTN", path_alter), str(row), set_color)

            time.sleep(0.2)

    log.info("FINISH parsing")


def start(path="settings"):
    try:
        main(path)
    except Exception as msg:
        log.error(f"Error in parsing {msg}")


if __name__ == '__main__':
    start()
