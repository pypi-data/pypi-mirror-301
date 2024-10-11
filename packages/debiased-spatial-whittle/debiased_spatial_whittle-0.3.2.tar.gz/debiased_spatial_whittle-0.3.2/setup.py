# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['debiased_spatial_whittle', 'debiased_spatial_whittle.bayes']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'param>=2.1.1,<3.0.0',
 'progressbar2>=4.2.0,<5.0.0',
 'scipy>=1.7.3,<2.0.0']

extras_require = \
{':extra == "others"': ['autograd>=1.5,<2.0',
                        'seaborn>=0.12.2,<0.13.0',
                        'numdifftools>=0.9.41,<0.10.0'],
 'gpu': ['cupy-cuda12x>=13.0.0,<14.0.0', 'torch>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'debiased-spatial-whittle',
    'version': '0.3.2',
    'description': 'Spatial Debiased Whittle likelihood for fast inference of spatio-temporal covariance models from gridded data',
    'long_description': '# Spatial Debiased Whittle Likelihood\n\n![Image](logo.png)\n\n[![Documentation Status](https://readthedocs.org/projects/debiased-spatial-whittle/badge/?version=latest)](https://debiased-spatial-whittle.readthedocs.io/en/latest/?badge=latest)\n[![.github/workflows/run_tests_on_push.yaml](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/run_tests_on_push.yaml/badge.svg)](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/run_tests_on_push.yaml)\n[![Pypi](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/pypi.yml/badge.svg)](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/pypi.yml)\n\n## Introduction\n\nThis package implements the Spatial Debiased Whittle Likelihood (SDW) as presented in the article of the same name, by the following authors:\n\n- Arthur P. Guillaumin\n- Adam M. Sykulski\n- Sofia C. Olhede\n- Frederik J. Simons\n\nThe SDW extends ideas from the Whittle likelihood and Debiased Whittle Likelihood to random fields and spatio-temporal data. In particular, it directly addresses the bias issue of the Whittle likelihood for observation domains with dimension greater than 2. It also allows us to work with rectangular domains (i.e., rather than square), missing observations, and complex shapes of data.\n\n## Installation instructions\n\nThe package can be installed via one of the following methods. Note that in all cases, since the repository is currently private, git needs to be configured on your machine with an SSH key linking your machine to your GitHub account.\n\n1. Via the use of Poetry ([https://python-poetry.org/](https://python-poetry.org/)), by adding the following line to the dependencies listed in the `pyproject.toml` of your project:\n\n    ```toml\n    debiased-spatial-whittle = {git = "git@github.com:arthurBarthe/dbw_private.git", branch="master"}\n    ```\n\n2. Otherwise, you can directly install via pip:\n\n    ```bash\n    pip install git+https://github.com/arthurBarthe/dbw_private.git\n    ```\n\n3. Install for development - in this case, you need to clone this repo and run\n\n    ```bash\n    poetry install\n    ```\n\n    in a terminal from where you cloned the repository.\n\nIf you get an error message regarding the version of Python, install a compatible version of Python on your machine and point to it via\n\n```bash\npoetry env use <path_to_python>\n',
    'author': 'arthur',
    'author_email': 'ahw795@qmul.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://arthurpgb.pythonanywhere.com/sdw',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
