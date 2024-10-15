# npeet_plus

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fork from [NPEET (Non-Parametric Entropy Estimation Toolbox)](https://github.com/gregversteeg/NPEET) with additional features and improvements for mutual information and entropy estimation. The package provides methods for estimating mutual information, conditional mutual information, KL divergence, and related quantities for both continuous and discrete data.

## Features

This package builds on top of the original NPEET by adding new features such as:

- **p-value computation** for mutual information using permutation testing (`mi_pvalue`).
- **Confidence interval estimation** for mutual information using bootstrapping (`mi_confidence_interval`).
- Extended functionality for conditional mutual information in the `midd` (discrete mutual information) and `micd` (mixed mutual information) functions.

## Installation

You can install `npeet_plus` via PyPI:

```bash
pip install npeet_plus
```

## Usage

### Importing the package

```python
import numpy as np
from npeet_plus import mi, mi_pvalue, mi_confidence_interval
```

### Mutual Information Example

Compute the mutual information between two variables `x` and `y`:

```python
x = np.random.randn(1000, 1)
y = x + 0.5 * np.random.randn(1000, 1)

mi_value = mi(x, y)
print(f"Mutual Information: {mi_value}")
```

### Compute p-value for Mutual Information

The function `mi_pvalue` computes the observed mutual information and estimates the p-value under the null hypothesis of independence using permutation testing:

```python
mi_observed, p_value = mi_pvalue(x, y, k=3, n_permutations=1000)
print(f"Observed MI: {mi_observed}, P-value: {p_value}")
```

### Compute Confidence Interval for Mutual Information

The function `mi_confidence_interval` computes the observed mutual information and estimates the confidence interval using bootstrapping:

```python
mi_observed, ci_lower, ci_upper, mi_bootstrap = mi_confidence_interval(
    x, y, n_bootstraps=1000, confidence_level=0.95
)
print(f"Observed MI: {mi_observed}")
print(f"95% Confidence Interval: [{ci_lower}, {ci_upper}]")
```

## Functions

### `entropy(x, k=3, base=2)`

Estimate the entropy of a continuous variable `x` using k-nearest neighbors.

- **Parameters**:
  - `x`: array-like, the variable of interest.
  - `k`: number of nearest neighbors.
  - `base`: logarithm base (default is 2).
  
- **Returns**: entropy estimate.

### `mi(x, y, z=None, k=3, base=2, alpha=0)`

Estimate the mutual information between `x` and `y` using k-nearest neighbors. Optionally, you can condition on `z`.

- **Parameters**:
  - `x`, `y`: array-like, variables for mutual information computation.
  - `z`: optional, array-like, conditional variable for conditional MI.
  - `k`: number of nearest neighbors.
  - `base`: logarithm base (default is 2).
  - `alpha`: regularization parameter for LNC correction (default is 0).
  
- **Returns**: mutual information estimate.

### `mi_pvalue(x, y, z=None, mi_type="mi", k=3, base=2, n_permutations=1000, random_state=None, warning=True)`

Estimate the p-value of mutual information between `x` and `y` under the null hypothesis of independence using permutation testing.

- **Parameters**:
  - `x`, `y`: array-like, variables for mutual information computation.
  - `z`: optional, array-like, conditional variable for conditional MI.
  - `mi_type`: type of mutual information to use (`"mi"` for continuous, `"midd"` for discrete, `"micd"` for mixed).
  - `k`: number of nearest neighbors.
  - `base`: logarithm base (default is 2).
  - `n_permutations`: number of permutations to estimate p-value (default is 1000).
  - `random_state`: seed for random number generator.
  - `warning`: whether to show warnings for insufficient data (default is `True`).

- **Returns**: observed mutual information, p-value.

### `mi_confidence_interval(x, y, z=None, mi_type="mi", k=3, base=2, n_bootstraps=1000, confidence_level=0.95, random_state=None, warning=True)`

Estimate the confidence interval for mutual information between `x` and `y` using bootstrapping.

- **Parameters**:
  - `x`, `y`: array-like, variables for mutual information computation.
  - `z`: optional, array-like, conditional variable for conditional MI.
  - `mi_type`: type of mutual information to use (`"mi"` for continuous, `"midd"` for discrete, `"micd"` for mixed).
  - `k`: number of nearest neighbors.
  - `base`: logarithm base (default is 2).
  - `n_bootstraps`: number of bootstraps to estimate the confidence interval (default is 1000).
  - `confidence_level`: confidence level for the interval (default is 0.95).
  - `random_state`: seed for random number generator.
  - `warning`: whether to show warnings for insufficient data (default is `True`).

- **Returns**: observed mutual information, lower bound of CI, upper bound of CI, bootstrap MI values.

## Modifications from the Original NPEET

- **New functions added**:
  - `mi_pvalue`: Compute the p-value of mutual information using permutation testing.
  - `mi_confidence_interval`: Compute the confidence interval of mutual information using bootstrapping.
  
- **Enhancements**:
  - Added conditional mutual information computation for both `midd` and `micd` functions, enabling more accurate estimations for discrete and mixed data.

## Dependencies

- `numpy>=1.18.0`
- `scipy>=1.4.0`
- `scikit-learn>=0.22.0`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

## Acknowledgments

- Original codebase: [Greg Ver Steeg](https://github.com/gregversteeg/NPEET)
- Author of the original NPEET toolbox: Greg Ver Steeg
- Author of modifications: Albert Buchard
