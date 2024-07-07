import filecmp

direc1 = "/Users/baharspring/veeam/source"

direc2 = "/Users/baharspring/veeam/replica"

comp = filecmp.cmp(direc1, direc2)

print(comp)

comp_content = filecmp.cmp(direc1, direc2)
print(comp_content)
