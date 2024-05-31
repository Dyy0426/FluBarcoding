import _locale
import re

# Set the default locale to Chinese (Simplified) with UTF-8 encoding
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

# Open the input file 'X' in read mode
fi = open('X', 'r')
# Open the output file 'XX' in write mode
fo = open('XX', 'w')

# Initialize a counter variable
x = 1

# Read all lines from the input file, starting from the 25th line
lines = fi.readlines()[24::]

# Iterate through each line in the file
for line in lines:
    # If the line contains the word 'Region'
    if 'Region' in line:
        # Replace the line with 'XXX' followed by the counter value, and write to the output file
        fo.writelines(line.replace(line, "XXX") + " " + str(x) + "\n")
        # Increment the counter
        x = x + 1
    else:
        # If the line does not contain 'Region', write it as-is to the output file
        fo.writelines(line)

# Close the input file
fi.close()
# Close the output file
fo.close()

