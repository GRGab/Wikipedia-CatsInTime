import plfit
import numpy as np
import matplotlib.pyplot as plt
from time import time
plt.ion()
X = np.random.rand(1000)
myplfit = plfit.plfit(X)

plt.figure()
myplfit.plotpdf()

ti = time()
myplfit.test_pl(niter=100)
print(time() - ti, 's')