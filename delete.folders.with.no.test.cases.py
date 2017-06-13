# ! /usr/bin/env/python 3.0
#
# Running this script will delete all folders that do not contain test cases
#
# 2017-02-28 smcdonagh@keywcorp.com: initial version 
#
import sys, os, re, argparse, shutil
import py_common


def remove_empty_kdm_test_case_folders(test_suite_path):
    count = 0
    test_cases = []
    lowest_dirs = []

    for root, dirs, files in os.walk(test_suite_path):

        del test_cases[:]
        count = 0

        if not dirs:

            if "kdm" in root:

                cwe_folder = root.rsplit("\\", 5)[1]

                # ensure folder is a kdm test case folder
                if cwe_folder.startswith("SFP"):

                    lowest_dirs.append(root)

                    for file in files:
                        # print("FOUND_FILES_KDM", file)
                        if not file.endswith(".h") and not file.endswith("_a.c") and not file.endswith(
                                "_a.cpp") and not file.endswith(".obj") and file.startswith("SFP"):
                            print("KDM_FILES_IN_COUNT:", root + "\\" + file)
                            count += 1

                            # todo; put all in  a list, strip end, dedup like score

                            # count = len(test_cases)
                    print("DIR:", root, "TEST CASE COUNT:", count)
                    if count == 0:
                        print("THIS FOLDER WILLL BE DELETED:", root, "COUNT:", count)
                        shutil.rmtree(root)
            else:
                print("This is not a kdm directory:", root)


def remove_empty_juliet_test_case_folders(test_suite_path):
    count = 0

    # get juliet regex
    regex = py_common.get_primary_testcase_filename_regex()
    test_cases = []
    lowest_dirs = []

    for root, dirs, files in os.walk(test_suite_path):

        del test_cases[:]
        count = 0

        if not dirs:

            if "juliet" in root:
                parent_folder = root.rsplit("\\", 2)[1]
                grand_parent_folder = root.rsplit("\\", 1)[1]

                # ensure folder is a juliet test case folder
                if parent_folder.startswith("CWE") or grand_parent_folder.startswith("CWE"):
                    lowest_dirs.append(root)
                    test_cases = py_common.find_files_in_dir(root, regex)
                    count = len(test_cases)
                    print("DIR:", root, "TEST CASE COUNT:", count)
                    if count == 0:
                        print("THIS FOLDER WILLL BE DELETED:", root, "COUNT:", count)
                        shutil.rmtree(root)
            else:
                print("This is not a Juliet directory:", root)


if __name__ == '__main__':
    py_common.print_with_timestamp("STARTED")

    parser = argparse.ArgumentParser(description='A script to remove all folders that contain no c test cases')

    parser.add_argument('suite_path',
                        help='The input path to the test case suite (can be the kdm or juliet directory or the root of those directories)')

    args = parser.parse_args()

    suite_path = args.suite_path

    full_suite_path = os.getcwd() + "\\" + suite_path

    remove_empty_juliet_test_case_folders(full_suite_path)
    remove_empty_kdm_test_case_folders(full_suite_path)

    py_common.print_with_timestamp("FINISHED")
