
import pandas as pd


def xlsx_reader(xlsx_file, column_names: list):
    filename = str(xlsx_file).rstrip('.xls')
    file_summary = {
        'file': filename,
        'summary': []
    }

    excel_file = pd.ExcelFile(xlsx_file)
    excel_sheet_names = excel_file.sheet_names

    # Co robi ta funkcja?
    # 1. Otwiera plik excela.
    # 2. Przeprowadza iteracje po:
    #   - arkuszach
    #   - kolumnach, które zwróciły true
    #   - po nazwach kolumn, żeby sprawdzić prawidłową nazwe
    # 3. Tworzy dict z danymi, które potrzeba zwrócić

    for sheet in excel_sheet_names:
        dataframe = pd.read_excel(xlsx_file, sheet_name=sheet)
        dataframe = dataframe.astype(str).apply(lambda x: x.str.strip())

        df_columns = dataframe.isin(column_names).any()

        for col_key, col_value in df_columns.items():
            if col_value:
                right_column_name = ''
                for col_name in column_names:
                    if col_name in dataframe[[col_key]].values:
                        right_column_name = col_name

                col_values_to_numeric = dataframe[[col_key]].apply(pd.to_numeric, errors='coerce')
                col_sum = col_values_to_numeric.sum()
                col_avg = col_values_to_numeric.mean()
                col_sum = round(col_sum.values[0], 2)
                col_avg = round(col_avg.values[0], 2)

                column_summary_dict = {
                    "column": right_column_name,
                    "sum": col_sum,
                    "avg": col_avg
                }
                file_summary['summary'].append(column_summary_dict)

    return file_summary
