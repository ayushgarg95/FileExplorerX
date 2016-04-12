import os
import shutil
import errno


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)
######## copy one file to another folder

# srcfile = '/home/ayush/Downloads/code.py'
# dstdir = '/home/ayush/Coding/code.py'


# #assert not os.path.isabs(srcfile)

# #os.makedirs(dstdir) # create all directories, raise an error if it already exists
# shutil.copyfile(srcfile, dstdir)



# ######### copy a folder to another folder

# srcfile = '/home/ayush/Downloads/sunflower'
# dstdir = '/home/ayush/Coding/sunflower'

# if not os.path.isdir(dstdir):
# 	shutil.copytree(srcfile, dstdir)


########### move a folder

