import pandas as pa, glob, os
class DataProcessor(object):

    def generate_features(self, data_frame, historic_range, sample_window, outfile):
        aggregated_chunk_window = 2*(sample_window-1) - 1
        df_list = []
        for x in range(0,historic_range):
            df_copy = data_frame.copy()
            df_size = data_frame.count(axis=0).iloc[0]
            df_chunk_rows = df_size - aggregated_chunk_window + x
            df_chunked = df_copy[x:df_chunk_rows]
            df_chunked_size = df_chunked.count(axis=0).iloc[0]
            df_chunked.index = range(df_chunked_size)
            df_list.append(df_chunked)
        df_concat_file = pa.concat(df_list, axis=1)
        df_concat_file.to_csv(outfile, index=None)

    def generate_class_labels(self, csv_raw_data_folder, state, sample_window, outfile):
        label_file_regex = csv_raw_data_folder + '/' + state + '*.csv'
        df = pa.concat(map(pa.read_csv, glob.glob(os.path.join("", label_file_regex))), ignore_index=True)
        df.columns = ['dom', 'doy', 'mnth', 'yr', 'pcp']
        s_val_data = []
        for index,row in df.iterrows():
            if (index + sample_window) <= len(df):
                s_val = "S_" + str(int(row[2])) + "/" + str(int(row[0])) + "/" + str(int(row[3]))
                subset_ix = range(index, index + sample_window)
                s_val_data.append([s_val, df.iloc[subset_ix]['pcp'].sum()])
        s_val_df = pa.DataFrame(s_val_data)
        s_val_df.columns = ['s_val', 'pcp_sum']
        s_val_df['c_val'] = 0
        s_val_df.loc[s_val_df['pcp_sum'] >= s_val_df['pcp_sum'].quantile(0.95), 'c_val'] = 1
        print s_val_df
        s_val_df.to_csv(outfile)


