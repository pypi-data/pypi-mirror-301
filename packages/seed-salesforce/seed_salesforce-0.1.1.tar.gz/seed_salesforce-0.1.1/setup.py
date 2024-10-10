# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seed_salesforce']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil', 'simple-salesforce>=1.12.6,<2.0.0']

setup_kwargs = {
    'name': 'seed-salesforce',
    'version': '0.1.1',
    'description': 'Package for connecting SEED data to Salesforce',
    'long_description': '## SEED Salesforce Connection\n\nThe SEED Salesforce connection enables data exchange between a SEED instance and a Salesforce instance.\n\n### Getting Started\n\nClone this repository, then install the poetry-based dependencies.\n\n```\npip install poetry\npoetry install\n```\n\n### Configuring\n\nThe Salesforce configuration file is needed for this library to function correctly.\n\n#### Salesforce\n\nCopy `salesforce-config-example.json` to `salesforce-config-dev.json` and fill\nin with the correct credentials. The format of the Salesforce should contain the following:\n\n```\n{\n    "instance": "https://<url>.lightning.force.com",\n    "username": "user@company.com",\n    "password": "secure-password",\n    "security_token": "secure-token"\n    "domain": ""\n}\n```\n\n**IMPORTANT:** If you are connecting to a sandbox Salesforce environment, make sure to add "domain": "test" to the `salesforce-config-dev.json` file or authentication will fail.\n\n### Running Tests\n\nMake sure to add and configure the Salesforce configuration file. Note that it must be named `salesforce-config-dev.json` for the tests to run correctly.\n\nRun the tests using:\n\n```\npoetry run pytest\n```\n\n#### GitHub Actions\n\nThe credentials are stored in a GitHub Action Secret. Add the following with correctly filled out information to a secret key named SALESFORCE_CONFIG:\n\nNote that double quotes must be escaped.\n\n```\n{\n    \\"instance\\": \\"https://<environment>.lightning.force.com\\",\n    \\"username\\": \\"user@somedomain.com\\",\n    \\"password\\": \\"alongpassword!asdf\\",\n    \\"security_token\\": \\"access1key2with3numbers\\",\n    \\"domain\\": \\"test\\"\n}\n```\n',
    'author': 'Nicholas Long',
    'author_email': 'nicholas.long@nrel.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://seed-platform.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
