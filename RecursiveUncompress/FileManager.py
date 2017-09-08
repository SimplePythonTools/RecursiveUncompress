import shutil
import os
import glob


class CompressedFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = file_path.split('/')[-1]
        self.file_name_no_extension = self.file_name.split('.')[0]
        # self.file_default_output_folder = file_path[0: file_path.rfind(".")]
        self.file_output_folder = file_path[0: file_path.rfind("/") + 1] + self.file_name_no_extension
        # print("file_path: " + file_path)
        # print("file_name_no_extension: " + self.file_name_no_extension)
        # print("default folder for extraction: " + self.file_default_output_folder)

    def uncompress(self, output_path, remove_source=False, clean_before_uncompress=False):
        if output_path is None:
            output_path = self.file_output_folder
        # print("Uncompress: " +  self.file_path + " to " + output_path)
        if clean_before_uncompress and os.path.exists(output_path):
            shutil.rmtree(output_path)

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        shutil.unpack_archive(self.file_path, extract_dir=output_path)

        if remove_source:
            # print("Removing "+self.file_path)
            os.remove(self.file_path)

    def recursive_uncompress(self, output_path=None, remove_source=False, remove_sub_sources=True, clean_before_uncompress = False):
        if output_path is None:
            output_path = self.file_output_folder
        else:
            self.file_output_folder = output_path

        self.uncompress(output_path=output_path, remove_source=remove_source, clean_before_uncompress=clean_before_uncompress)
        for compatible_file_format in shutil.get_unpack_formats():
            for file_format in compatible_file_format[1]:
                # print("looking for files " + file_format)
                for file in glob.glob(output_path + "/**/*" + file_format, recursive=True):
                    # print("Found file " + file)
                    CompressedFile(file).recursive_uncompress(remove_source=remove_sub_sources)

    def clean_output(self):
        if os.path.exists(self.file_output_folder):
            shutil.rmtree(self.file_output_folder)