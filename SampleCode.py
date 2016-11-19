
# coding: utf-8

# In[23]:

import pyfeko as pf


# こあｆｄｆ
# あぢおあ
# ｓだ
# 
# 

# In[ ]:

n = 3
df = pd.DataFrame(np.arange(n * 10).reshape(-1, n), columns=list('abc'))
window = 2


# In[26]:

df


# original df

# In[14]:

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



