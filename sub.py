
import subprocess as s


import os

lp=os.path.dirname(__file__)
path=os.path.join(lp,'WIN','LP_XMLConverter.exe')

out = s.check_output([path])

print (out)