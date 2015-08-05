import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt 
import random
                
def normal():
    font = {'family' : 'serif',
            'color'  : 'darkred',
            'weight' : 'normal',
            'size'   : 16,
            }

    x = np.arange(0.0, 4, 0.01)
    y = np.cos(2 * np.pi * x) * np.exp(-x)
    p1,=plt.plot(x, y, 'k')

    y=[np.sqrt(y) for y in x]
    p2,=plt.plot(x,y,'b')

    x = np.arange(0.0, 2, 0.01)
    y=[y*y for y in x]
    p3,=plt.plot(x,y,'r')

    plt.legend([p1,p2,p3],["cos","x^2","x"],loc=2)


    plt.title('Damped exponential decay', fontdict=font)
    plt.text(2, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict=font)
    plt.xlabel('time (s)', fontdict=font)
    plt.ylabel('voltage (mV)', fontdict=font)
    plt.grid(True)
    plt.axis('equal')
 
    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)

    plt.show()

def bar():
    
    import pylab as pl
    b1 = pl.bar([0, 1, 2], [0.2, 0.3, 0.1], width=0.4, align="center")
    pl.legend([b1], ["Bar 1"])
    pl.show()

def hist():
    """
    Demo of the histogram (hist) function with a few features.
    In addition to the basic histogram, this demo shows a few optional features:

    * Setting the number of data bins
    * The ``normed`` flag, which normalizes bin heights so that the integral of
        the histogram is 1. The resulting histogram is a probability density.
    * Setting the face color of the bars
    * Setting the opacity (alpha value)."""

    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    # example data
    mu = 100 # mean of distribution
    sigma = 15 # standard deviation of distribution
    x = mu + sigma * np.random.randn(10000)

    num_bins = 50
    # the histogram of the data
    n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
    #add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--')
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.show()

def binomail(n=20,p=0.5):
    p = 0.1
    n=2000
    x = np.arange(n)
    y = stats.binom.pmf(x,n,p)
    print y

    x1=[]
    y1=[]
    for each in x:
        if y[each]>0.001:
            x1.append(each)
            y1.append(y[each])

    pl.bar(x1, y1,width=0.4, align="center")
    
    pl.xlabel("Number")
    pl.ylabel("Probability")    
    pl.title("n={0} p={1}".format(n,p))

    pl.legend()
    pl.grid(True)
    #pl.savefig("n={0} p={1}.png".format(n,p))
    pl.show()

def sca():
    plt.figure(figsize=(8,4))
    plt.plot(range(5))
    plt.show()

if __name__ == '__main__':
    sca()
