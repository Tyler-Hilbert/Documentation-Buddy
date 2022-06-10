# Verifies all Python files are properly documented

import fnmatch
import os

# Prints missing documentation
# Returns number of errors
def checkPyFileForDocumentation(fileToTest):
    numErrors = 0

    # Read in file
    with open(fileToTest) as f:
        lines = f.readlines()

    # Check for comment at beginning of file
    for li in range (len(lines)):
        line = lines[li]
        if len(line.strip()) == 0:
            continue
        elif line.strip()[0] == '#' or line.strip()[0] == '"':
            break
        else:
            numErrors += 1
            print ("error:Need comment at beginning of file ", fileToTest)
            break

    # Check that all functions and classes have comments
    inMultilineComment = False
    for li in range (len(lines)):
        line = lines[li].strip()
        if '"""' in line or "'''" in line:
            inMultilineComment = not inMultilineComment

        if (not inMultilineComment) and ("def " in line[0:4] or "class " in line[0:7]):
            # Check if there is a comment
            if not (
                '#' in line or
                '#' in lines[max(0,li-1)] or
                '#' in lines[max(0,li+1)] or
                '"""' in lines[li+1] or
                "'''" in lines[li+1]
            ):
                numErrors += 1
                print ("error:missing comment in ", fileToTest, " line number ", li+1)

    return numErrors

# Read in all Python files
matches = []
numErrors = 0
for root, dirnames, filenames in os.walk('test'):
    for filename in fnmatch.filter(filenames, '*.py'):
        numErrors += checkPyFileForDocumentation(os.path.join(root, filename))
print ("Project has ", numErrors, " places missing documentation")
