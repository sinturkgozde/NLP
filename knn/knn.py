
# coding: utf-8

# In[8]:

import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from itertools import product
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier


# In[9]:

data = pd.read_csv("processed.switzerland.data")
testdata=pd.read_csv("processed.cleveland.data")


# In[10]:


neigh = KNeighborsClassifier()
a= np.array(data["age"])
a1 = a.reshape(a.size,1)
b = np.array(data["13"])
a2= np.array(data[["age","1","4"]])


testdata= np.array(data[["age","1","4"]])

testdata_results= np.array(data["13"])


neigh.fit(a2,b)
predictions_result= neigh.predict(testdata)

plt.scatter(data["1"],data["age"])
plt.show()


# In[ ]:



