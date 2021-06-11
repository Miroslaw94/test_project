import pandas as pd

from django.core.files.uploadedfile import InMemoryUploadedFile


def excel_columns_calculator(excel_file: InMemoryUploadedFile, column_names: list) -> dict:
    """
    Method which reads excel file and calculates sum and average values for each of given columns.

    :param excel_file:
    :param column_names: Name of columns from excel file which user wants to calculate.
    :return: Returns dict with name of excel file and sums and averages of given columns.
    """
    filename = str(excel_file).rstrip('.xls')
    file_summary = {
        'file': filename,
        'summary': []
    }

    excel_file = pd.ExcelFile(excel_file)
    excel_sheet_names = excel_file.sheet_names

    for sheet in excel_sheet_names:
        dataframe = pd.read_excel(excel_file, sheet_name=sheet)
        dataframe = dataframe.astype(str).apply(lambda x: x.str.strip())

        df_columns_to_calculate = dataframe.isin(column_names).any()

        for col_key, col_value in df_columns_to_calculate.items():
            if col_value:
                right_column_name = ''
                for col_name in column_names:
                    if col_name in dataframe[[col_key]].values:
                        right_column_name = col_name

                col_values_to_numeric = dataframe[[col_key]].apply(pd.to_numeric, errors='coerce')
                column_sum = col_values_to_numeric.sum()
                column_avg = col_values_to_numeric.mean()
                column_sum = round(column_sum.values[0], 2)
                column_avg = round(column_avg.values[0], 2)

                column_summary_dict = {
                    "column": right_column_name,
                    "sum": column_sum,
                    "avg": column_avg
                }
                file_summary['summary'].append(column_summary_dict)

    return file_summary
