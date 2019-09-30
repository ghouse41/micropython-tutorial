import os

basedir =  os.path.dirname(os.path.abspath(__file__))

print ("main dir", basedir)

source_dir = os.path.join(basedir,"source")

print(source_dir)