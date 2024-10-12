# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['prodigy_prot', 'prodigy_prot.modules']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.80,<2.0', 'freesasa==2.2.1', 'numpy>=1.22.0,<2.0.0']

entry_points = \
{'console_scripts': ['prodigy = prodigy_prot.predict_IC:main']}

setup_kwargs = {
    'name': 'prodigy-prot',
    'version': '2.2.4',
    'description': 'PROtein binDIng enerGY prediction',
    'long_description': '# PRODIGY / Binding Affinity Prediction \n\n![PyPI - License](https://img.shields.io/pypi/l/prodigy-prot)\n![PyPI - Status](https://img.shields.io/pypi/status/prodigy-prot)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prodigy-prot)\n[![ci](https://github.com/haddocking/prodigy/actions/workflows/ci.yml/badge.svg)](https://github.com/haddocking/prodigy/actions/workflows/ci.yml)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/98180cbac27d4a5aaf46a3dd72c3174d)](https://www.codacy.com/gh/haddocking/prodigy/dashboard?utm_source=github.com&utm_medium=referral&utm_content=haddocking/prodigy&utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/98180cbac27d4a5aaf46a3dd72c3174d)](https://www.codacy.com/gh/haddocking/prodigy/dashboard?utm_source=github.com&utm_medium=referral&utm_content=haddocking/prodigy&utm_campaign=Badge_Coverage)\n[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green)](https://fair-software.eu)\n\n[![SQAaaS badge shields.io](https://img.shields.io/badge/sqaaas%20software-gold-yellow)](https://api.eu.badgr.io/public/assertions/w8HcpcH4Svi3-UZ93LHHMA "SQAaaS gold badge achieved")\n\n\n\n\n[![SQAaaS badge](https://github.com/EOSC-synergy/SQAaaS/raw/master/badges/badges_150x116/badge_software_gold.png)](https://api.eu.badgr.io/public/assertions/w8HcpcH4Svi3-UZ93LHHMA "SQAaaS gold badge achieved")\n\n* * *\n\nPRODIGY is also available as a web service @ [wenmr.science.uu.nl/prodigy](https://wenmr.science.uu.nl/prodigy/)\n\n## Installation\n\n```text\npip install prodigy-prot\n```\n\nIf you want to develop PRODIGY, check [DEVELOPMENT](DEVELOPMENT.md) for more details.\n\n## Usage\n\n```bash\nprodigy <pdb file> [--selection <chain1><chain2>]\n```\n\nTo get a list of all the possible options.\n\n```bash\n$ prodigy --help\nusage: prodigy [-h] [--distance-cutoff DISTANCE_CUTOFF] [--acc-threshold ACC_THRESHOLD] [--temperature TEMPERATURE]\n               [--contact_list] [--pymol_selection] [-q] [-V] [--selection A B [A,B C ...]]\n               structf\n\nBinding affinity predictor based on Intermolecular Contacts (ICs).\n\nAnna Vangone and Alexandre M.J.J. Bonvin,\nContacts-based prediction of binding affinity in protein-protein complexes.\neLife (2015)\n\npositional arguments:\n  structf               Structure to analyse in PDB or mmCIF format\n\noptions:\n  -h, --help            show this help message and exit\n  --distance-cutoff DISTANCE_CUTOFF\n                        Distance cutoff to calculate ICs\n  --acc-threshold ACC_THRESHOLD\n                        Accessibility threshold for BSA analysis\n  --temperature TEMPERATURE\n                        Temperature (C) for Kd prediction\n  --contact_list        Output a list of contacts\n  --pymol_selection     Output a script to highlight the interface (pymol)\n  -q, --quiet           Outputs only the predicted affinity value\n  -V, --version         Print the version and exit.\n\nSelection Options:\n\n      By default, all intermolecular contacts are taken into consideration,\n      a molecule being defined as an isolated group of amino acids sharing\n      a common chain identifier. In specific cases, for example\n      antibody-antigen complexes, some chains should be considered as a\n      single molecule.\n\n      Use the --selection option to provide collections of chains that should\n      be considered for the calculation. Separate by a space the chains that\n      are to be considered _different_ molecules. Use commas to include multiple\n      chains as part of a single group:\n\n      --selection A B => Contacts calculated (only) between chains A and B.\n      --selection A,B C => Contacts calculated (only) between chains A and C; and B and C.\n      --selection A B C => Contacts calculated (only) between chains A and B; B and C; and A and C.\n\n\n  --selection A B [A,B C ...]\n```\n\n## Example\n\nDownload the PDB [3BZD](https://www.rcsb.org/structure/3bzd) and run PRODIGY on it.\n\n```bash\n$ curl -o 3bzd.pdb https://files.rcsb.org/download/3BZD.pdb\n$ prodigy 3bzd.pdb\n[+] Reading structure file: /Users/rvhonorato/dbg/3bzd.pdb\n[+] Parsed structure file 3bzd (2 chains, 343 residues)\n[+] No. of intermolecular contacts: 51\n[+] No. of charged-charged contacts: 4\n[+] No. of charged-polar contacts: 7\n[+] No. of charged-apolar contacts: 6\n[+] No. of polar-polar contacts: 7\n[+] No. of apolar-polar contacts: 15\n[+] No. of apolar-apolar contacts: 12\n[+] Percentage of apolar NIS residues: 29.48\n[+] Percentage of charged NIS residues: 29.48\n[++] Predicted binding affinity (kcal.mol-1):     -9.4\n[++] Predicted dissociation constant (M) at 25.0˚C:  1.3e-07\n```\n\nDetails of the binding affinity predictor implemented in PRODIGY can be found at [10.7554/elife.07454](https://doi.org/10.7554/elife.07454)\n\n## Citing us\n\nIf our tool is useful to you, please cite PRODIGY in your publications:\n\n- **Xue L, Rodrigues J, Kastritis P, Bonvin A.M.J.J, Vangone A.**: PRODIGY: a web server for predicting the binding affinity of protein-protein complexes. _Bioinformatics_ (2016) ([10.1093/bioinformatics/btw514](https://doi.org/10.1093/bioinformatics/btw514))\n\n- **Anna Vangone and Alexandre M.J.J. Bonvin**: Contacts-based prediction of binding affinity in protein-protein complexes. _eLife_, e07454 (2015) ([10.7554/eLife.07454](https://doi.org/10.7554/elife.07454))\n\n- **Panagiotis L. Kastritis , João P.G.L.M. Rodrigues, Gert E. Folkers, Rolf Boelens, Alexandre M.J.J. Bonvin**: Proteins Feel More Than They See: Fine-Tuning of Binding Affinity by Properties of the Non-Interacting Surface. _Journal of Molecular Biology_, 14, 2632–2652 (2014). ([10.1016/j.jmb.2014.04.017](https://doi.org/10.1016/j.jmb.2014.04.017))\n\n## Contact\n\nFor questions about PRODIGY usage, please reach out the team at [ask.bioexcel.eu](https://ask.bioexcel.eu/)\n\n## Information about dependencies\n\nThe scripts rely on [Biopython](www.biopython.org) to validate the PDB structures and calculate\ninteratomic distances. [freesasa](https://github.com/mittinatten/freesasa), with the parameter\nset used in NACCESS ([Chothia, 1976](http://www.ncbi.nlm.nih.gov/pubmed/994183)), is also\nrequired for calculating the buried surface area.\n\n**DISCLAIMER**: given the different software to calculate solvent accessiblity, predicted\nvalues might differ (very slightly) from those published in the reference implementations.\nThe correlation of the actual atomic accessibilities is over 0.99, so we expect these\ndifferences to be very minor.\n\n---\n',
    'author': 'Computational Structural Biology Group at Utrecht University',
    'author_email': 'prodigy.bonvinlab@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
