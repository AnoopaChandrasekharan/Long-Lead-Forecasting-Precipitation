import zipfile
import os
class ZipExtractor(object):

    def __init__(self, zip_source_path, unzip_dest_path):
        self.zip_source_path = zip_source_path
        self.unzip_dest_path = unzip_dest_path
        if not os.path.exists(unzip_dest_path):
            os.makedirs(unzip_dest_path)

    def extract_zip(self):
        zip_ref = zipfile.ZipFile(self.zip_source_path, 'r')
        zip_ref.extractall(self.unzip_dest_path)
        zip_ref.close()