import os
from lib.zipextractor import ZipExtractor
from lib.csvmanipulator import CsvManipulator
from lib.configservice import raw_zip_file_location
from lib.configservice import state
from lib.configservice import variables
from lib.configservice import historic_range
from lib.configservice import sample_window
from lib.dataprocessor import DataProcessor

def create_required_sub_folders(extract_data_folder):
    sub_folders = ["variable-combined-data", "state-combined-data", "features-data", "clabel-data"]
    for folder in sub_folders:
        sub_folder_path = extract_data_folder + '/' + folder
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)


def main():
    extract_data_folder = "extracted-data"
    zipExtractor = ZipExtractor(raw_zip_file_location, extract_data_folder)
    zipExtractor.extract_zip()
    create_required_sub_folders(extract_data_folder)

    #Populating data
    csvManipulator = CsvManipulator(extract_data_folder+"/raw_data")
    variable_file_list_map = csvManipulator.construct_map_variable_to_filelist(variables)
    ## Concatinating data first vertically and then horizontally
    variable_concated_files_map = csvManipulator.concat_variable_filelist_vertical(variable_file_list_map, extract_data_folder + "/" + "variable-combined-data")
    horizontal_concat_df = csvManipulator.concat_variables_filelists_horizontal(variable_concated_files_map, extract_data_folder + "/"+ "state-combined-data/combined.csv")

    dataProcessor = DataProcessor()
    dataProcessor.generate_features(horizontal_concat_df, historic_range, sample_window, extract_data_folder + "/features-data/features.csv")
    dataProcessor.generate_class_labels(extract_data_folder + "/raw_data", state, sample_window, extract_data_folder + "/clabel-data/c-label.csv")

if __name__ == "__main__":
    main()