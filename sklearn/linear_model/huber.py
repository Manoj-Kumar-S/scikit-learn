import numpy as np

from scipy import optimize

from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model.base import center_data
from sklearn.utils import check_X_y

def _huber_loss_and_gradient(w, X, y, epsilon, alpha):

    linear_loss = y - np.dot(X, w)
    abs_linear_loss = np.abs(linear_loss)
    outliers_true = abs_linear_loss > epsilon
    n_outliers = np.count_nonzero(outliers_true)
    outliers = linear_loss[outliers_true]
    outlier_loss = epsilon * np.sum(outliers) - n_outliers * 0.5 * epsilon**2
    non_outliers = linear_loss[~outliers_true]
    loss = 0.5 * np.dot(non_outliers, non_outliers) + outlier_loss

    # Calulate the gradient
    grad = np.dot(non_outliers, -X[~outliers_true, :])
    outliers_true_pos = np.logical_and(linear_loss >= 0, outliers_true)
    outliers_true_neg = np.logical_and(linear_loss < 0, outliers_true)
    grad -= epsilon * X[outliers_true_pos, :].sum(axis=0)
    grad += epsilon * X[outliers_true_neg, :].sum(axis=0)
    grad += alpha * 2 * w
    return loss + alpha * np.dot(w, w), grad


class HuberRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, epsilon=0.1, n_iter=100, alpha=0.0001, warm_start=False):
        self.epsilon = epsilon
        self.n_iter = n_iter
        self.alpha = alpha
        self.warm_start = warm_start

    def fit(self, X, y):
        X, y = check_X_y(X, y)

        coef = getattr(self, 'coef', None)
        if not self.warm_start or (self.warm_start and coef is None):
            self.coef_ = np.zeros(X.shape[1])
        self.coef, f, _ = optimize.fmin_l_bfgs_b(
            _huber_loss_and_gradient, self.coef_,
        	args=(X, y, self.epsilon, self.alpha), maxiter=self.n_iter)
        self.loss_ = f
        return self
