

```python
import pyfeko as pf
```


```python
n =  1000
f = 10
deg360 = np.linspace(0, 2*np.pi, n)
int360 = pd.Series(np.sin(deg360 * f), index=deg360)
int360.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x2a286248630>




![png](SampleCode_files/SampleCode_1_1.png)



```python
rol360 = int360.rolling_around(100, center=True)
rol360.index = deg360
rol360
pd.DataFrame({'移動平均': rol360,
		              '平均前': int360}).plot(color=('r', 'b'),
                                               style=['D--', 'D:'],
                                               fillstyle='none',
                                   				markeredgewidth=.5,
                                   				alpha=.5)

```




    <matplotlib.axes._subplots.AxesSubplot at 0x2a286a590f0>




![png](SampleCode_files/SampleCode_2_1.png)



```python
 [i for i in map(len, [deg360, int360, rol360])]

```




    [10, 10, 10]



original df


```python
a = df.copy()
a.rolling(window).mean()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-42-1062152c57bd> in <module>()
    ----> 1 a = df.copy()
          2 a.rolling(window).mean()
    

    NameError: name 'df' is not defined


normal rolling mean


```python
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>4</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6</td>
      <td>7</td>
      <td>8</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9</td>
      <td>10</td>
      <td>11</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12</td>
      <td>13</td>
      <td>14</td>
    </tr>
    <tr>
      <th>5</th>
      <td>15</td>
      <td>16</td>
      <td>17</td>
    </tr>
    <tr>
      <th>6</th>
      <td>18</td>
      <td>19</td>
      <td>20</td>
    </tr>
    <tr>
      <th>7</th>
      <td>21</td>
      <td>22</td>
      <td>23</td>
    </tr>
    <tr>
      <th>8</th>
      <td>24</td>
      <td>25</td>
      <td>26</td>
    </tr>
    <tr>
      <th>9</th>
      <td>27</td>
      <td>28</td>
      <td>29</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.rollxing_around(2, mirror=True)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-18-7f575abb952e> in <module>()
    ----> 1 df.rollxing_around(2, mirror=True)
    

    C:\tools\Anaconda3\lib\site-packages\pandas\core\generic.py in __getattr__(self, name)
       2742             if name in self._info_axis:
       2743                 return self[name]
    -> 2744             return object.__getattribute__(self, name)
       2745 
       2746     def __setattr__(self, name, value):
    

    AttributeError: 'DataFrame' object has no attribute 'rollxing_around'


around rolling mean mirror


```python
df.rolling_around(2, mirror=False)  # mirror=False省略可
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-20-3d274f76e95c> in <module>()
    ----> 1 df.rolling_around(2, mirror=False)  # mirror=False省略可
    

    E:\Users\U1and0\Dropbox\Program\python\pyfeko\pyfeko.py in rolling_around(self, window, mirror, min_periods, freq, center, win_type, on, axis, *args, **kwargs)
        283     ```
        284     """
    --> 285     df_append = df.sort_index(ascending=False) if mirror else df  # mirror=Trueであれば"降順並べ替え"
        286     df_roll = pd.concat(df_append, df, df_append, ignore_index=True)  # データをつなげる
        287     # mirror=Trueなら鏡像データ
    

    NameError: name 'df' is not defined


around rolling mean NOT mirror


```python

```
