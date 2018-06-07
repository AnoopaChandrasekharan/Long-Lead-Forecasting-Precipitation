import pandas
import os
class CsvManipulator(object):

    def __init__(self, csv_raw_data_folder):
        self.csv_raw_data_folder = csv_raw_data_folder

    def construct_map_variable_to_filelist(self, variables_list):
        variable_file_list_map = {}
        for variable in variables_list:
            filelist = []
            for file in os.listdir(self.csv_raw_data_folder):
                if file.startswith(variable):
                    filelist.append(self.csv_raw_data_folder + '/' + file)
            variable_file_list_map[variable] = sorted(filelist)
        return variable_file_list_map

    def concat_variable_filelist_vertical(self, variable_file_list_map, outfolder):
        variable_concated_files_map = {}
        for variable in variable_file_list_map.keys():
            variable_files_frame_list = []
            for variable_file in variable_file_list_map[variable]:
                df = pandas.read_csv(variable_file, index_col=None, header=0)
                variable_files_frame_list.append(df)
            variable_frame = pandas.concat(variable_files_frame_list)
            outfile = outfolder + '/' + variable + '.csv'
            variable_frame.to_csv(outfile, index=None)
            variable_concated_files_map[variable] = variable_frame
        return variable_concated_files_map

    def concat_variables_filelists_horizontal(self, variable_concated_files_map, outfile):
        variable_file_list = variable_concated_files_map.values()
        concat_df = pandas.concat(variable_file_list, axis=1)
        concat_df.to_csv(outfile, index=None)
        return concat_df






