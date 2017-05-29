import sys
sys.path.append('./bin')
from runfeko import Runfeko

task = Runfeko()
print(task._main())  # Send selected files as mail
