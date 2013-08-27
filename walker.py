import os
from xattr import xattr
from sys import argv, stderr

directory = './walker'
child_was_empty = None
last_depth = None


#from https://github.com/danthedeckie/display_colors/blob/master/display_colors.py

FinderInfo = u'com.apple.FinderInfo'

colors = {'none': 0, 'gray': 2, 'green': 4, 'purple': 6, \
          'blue': 8, 'yellow': 10, 'red': 12, 'orange': 14}
names  = {0: 'none', 2: 'gray', 4: 'green', 6: 'purple', \
          8: 'blue', 10 : 'yellow', 12 : 'red', 14 : 'orange' }

blank = 32*chr(0)

def get(filename):
    attrs = xattr(filename)
    if FinderInfo in attrs:
        return names[ord(attrs.get(FinderInfo)[9])]
    else:
        return names[0]

def set(filename, color=0):
    attrs = xattr(filename)
    if FinderInfo in attrs:
        previous = attrs[FinderInfo]
    else:
        previous = blank

    new = previous[:9] + chr(colors[color]) + previous[10:]
    attrs.set(FinderInfo, new)
    return new

for root, dirs, files in reversed(list(os.walk(directory))):
    c = get(root)
    try:
        files.remove('.DS_Store')
    except ValueError:
        pass

    if (files == [] or files == None) and dirs == []: 
        child_was_empty = True
        #print "1 Would mark %s as empty" % root
        set(root, 'gray')
        last_depth = root.count('/')
        continue

    if root.count('/') < last_depth and last_depth is not None:

        if (files == [] or files == None) and child_was_empty:
            #print "2 Would mark %s as empty " % root
            #print files
            set(root, 'gray')
        else:
            child_was_empty = False
            if c == 'gray':
                set(root, 'none')

    elif last_depth is None:
        # first run, deepest sub in first folder
        if c == 'gray':
            set(root, 'none')
        last_depth = root.count('/')    	
    else: 
        #resetting walker
        if c == 'gray':
            set(root, 'none')

        last_depth = root.count('/')
        child_Was_empty = False

