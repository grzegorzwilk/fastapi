import subprocess as sub 
import os

lp=os.path.dirname(__file__)
path=os.path.join(lp,'LP','LP_XMLConverter.exe')
o = sub.check_output(['wine',path])
print (o)