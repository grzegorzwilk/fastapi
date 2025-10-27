import subprocess as sub 

o = sub.check_output(['wine','--help'])
print (o)