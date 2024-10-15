from .estimators import (
    entropy,
    centropy,
    mi,
    cmi,
    kldiv,
    lnc_correction,
    mi_pvalue,
    entropyd,
    midd,
    cmidd,
    centropyd,
    tcd,
    ctcd,
    corexd,
    corexdc,
    micd,
    midc,
    centropycd,
    centropydc,
    ctcdc,
    ctccd,
    corexcd,
    corexdc,
    shuffle_test,
)

# """
# # Written by Greg Ver Steeg
# # See readme.pdf for documentation
# # Or go to http://www.isi.edu/~gregv/npeet.html
#
# import warnings
#
# import numpy as np
# import numpy.linalg as la
# from numpy import log
# from scipy.special import digamma
# from sklearn.neighbors import BallTree, KDTree
#
# # CONTINUOUS ESTIMATORS
#
#
# def entropy(x, k=3, base=2):
#     """The classic K-L k-nearest neighbor continuous entropy estimator
#     x should be a list of vectors, e.g. x = [[1.3], [3.7], [5.1], [2.4]]
#     if x is a one-dimensional scalar and we have four samples
#     """
#     assert k <= len(x) - 1, "Set k smaller than num. samples - 1"
#     x = np.asarray(x)
#     n_elements, n_features = x.shape
#     x = add_noise(x)
#     tree = build_tree(x)
#     nn = query_neighbors(tree, x, k)
#     const = digamma(n_elements) - digamma(k) + n_features * log(2)
#     return (const + n_features * np.log(nn).mean()) / log(base)
#
#
# def centropy(x, y, k=3, base=2):
#     """The classic K-L k-nearest neighbor continuous entropy estimator for the
#     entropy of X conditioned on Y.
#     """
#     xy = np.c_[x, y]
#     entropy_union_xy = entropy(xy, k=k, base=base)
#     entropy_y = entropy(y, k=k, base=base)
#     return entropy_union_xy - entropy_y
#
#
# def tc(xs, k=3, base=2):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     entropy_features = [entropy(col, k=k, base=base) for col in xs_columns]
#     return np.sum(entropy_features) - entropy(xs, k, base)
#
#
# def ctc(xs, y, k=3, base=2):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     centropy_features = [centropy(col, y, k=k, base=base) for col in xs_columns]
#     return np.sum(centropy_features) - centropy(xs, y, k, base)
#
#
# def corex(xs, ys, k=3, base=2):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     cmi_features = [mi(col, ys, k=k, base=base) for col in xs_columns]
#     return np.sum(cmi_features) - mi(xs, ys, k=k, base=base)
#
#
# def mi(x, y, z=None, k=3, base=2, alpha=0):
#     """Mutual information of x and y (conditioned on z if z is not None)
#     x, y should be a list of vectors, e.g. x = [[1.3], [3.7], [5.1], [2.4]]
#     if x is a one-dimensional scalar and we have four samples
#
#     Parameters
#     ----------
#     x : array-like  (n_samples, n_features)  : Multi-dimensional array of samples
#     y : array-like  (n_samples, n_features)  : Multi-dimensional array of samples
#     z : array-like  (n_samples, n_features)  : Multi-dimensional array of samples
#     k : int  : Number of nearest neighbors to consider
#     base : int  : Base of logarithm
#     alpha : float  : Regularization parameter for LNC correction
#     """
#     assert len(x) == len(y), "Arrays should have same length"
#     assert k <= len(x) - 1, "Set k smaller than num. samples - 1"
#     x, y = np.asarray(x), np.asarray(y)
#     x, y = x.reshape(x.shape[0], -1), y.reshape(y.shape[0], -1)
#     x = add_noise(x)
#     y = add_noise(y)
#     points = [x, y]
#     if z is not None:
#         z = np.asarray(z)
#         z = z.reshape(z.shape[0], -1)
#         points.append(z)
#     points = np.hstack(points)
#     # Find nearest neighbors in joint space, p=inf means max-norm
#     tree = build_tree(points)
#     dvec = query_neighbors(tree, points, k)
#     if z is None:
#         a, b, c, d = (
#             avgdigamma(x, dvec),
#             avgdigamma(y, dvec),
#             digamma(k),
#             digamma(len(x)),
#         )
#         if alpha > 0:
#             d += lnc_correction(tree, points, k, alpha)
#     else:
#         xz = np.c_[x, z]
#         yz = np.c_[y, z]
#         a, b, c, d = (
#             avgdigamma(xz, dvec),
#             avgdigamma(yz, dvec),
#             avgdigamma(z, dvec),
#             digamma(k),
#         )
#     return (-a - b + c + d) / log(base)
#
#
# def mi_pvalue(
#     x,
#     y,
#     z=None,
#     mi_type="mi",
#     k=3,
#     base=2,
#     n_permutations=1000,
#     random_state=None,
#     warning=True,
# ):
#     """
#     Compute the mutual information between x and y, and estimate the p-value
#     under the null hypothesis of independence using permutation testing.
#     You can select which mutual information function to use: 'mi', 'midd', or 'micd'.
#
#     Parameters
#     ----------
#     x : array-like, shape (n_samples,)
#         First variable.
#     y : array-like, shape (n_samples,)
#         Second variable.
#     z : array-like, shape (n_samples,), optional
#         Conditioning variable(s) for conditional mutual information.
#     mi_type : str, default='mi'
#         Type of mutual information function to use:
#         - 'mi'   : Use for continuous variables.
#         - 'midd' : Use for discrete variables.
#         - 'micd' : Use when x is continuous and y is discrete.
#     k : int, default=3
#         Number of nearest neighbors for density estimation (used in 'mi' and 'micd').
#     base : float, default=2
#         Log base for entropy calculations.
#     n_permutations : int, default=1000
#         Number of permutations for the permutation test.
#     random_state : int or None, default=None
#         Seed for random number generator.
#     warning : bool, default=True
#         Whether to show warnings when insufficient data after conditioning.
#
#     Returns
#     -------
#     mi_observed : float
#         Observed mutual information between x and y.
#     p_value : float
#         Estimated p-value under the null hypothesis of independence.
#     mi_permutations : ndarray, shape (n_permutations,)
#         MI values from the permutation distribution.
#     """
#     np.random.seed(random_state)
#
#     # Select the appropriate mutual information function
#     if mi_type == "mi":
#         mi_func = mi
#         mi_kwargs = {"k": k, "base": base}
#     elif mi_type == "midd":
#         mi_func = midd
#         mi_kwargs = {"base": base}
#     elif mi_type == "micd":
#         mi_func = micd
#         mi_kwargs = {"k": k, "base": base, "warning": warning}
#     else:
#         raise ValueError("Invalid mi_type. Options are 'mi', 'midd', or 'micd'.")
#
#     # Compute the observed mutual information
#     mi_observed = mi_func(x, y, z=z, **mi_kwargs)
#
#     # Initialize the array to store MI values from permutations
#     mi_permutations = np.zeros(n_permutations)
#
#     # Perform permutation testing
#     for i in range(n_permutations):
#         y_permuted = np.random.permutation(y)
#         mi_perm = mi_func(x, y_permuted, z=z, **mi_kwargs)
#         mi_permutations[i] = mi_perm
#
#     # Compute the p-value
#     p_value = np.mean(mi_permutations >= mi_observed)
#
#     return mi_observed, p_value, mi_permutations
#
#
# def cmi(x, y, z, k=3, base=2):
#     """Mutual information of x and y, conditioned on z
#     Legacy function. Use mi(x, y, z) directly.
#     """
#     return mi(x, y, z=z, k=k, base=base)
#
#
# def kldiv(x, xp, k=3, base=2):
#     """KL Divergence between p and q for x~p(x), xp~q(x)
#     x, xp should be a list of vectors, e.g. x = [[1.3], [3.7], [5.1], [2.4]]
#     if x is a one-dimensional scalar and we have four samples
#     """
#     assert k < min(len(x), len(xp)), "Set k smaller than num. samples - 1"
#     assert len(x[0]) == len(xp[0]), "Two distributions must have same dim."
#     x, xp = np.asarray(x), np.asarray(xp)
#     x, xp = x.reshape(x.shape[0], -1), xp.reshape(xp.shape[0], -1)
#     d = len(x[0])
#     n = len(x)
#     m = len(xp)
#     const = log(m) - log(n - 1)
#     tree = build_tree(x)
#     treep = build_tree(xp)
#     nn = query_neighbors(tree, x, k)
#     nnp = query_neighbors(treep, x, k - 1)
#     return (const + d * (np.log(nnp).mean() - np.log(nn).mean())) / log(base)
#
#
# def lnc_correction(tree, points, k, alpha):
#     """
#     Local Non-uniformity Correction. This function is used to correct the bias in mutual information estimation,
#     which is caused by the non-uniformity of the local neighborhood of each point. The correction term is calculated
#     by comparing the volume of the PCA-bounding box and the volume of the original box. If the volume of the PCA-bounding
#     box is smaller than the volume of the original box, the correction term is added to the mutual information estimate.
#
#     :param tree:  BallTree or KDTree object
#     :param points:  array-like  (n_samples, n_features)  : Multi-dimensional array of samples
#     :param k:   int  : Number of nearest neighbors to consider
#     :param alpha:  float  : Regularization parameter for LNC correction
#     :return:
#     """
#     e = 0
#     n_sample = points.shape[0]
#     for point in points:
#         # Find k-nearest neighbors in joint space, p=inf means max norm
#         knn = tree.query(point[None, :], k=k + 1, return_distance=False)[0]
#         knn_points = points[knn]
#         # Substract mean of k-nearest neighbor points
#         knn_points = knn_points - knn_points[0]
#         # Calculate covariance matrix of k-nearest neighbor points, obtain eigen vectors
#         covr = knn_points.T @ knn_points / k
#         _, v = la.eig(covr)
#         # Calculate PCA-bounding box using eigen vectors
#         V_rect = np.log(np.abs(knn_points @ v).max(axis=0)).sum()
#         # Calculate the volume of original box
#         log_knn_dist = np.log(np.abs(knn_points).max(axis=0)).sum()
#
#         # Perform local non-uniformity checking and update correction term
#         if V_rect < log_knn_dist + np.log(alpha):
#             e += (log_knn_dist - V_rect) / n_sample
#     return e
#
#
# # DISCRETE ESTIMATORS
# def entropyd(sx, base=2):
#     """Discrete entropy estimator
#     sx is a list of samples
#     """
#     unique, count = np.unique(sx, return_counts=True, axis=0)
#     # Convert to float as otherwise integer division results in all 0 for proba.
#     proba = count.astype(float) / len(sx)
#     # Avoid 0 division; remove probabilities == 0.0 (removing them does not change the entropy estimate as 0 * log(1/0) = 0.
#     proba = proba[proba > 0.0]
#     return np.sum(proba * np.log(1.0 / proba)) / log(base)
#
#
# def midd(x, y, z=None, base=2):
#     """Discrete mutual information estimator.
#     Computes I(X; Y) or I(X; Y | Z) if z is provided.
#
#     Parameters
#     ----------
#     x : array-like
#         Discrete variable X.
#     y : array-like
#         Discrete variable Y.
#     z : array-like, optional
#         Discrete conditioning variable Z.
#     base : float, default=2
#         Logarithm base.
#
#     Returns
#     -------
#     mi_value : float
#         Mutual information I(X; Y) or conditional mutual information I(X; Y | Z).
#     """
#     assert len(x) == len(y), "Arrays should have same length"
#     if z is None:
#         # Mutual information I(X; Y)
#         return entropyd(x, base) - centropyd(x, y, base)
#     else:
#         # Conditional mutual information I(X; Y | Z)
#         assert len(x) == len(z), "Arrays should have same length"
#         xz = np.c_[x, z]
#         yz = np.c_[y, z]
#         xyz = np.c_[x, y, z]
#         h_xz = entropyd(xz, base)
#         h_yz = entropyd(yz, base)
#         h_xyz = entropyd(xyz, base)
#         h_z = entropyd(z, base)
#         cmi = h_xz + h_yz - h_xyz - h_z
#         return cmi
#
#
# def cmidd(x, y, z, base=2):
#     """Discrete mutual information estimator
#     Given a list of samples which can be any hashable object
#     """
#     assert len(x) == len(y) == len(z), "Arrays should have same length"
#     xz = np.c_[x, z]
#     yz = np.c_[y, z]
#     xyz = np.c_[x, y, z]
#     return (
#         entropyd(xz, base)
#         + entropyd(yz, base)
#         - entropyd(xyz, base)
#         - entropyd(z, base)
#     )
#
#
# def centropyd(x, y, base=2):
#     """The classic K-L k-nearest neighbor continuous entropy estimator for the
#     entropy of X conditioned on Y.
#     """
#     xy = np.c_[x, y]
#     return entropyd(xy, base) - entropyd(y, base)
#
#
# def tcd(xs, base=2):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     entropy_features = [entropyd(col, base=base) for col in xs_columns]
#     return np.sum(entropy_features) - entropyd(xs, base)
#
#
# def ctcd(xs, y, base=2):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     centropy_features = [centropyd(col, y, base=base) for col in xs_columns]
#     return np.sum(centropy_features) - centropyd(xs, y, base)
#
#
# def corexd(xs, ys, base=2):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     cmi_features = [midd(col, ys, base=base) for col in xs_columns]
#     return np.sum(cmi_features) - midd(xs, ys, base=base)
#
#
# # MIXED ESTIMATORS
# def micd(x, y, z=None, k=3, base=2, warning=True):
#     """Mutual information estimator where x is continuous and y is discrete.
#     Computes I(X; Y) or I(X; Y | Z) if z is provided.
#
#     Parameters
#     ----------
#     x : array-like, shape (n_samples,)
#         Continuous variable X.
#     y : array-like, shape (n_samples,)
#         Discrete variable Y.
#     z : array-like, shape (n_samples,), optional
#         Discrete conditioning variable Z.
#     k : int, default=3
#         Number of nearest neighbors for entropy estimation.
#     base : float, default=2
#         Logarithm base.
#     warning : bool, default=True
#         Whether to show warnings when insufficient data after conditioning.
#
#     Returns
#     -------
#     mi_value : float
#         Mutual information I(X; Y) or conditional mutual information I(X; Y | Z).
#     """
#     assert len(x) == len(y), "Arrays should have same length"
#     x = np.asarray(x)
#     if z is None:
#         # Mutual information I(X; Y)
#         entropy_x = entropy(x, k, base)
#         y_unique, y_count = np.unique(y, return_counts=True, axis=0)
#         y_proba = y_count / len(y)
#         entropy_x_given_y = 0.0
#         for yval, py in zip(y_unique, y_proba):
#             idx = (y == yval).all(axis=1)
#             x_given_y = x[idx]
#             if len(x_given_y) >= k + 1:
#                 entropy_x_y = entropy(x_given_y, k, base)
#             else:
#                 if warning:
#                     warnings.warn(
#                         f"Warning, after conditioning on y={yval}, insufficient data. "
#                         "Assuming maximal entropy."
#                     )
#                 entropy_x_y = entropy_x
#             entropy_x_given_y += py * entropy_x_y
#         mi_value = entropy_x - entropy_x_given_y
#         return abs(mi_value)
#     else:
#         # Conditional mutual information I(X; Y | Z)
#         assert len(x) == len(z), "Arrays should have same length"
#         z = np.asarray(z)
#         z_unique, z_count = np.unique(z, return_counts=True, axis=0)
#         z_proba = z_count / len(z)
#         entropy_x_given_z = 0.0
#         entropy_x_given_yz = 0.0
#         entropy_x = entropy(x, k, base)
#         for zval, pz in zip(z_unique, z_proba):
#             idx_z = (z == zval).all(axis=1)
#             x_given_z = x[idx_z]
#             y_given_z = y[idx_z]
#             if len(x_given_z) >= k + 1:
#                 entropy_x_z = entropy(x_given_z, k, base)
#             else:
#                 if warning:
#                     warnings.warn(
#                         f"Warning, after conditioning on z={zval}, insufficient data. "
#                         "Assuming maximal entropy."
#                     )
#                 entropy_x_z = entropy_x
#             entropy_x_given_z += pz * entropy_x_z
#             y_unique_given_z, y_count_given_z = np.unique(
#                 y_given_z, return_counts=True, axis=0
#             )
#             y_proba_given_z = y_count_given_z / y_count_given_z.sum()
#             for yval, pyz in zip(y_unique_given_z, y_proba_given_z):
#                 idx_yz = idx_z & (y == yval).all(axis=1)
#                 x_given_yz = x[idx_yz]
#                 p_yz = pyz * pz  # Joint probability P(Y = y, Z = z)
#                 if len(x_given_yz) >= k + 1:
#                     entropy_x_yz = entropy(x_given_yz, k, base)
#                 else:
#                     if warning:
#                         warnings.warn(
#                             f"Warning, after conditioning on y={yval}, z={zval}, insufficient data. "
#                             "Assuming maximal entropy."
#                         )
#                     entropy_x_yz = entropy_x
#                 entropy_x_given_yz += p_yz * entropy_x_yz
#         cmi_value = entropy_x_given_z - entropy_x_given_yz
#         return abs(cmi_value)
#
#
# def midc(x, y, k=3, base=2, warning=True):
#     return micd(y, x, k, base, warning)
#
#
# def centropycd(x, y, k=3, base=2, warning=True):
#     return entropy(x, base) - micd(x, y, k=k, base=base, warning=warning)
#
#
# def centropydc(x, y, k=3, base=2, warning=True):
#     return centropycd(y, x, k=k, base=base, warning=warning)
#
#
# def ctcdc(xs, y, k=3, base=2, warning=True):
#     xs_columns = np.expand_dims(xs, axis=0).T
#     centropy_features = [
#         centropydc(col, y, k=k, base=base, warning=warning) for col in xs_columns
#     ]
#     return np.sum(centropy_features) - centropydc(xs, y, k, base, warning)
#
#
# def ctccd(xs, y, k=3, base=2, warning=True):
#     return ctcdc(y, xs, k=k, base=base, warning=warning)
#
#
# def corexcd(xs, ys, k=3, base=2, warning=True):
#     return corexdc(ys, xs, k=k, base=base, warning=warning)
#
#
# def corexdc(xs, ys, k=3, base=2, warning=True):
#     return tcd(xs, base) - ctcdc(xs, ys, k, base, warning)
#
#
# # UTILITY FUNCTIONS
#
#
# def add_noise(x, intens=1e-10):
#     # small noise to break degeneracy, see doc.
#     return x + intens * np.random.random_sample(x.shape)
#
#
# def query_neighbors(tree, x, k):
#     return tree.query(x, k=k + 1)[0][:, k]
#
#
# def count_neighbors(tree, x, r):
#     return tree.query_radius(x, r, count_only=True)
#
#
# def avgdigamma(points, dvec):
#     # This part finds number of neighbors in some radius in the marginal space
#     # returns expectation value of <psi(nx)>
#     tree = build_tree(points)
#     dvec = dvec - 1e-15
#     num_points = count_neighbors(tree, points, dvec)
#     return np.mean(digamma(num_points))
#
#
# def build_tree(points):
#     if points.shape[1] >= 20:
#         return BallTree(points, metric="chebyshev")
#     return KDTree(points, metric="chebyshev")
#
#
# # TESTS
#
#
# def shuffle_test(measure, x, y, z=False, ns=200, ci=0.95, **kwargs):
#     """Shuffle test
#     Repeatedly shuffle the x-values and then estimate measure(x, y, [z]).
#     Returns the mean and conf. interval ('ci=0.95' default) over 'ns' runs.
#     'measure' could me mi, cmi, e.g. Keyword arguments can be passed.
#     Mutual information and CMI should have a mean near zero.
#     """
#     x_clone = np.copy(x)  # A copy that we can shuffle
#     outputs = []
#     for i in range(ns):
#         np.random.shuffle(x_clone)
#         if z:
#             outputs.append(measure(x_clone, y, z, **kwargs))
#         else:
#             outputs.append(measure(x_clone, y, **kwargs))
#     outputs.sort()
#     return np.mean(outputs), (
#         outputs[int((1.0 - ci) / 2 * ns)],
#         outputs[int((1.0 + ci) / 2 * ns)],
#     )
#
#
# if __name__ == "__main__":
#     print("MI between two independent continuous random variables X and Y:")
#     np.random.seed(0)
#     x = np.random.randn(1000, 10)
#     y = np.random.randn(1000, 3)
#     print(mi(x, y, base=2, alpha=0))
#
#     print("Estimating MI and p-value between two independent random variables X and Y:")
#     np.random.seed(42)
#     n_samples = 500
#     x = np.random.randn(n_samples, 1)
#     y = np.random.randn(n_samples, 1)
#     mi_observed, p_value, mi_permutations = mi_pvalue(x, y, k=3, n_permutations=1000)
#     print(f"Observed MI: {mi_observed}")
#     print(f"P-value: {p_value}")
#
#     print("\nEstimating MI and p-value between dependent random variables X and Y:")
#     y_dependent = x + 0.5 * np.random.randn(n_samples, 1)
#     mi_observed_dep, p_value_dep, _ = mi_pvalue(
#         x, y_dependent, k=3, n_permutations=1000
#     )
#     print(f"Observed MI: {mi_observed_dep}")
#     print(f"P-value: {p_value_dep}")
#
#
# """
