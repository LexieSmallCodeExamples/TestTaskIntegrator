import os
import shutil
import sys
import csv
import sqlite3
from sqlite3 import Error

id_argument = sys.argv[1]


def search_for_folder(file_name, root_folder):
    for root, sub_dirs, files in os.walk(root_folder):
        for element in sub_dirs:
            if element == file_name:
                folder_path = root_folder + "\\" + element
    return folder_path


def copy_found_tree(src_directory, dst_directory, symlinks=False, ignore=None):
    for item in os.listdir(src_directory):
        source_directory = os.path.join(src_directory, item)
        destination_directory = os.path.join(dst_directory, item)
        if os.path.isdir(source_directory):
            shutil.copy_found_tree(source_directory, destination_directory, symlinks, ignore)
        else:
            shutil.copy2(source_directory, destination_directory)


current_working_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
source_data_directory = current_working_directory + "\\Default_data_for_test_task"
csv_file_name = "\\data.csv"
csv_file_path = source_data_directory + csv_file_name

with open(csv_file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if id_argument == row[0]:
                received_file_name = row[1]

searching_folder_directory = source_data_directory + "\\data_for_integration"
found_folder_path = search_for_folder(received_file_name, searching_folder_directory)
print(found_folder_path)
path_to_create = current_working_directory + "\\result_data"
try:
    os.mkdir(path_to_create)
except OSError:
    print("Creation of the directory %s failed" % path_to_create)
else:
    print("Successfully created the directory %s " % path_to_create)

copy_found_tree(found_folder_path, path_to_create)

connectionObject = sqlite3.connect("result_files.db")
cursorObject = connectionObject.cursor()
createTable = "CREATE TABLE result_files(id int, path_to_source_data str, path_to_result_file str, size_of_result_file float)"
cursorObject.execute(createTable)

size_of_file = os.path.getsize(found_folder_path)
cursorObject.execute("INSERT INTO result_files values(?, ?, ?, ?)", (id_argument,found_folder_path, found_folder_path, size_of_file))
