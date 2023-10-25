import os, sys
import pandas as pd

class DataManager():
    def __init__(self) -> None:
        working_dir = os.path.dirname(os.path.abspath(sys.argv[0])).replace('\\', '/')
        self.input_data_path = working_dir + '/input_data/'
        self.output_data_path = working_dir + '/output_data/'


    def read_data_from_xl(self, file_name: str) -> pd.DataFrame:
        filepath = self.input_data_path + file_name
        print(f'loading links from {filepath}...\n')
        df = pd.read_excel(filepath)
        return df
    

    def write_data_to_xl(self, links: list, file_name: str) -> None:
        df = pd.DataFrame(links)
        save_path = self.output_data_path + file_name + '.xlsx'
        df.to_excel(save_path, header=False, index=False)
        print(f'saved to {save_path}')