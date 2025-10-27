import subprocess as sub 
import os

lp=os.path.dirname(__file__)
path=os.path.join(lp,'LP','LP_XMLConverter.exe')
# o = sub.check_output(['wine',path])
# print (o)

import subprocess

try:
    result = subprocess.run(
        ['wine',path],
        capture_output=True,
        text=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"Exit code: {e.returncode}")
    print(f"stdout: {e.stdout}")
    print(f"stderr: {e.stderr}")  # To pokaże błąd!