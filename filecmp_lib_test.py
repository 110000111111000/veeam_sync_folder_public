import os
import filecmp

# Define the directories to be compared
direc1 = "/Users/baharspring/veeam/parent1"
direc2 = "/Users/baharspring/veeam/parent2"

# Perform a shallow comparison of the two directories
def compare_directories(direc1, direc2):
    comp = filecmp.dircmp(direc1, direc2)
    return comp

def print_comparison(comp, shallow=True):
    if shallow:
        print("Shallow comparison:")
    else:
        print("Deep comparison:")

    print("Common files:", comp.common_files)
    print("Files only in", direc1, ":", comp.left_only)
    print("Files only in", direc2, ":", comp.right_only)
    print("Differing files:", comp.diff_files)
    print("Files with errors:", comp.funny_files, "\n")

# Perform shallow comparison
comp = compare_directories(direc1, direc2)
print_comparison(comp)

# Perform deep comparison
comp.report_full_closure()
