import pandas as pd

class Data2Excel:
    def __init__(self, sheet_names):
        self.sheet_names = sheet_names
        self.data_dict = {}
        self.dataframes = {}
        for name in sheet_names:
            self.data_dict[name] = []

    def add_row(self):
        for value in self.data_dict.values():
            value.append([])

    def add_sheet_name(self, sheet_name):
        self.data_dict[sheet_name] = []

    def add_dataframes(self, sheet_name, dataframe):
        self.dataframes[sheet_name] = dataframe

    def add_data(self, sheet_name, data1):
        if sheet_name in self.data_dict.keys():
            self.data_dict[sheet_name][-1].append(data1)
        else:
            self.data_dict[sheet_name] = [[]]
            self.data_dict[sheet_name][-1].append(data1)

    # def create_dataframes(self):
    #     for name, value in self.data_dict.items():
    #         self.dataframes[name] = pd.DataFrame(value)

    def write2excel(self, sheet_names, header, writer1):
        for key_name in sheet_names:
            df_output = pd.DataFrame(self.data_dict[key_name], columns=header)
            df_output.to_excel(writer1, sheet_name=key_name, index=False)
