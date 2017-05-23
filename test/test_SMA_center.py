import sys
sys.path.append('..')
from pyfeko import *

n = 3
df = pd.DataFrame(np.arange(n * 10).reshape(-1, n), columns=list('abc'))
window = 2

a = df.copy()
normal_rolling_mean = a.rolling(window).mean()
print('original\n', df)
print('normal rolling mean\n', normal_rolling_mean)
print('around rolling mean mirror \n', df.rolling_around(2, mirror=True))
print('around rolling mean NOT mirror\n',
      df.rolling_around(2, mirror=False))  # mirror=False省略可
