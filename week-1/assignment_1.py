# -*- coding: utf-8 -*-
"""Assignment-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y6DODSxXrkT472_g44tf9gbjJ3dYTU4s

Name: Sanjeev Kumar Khatri

Roll no : 23

Group : CS

Assignment : 01

## Practical Assignemnt - 1 ##
1. Getting started with Python Machine Learning Introduction to NumPy, SciPy, and Matplotlib Installing with Python
2. Chewing data efficiently with NumPy and intelligently with SciPy
3. Learning NumPy, SciPy
4. First application of machine learning
  * Reading in the data
  * Preprocessing and cleaning the data
   * Choosing the right model and learning algorithm

###1. Learning Numpy ###
"""

# importing numpy
import numpy as np 
np.version.full_version

a = np.array([0,1,2,3,4,5])
a

# for dimension and shape
a.ndim , a.shape

# converting this array into two-dimensional array
b = a.reshape((3,2))
b

b.ndim , b.shape

"""It is important to realize just how much the NumPy package is optimized. For example, doing the following avoids copies wherever possible:"""

b[1][0] = 77
b

a

"""we can say here `a[2]` has also changed

For `copy`:
"""

c = a.reshape((3,2)).copy()
c

c[0][0] = -99
c

"""Value of `a[0]` remain unchanged:"""

a

"""Multiplying a NumPy array will result in an array of the same size"""

d = np.array([1,2,3,4,5])
d*2

d**2

"""This works differently in python lists"""

[1,2,3,4,5] * 2

[1,2,3,4,5] ** 2

"""#### Indexing ####

In addition to normal list indexing, it allows you to use arrays themselves as indices by performing the following:

* One can use a list as an index itself, which will then pick the elements individually from that dimension:
"""

a[np.array([2,3,4])]

"""In normal list

"""

a[[2,3,4]]

a>4 # check with every element of an array

a[a>4] # give the element greater than 4

a[a>4] = 4 # changint the elements to 4 which are greater than 4
a

a.clip(0,4)

"""#### Handling the Nonexistent values (NAN)####"""

# lets pretend we have read this from a texxt file:
c = np.array([1,2,np.NAN , 3, 4])
c

np.isnan(c)

c[~np.isnan(c)]

np.mean(c[~np.isnan(c)])

"""#### Comparing the runtime ####

* Python lists vs Numpy 
"""

import timeit

normal_py_sec = timeit.timeit('sum(x*x for x in range(1000))', number = 10000)

naive_np_sec = timeit.timeit('sum(na * na)' , setup = "import numpy as np ; na = np.arange(1000)", number = 10000)

good_np_sec = timeit.timeit('na.dot(na)', setup = "import numpy as np ; na = np.arange(1000)" , number = 10000)


print(f"Normal python : %f sec" % normal_py_sec)
print(f"Naive Numpy : %f sec" % naive_np_sec)
print(f"Good Numpy : %f sec" % good_np_sec)

a = np.array([1,2,3])
a.dtype

np.array([1, "stringy"])

np.array([1 , "stringy" , {1,2,3}])

"""### 2. Learning Scipy ###"""

import scipy 
scipy.version.full_version

scipy.dot is np.dot

"""Reading the data """

data = np.genfromtxt("web_traffic.tsv" , delimiter = "\t")
print(data[:12])

data.shape

x = data[:,0]
y = data[:,1]

"""Checking the NAN value in x and y :"""

np.sum(np.isnan(y)) , np.sum(np.isnan(x))

x = x[~np.isnan(y)]
y = y[~np.isnan(y)]

np.sum(np.isnan(y))

"""Using `Matplotlib` to plot the scatter plot of the given data """

import matplotlib.pyplot as plt

def plot_web_traffic(x , y ,models = None , mx =  None):
  """
  Plot the web traffic (y) over time (x).
  If models is given, it is expected to be a list of fitted models,
  Which will be ploted as well
  """

  plt.figure(figsize = (12,6)) # widthe and height of the plot in inches
  plt.scatter(x , y,s =10)
  plt.title("Web traffic over the last month")

  plt.xlabel("Time")
  plt.ylabel("Hits/hour")
  plt.xticks(
      [
       w * 7 * 24 for w in range(5)
       ],
      [
       'week %i' %(w + 1) for w in range(5)
      ])
  if models:
    colors = ['g' , 'k' , 'b' , 'm' , 'r']
    linestyles = ['-' , '-.' , '--' , ':' , '-']

    
    mx =  np.linspace(0, x[-1],1000)
    for model ,style ,color in zip(models , linestyles , colors):
      plt.plot(mx ,model(mx) , linestyle = style , linewidth = 2 , c = color)
    
    plt.legend(["d = %i" %m.order for m in models], loc = "upper left")
    
    plt.autoscale(tight = True)
    plt.grid()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
plot_web_traffic(x , y)

"""For saving :



"""

plt.savefig("web_traffic.png")

"""### Choosing the right model and learning algorithm ###

We will use scipy's polynomial fiting functions
"""

fp1 = np.polyfit(x , y ,1)
fp1

print("Model parameters: %s" % fp1)

"""using squared distance as error"""

def error(f,x,y):
  return np.sum((f(x) - y) ** 2)

f1 = np.poly1d(fp1)
print(error(f1,x,y))

plot_web_traffic(x , y , [f1])

"""Lets now fit a more complex model, a polynomial of degree 2 , to see whether it better understands our data."""

f2p = np.polyfit(x , y ,2)
f2p

f2 = np.poly1d(f2p)
error(f2,x,y)

plot_web_traffic(x , y , [f1,f2])

"""Lets increase the complexity and try degree 3,10 and 100"""

f3 = np.poly1d(np.polyfit(x, y, 3))
f10 = np.poly1d(np.polyfit(x,y,10))
f100 = np.poly1d(np.polyfit(x , y , 100))

plot_web_traffic(x , y , [f1,f2 ,f3,f10 ,f100])

print("Errors for the complete data set:")
for f in [f1,f2,f3,f10,f100]:
  print("td=%i : %f" %(f.order , error(f,x,y)))

"""Out of the five fitted models, the first-order model is clearly too simple, and the models of order 10 and 53 are clearly overfitting. Only the second- and third-order models seem to somehow match the data. However, if we extrapolate them at both borders, we see them going berserk.

#### Stepping back to go forward - another look at our data ####
* finding the inflection point between weeks 3 and 4 . let's separate the data and train two lines using week 3.5 as a separation point:
"""

inflection = int(3.5 * 7 * 24) # calculate the inflection point in hours
xa = x[:inflection] # data before the inflection point
ya = y[:inflection]
xb = x[inflection:] # data after
yb = y[inflection:]

fa = np.poly1d(np.polyfit(xa,ya,1))
fb = np.poly1d(np.polyfit(xb, yb ,1))

fa_error = error(fa,xa,ya)
fb_error = error(fb,xb , yb)
print(f"Error inflection = ",(fa_error + fb_error))

"""These two lines seems to be a much better fit to the data than the previous model."""

fa = np.poly1d(np.polyfit(xa, ya, 1))
fb = np.poly1d(np.polyfit(xb, yb, 1))

plot_web_traffic(x, y, [fa, fb])