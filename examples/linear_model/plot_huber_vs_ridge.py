"""
=======================================================
HuberRegressor vs Ridge on dataset with strong outliers
=======================================================

Fit Ridge and HuberRegressor on a dataset with outliers.

The example shows that the coefficients in ridge are strongly influenced
by the outliers are added to the dataset. The huber regressor is less
influenced by the outliers since the model fits the linear loss
for these. As the parameter epsilon is increased for the huber regressor, the
decision function approches that of the ridge.
"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor, Ridge

# Generate toy data.
rng = np.random.RandomState(0)
X, y = make_regression(n_samples=20, n_features=1, random_state=0, noise=4.0, bias=100.0)

# Add four strong outliers to the dataset.
X_outliers = rng.normal(0, 0.5, size=(4, 1))
y_outliers = rng.normal(0, 2.0, size=4)
X_outliers[:2, :] += X.max() + X.mean() / 4 
X_outliers[2:, :] += X.min() - X.mean() / 4
y_outliers[:2] += y.min() - y.mean() / 4
y_outliers[2:] += y.max() + y.mean() / 4
X = np.vstack((X, X_outliers))
y = np.concatenate((y, y_outliers))
plt.plot(X, y, 'b.')

# Fit the huber regressor over a series of epsilon values.
colors = ['r-', 'b-', 'y-', 'm-']
x = np.linspace(X.min(), X.max())
epsilon_values = [1.35, 1.5, 1.75, 3.0]
for color_ind, epsilon in enumerate(epsilon_values):
    huber = HuberRegressor(fit_intercept=True, alpha=0.0, n_iter=100, copy=True, epsilon=epsilon)
    huber.fit(X, y)
    coef_ = huber.coef_ * x + huber.intercept_
    plt.plot(x, coef_, colors[color_ind], label="huber loss, %s" % epsilon)

# Fit a ridge regressor to compare it to huber regressor.
ridge = Ridge(fit_intercept=True, alpha=0.0, random_state=0, normalize=True)
ridge.fit(X, y)
coef_ridge = ridge.coef_
coef_ = ridge.coef_ * x + ridge.intercept_
plt.plot(x, coef_, 'g-', label="ridge regression")

plt.axhline(y.mean(), color='black')
plt.axvline(X.mean(), color='black')

plt.title("Comparison of HuberRegressor vs Ridge")
plt.xlabel("X")
plt.ylabel("y")
plt.legend(loc=0, )
plt.show()
