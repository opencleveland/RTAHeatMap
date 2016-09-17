from os.path import dirname as directory_above
from os.path import join as join_paths
#
# Directories
src_directory = directory_above(directory_above(__file__))
data_directory = join_paths(src_directory, "data")
overhead_directory = join_paths(src_directory, "overhead")
#
# File paths
api_key_file_path = join_paths(overhead_directory, "api_key.txt")