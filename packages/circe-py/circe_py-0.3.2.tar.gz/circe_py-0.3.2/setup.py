# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circe']

package_data = \
{'': ['*'], 'circe': ['pyquic/*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.1.1,<3.0.0',
 'rich>=10.12.0,<11.0.0',
 'scanpy>=1.8.1,<2.0.0',
 'scikit-learn>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'circe-py',
    'version': '0.3.2',
    'description': 'Circe: Package for building co-accessibility networks from ATAC-seq data.',
    'long_description': '<p align="center">\n  <picture>\n    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cantinilab/circe/main/logo_dark_theme.svg" width="600">\n    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/cantinilab/circe/main/logo.svg" width="600">\n    <img alt="Circe logo" src="https://raw.githubusercontent.com/cantinilab/circe/main/logo.svg" width="600">\n  </picture>\n</p>\n\n-----------------\n# CIRCE: Cis-regulatory interactions between chromatin regions\n[![Unit_Tests](https://github.com/cantinilab/circe/actions/workflows/codecov.yaml/badge.svg)](https://github.com/cantinilab/circe/actions/workflows/codecov.yaml)\n[![codecov](https://codecov.io/gh/cantinilab/circe/graph/badge.svg?token=0OIFAP28D7)](https://codecov.io/gh/cantinilab/circe)\n[![PyPI version](https://img.shields.io/pypi/v/circe-py?color=blue)](https://img.shields.io/pypi/v/circe-py)\n[![Downloads](https://static.pepy.tech/badge/circe-py/month)](https://pepy.tech/project/circe-py)\n\n\n## Description\nThis repo contains a python package for inferring **co-accessibility networks from single-cell ATAC-seq data**, using [skggm](https://www.github.com/skggm/skggm) for the graphical lasso and [scanpy](https://www.github.com/theislab/scanpy) for data processing.\n\nIt is based on the pipeline and hypotheses presented in the manuscript "Cicero Predicts cis-Regulatory DNA Interactions from Single-Cell Chromatin Accessibility Data" by Pliner et al. (2018). This R package [Cicero](https://cole-trapnell-lab.github.io/cicero-release/) is available [here](https://www.github.com/cole-trapnell-lab/cicero-release).\n\n<br> Metacalls computation might create differences, but scores will be identical applied to the same metacalls (cf comparison plots below). It should run significantly faster than Cicero _(e.g.: running time of 5 sec instead of 17 min for the dataset 2)_.\n\n_If you have any suggestion, don\'t hesitate ! This package is still a work in progress :)_\n\n\n## Installation\nThe package can be installed using pip:\n\n```\npip install circe-py\n```\n\n and from github\n```\npip install "git+https://github.com/cantinilab/circe.git"\n```\n*Warning: If you clone the repo, don\'t stay in the repo to run your script because python will import the non-compiled cython file (probable error: circe.pyquic does not have a quic function)*\n\n## Minimal example\n```\nimport anndata as ad\nimport circe as ci\n\n# Load the data\natac = ad.read_h5ad(\'atac_data.h5ad\')\natac = ci.add_region_infos(atac)\n\n# Compute the co-accessibility network\nci.compute_atac_network(atac)\n\n# Extract the network and find CCANs modules\ncirce_network = ci.extract_atac_links(atac)\nccans_module = ci.find_ccans(atac)\n```\n### Visualisation\n```\nci.plot_connections(\n    adata,\n    chromosome="chr1",\n    start=1e7,\n    end=1.3e7\n```\n<img src="https://github.com/cantinilab/circe/raw/main/Figures/circe_figure.png" align="center"/>\n\n## Comparison to Cicero R package\n<br> *On the same metacells obtained from Cicero code.*\n\nAll tests can be found in the [circe benchmark repo](https://github.com/r-trimbour/circe_benchmark/)\n\n### Real dataset 2 - subsample of 10x PBMC (2021)\n- Pearson correlation coefficient: 0.999958\n- Spearman correlation coefficient: 0.999911\n<img src="https://github.com/cantinilab/circe/raw/main/Figures/correlation_real_dataset2.png" align="center" width="480"/>\n\nPerformance on real dataset 2:\n- Runtime: ~100x faster\n- Memory usage: ~5x less\n<img src="https://github.com/cantinilab/circe/raw/main/Figures/perf_real_dataset2.png" align="center" width="480"/>\n\n### Coming:\n\n- ~~_**Calculate metacells !**_~~\n- ~~_Add stats on similarity on large datasets._~~\n- ~~_Add stats on runtime, memory usage._~~\n- _Implement the multithreading use. Should speed up even more._\n- ~~_Fix seed for reproducibility._~~\n\n## Usage\nIt is currently developped to work with AnnData objects. Check Example1.ipynb for a simple usage example.\n\n## Citation\nTrimbour Rémi (2024). Circe: Co-accessibility network from ATAC-seq data in python (based on Cicero package). Package version 0.2.0.\n\n',
    'author': 'Rémi Trimbour',
    'author_email': 'remi.trimbour@pasteur.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
