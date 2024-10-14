# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entropy_pooling']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.10,<2.0']

setup_kwargs = {
    'name': 'entropy-pooling',
    'version': '1.0.8',
    'description': 'Entropy Pooling in Python with a BSD 3-Clause license.',
    'long_description': '[![pytest](https://github.com/fortitudo-tech/entropy-pooling/actions/workflows/tests.yml/badge.svg)](https://github.com/fortitudo-tech/entropy-pooling/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/fortitudo-tech/entropy-pooling/graph/badge.svg?token=XGIQ78ZLDN)](https://codecov.io/gh/fortitudo-tech/entropy-pooling)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fortitudo-tech/entropy-pooling/HEAD?labpath=examples)\n\nEntropy Pooling in Python\n=========================\n\nDue to popular demand from developers, this package contains the Entropy Pooling\nimplementation from the [fortitudo.tech Python package](https://github.com/fortitudo-tech/fortitudo.tech)\nwith a more permissive BSD 3-Clause license.\n\nThis package contains only one function called ep and has minimal dependencies\nwith just scipy. See [the examples](https://github.com/fortitudo-tech/entropy-pooling/tree/main/examples)\nfor how you can import and use the ep function.\n\nYou can explore the examples without local installations using\n[Binder](https://mybinder.org/v2/gh/fortitudo-tech/entropy-pooling/HEAD?labpath=examples).\n\nInstallation instructions\n-------------------------\n\nInstallation can be done via pip:\n\n    pip install entropy-pooling\n\nTheory\n------\nEntropy Pooling is a powerful method for implementing subjective views and\nperforming stress-tests for fully general Monte Carlo distributions. It was first\nintroduced by [Meucci (2008)](https://ssrn.com/abstract=1213325) and refined\nwith sequential algorithms by [Vorobets (2021)](https://ssrn.com/abstract=3936392).\n\n[You can loosely think about Entropy Pooling as a generalization of the Black-Litterman model](https://antonvorobets.substack.com/p/entropy-pooling-vs-black-litterman-abb608b810cd) without all the oversimplifying assumptions. Entropy Pooling operates directly on \n[the next generation market representation](https://youtu.be/4ESigySdGf8?si=yWYuP9te1K1RBU7j&t=46)\ndefined by the simulation matrix $R\\in \\mathbb{R}^{S\\times I}$ and associated joint\nscenario probability vector $p\\in \\mathbb{R}^{S}$.\n\nFor a quick introduction to Entropy Pooling intuition, watch [this YouTube video](https://youtu.be/qk_5l4ICXfY).\nFor a collection of Entropy Pooling resources, see this [Substack post](https://antonvorobets.substack.com/p/entropy-pooling-collection).\n\nThe original Entropy Pooling approach solves the minimum relative entropy problem\n\n$$q=\\underset{x}{\\text{argmin}}\\lbrace x^{T}\\left(\\ln x-\\ln p\\right)\\rbrace$$\n\nsubject to linear constraints on the posterior probabilities\n\n$$Gx\\leq h \\quad \\text{and} \\quad Ax=b.$$\n\nThe constraints matrices $A$ and $G$ contain functions of the Monte Carlo\nsimulation $R$ that allow you to implement subjective views and stress-tests by\nchanging the joint scenario probabilities from a prior probability vector $p$\nto a posterior probability vector $q$.\n\nA useful statistic when working with Entropy Pooling is the effective number of\nscenarios introduced by [Meucci (2012)](https://ssrn.com/abstract=1971808).\n\nFor a causal Bayesian network overlay on top of Entropy Pooling, see\n[Vorobets (2023)](https://ssrn.com/abstract=4444291).\n\nVideo walkthroughs\n------------------\n\nVideo walkthroughs of the two notebook examples are available [here](https://youtu.be/hDt103zEML8)\nand [here](https://youtu.be/DK1Pv5tuLgo). The videos give additional insights into\nEntropy Pooling theory and its sequential refinements. It is highly recommended\nto watch these videos to quickly increase your understanding.\n\nPortfolio Construction and Risk Management Book\n-----------------------------------------------\n\nEntropy Pooling is a core part of the next generation investment framework that\nalso utilizes fully general Monte Carlo distributions and CVaR analysis, see\n[this YouTube video](https://youtu.be/4ESigySdGf8?si) for an introduction. To\nget a pedagogical and deep presentation of all the possibilities Entropy Pooling\noffers, see the [Portfolio Construction and Risk Management Book](https://igg.me/at/pcrm-book).\n',
    'author': 'Fortitudo Technologies',
    'author_email': 'software@fortitudo.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://fortitudo.tech',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
