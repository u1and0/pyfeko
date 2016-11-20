
# coding: utf-8

# In[4]:

import pyfeko as pf


# In[1]:

n =  1000
f = 10
deg360 = np.linspace(0, 2*np.pi, n)
int360 = pd.Series(np.sin(deg360 * f), index=deg360)
int360.plot()


# In[9]:

rol360 = int360.rolling_around(100, center=True)
rol360.index = deg360
rol360
pd.DataFrame({'移動平均': rol360,
		              '平均前': int360}).plot(color=('r', 'b'),
                                               style=['D--', 'D:'],
                                               fillstyle='none',
                                   				markeredgewidth=.5,
                                   				alpha=.5)


# In[41]:

[i for i in map(len, [deg360, int360, rol360])]


# original df

# In[42]:

a = df.copy()
a.rolling(window).mean()


# normal rolling mean

# In[29]:

df


# In[18]:

df.rollxing_around(2, mirror=True)


# around rolling mean mirror

# In[20]:

df.rolling_around(2, mirror=False)  # mirror=False省略可


# around rolling mean NOT mirror

# In[ ]:



