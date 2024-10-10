# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unpast', 'unpast.tests', 'unpast.tests.utils', 'unpast.utils']

package_data = \
{'': ['*'],
 'unpast.tests': ['results/*', 'test_input/*', 'test_reference_output/*']}

install_requires = \
['fisher==0.1.9',
 'lifelines==0.27.4',
 'matplotlib==3.7.1',
 'numba==0.51.2',
 'numpy==1.22.3',
 'pandas==1.3.5',
 'python-louvain==0.15',
 'scikit-learn==1.2.2',
 'scikit-network>=0.24.0,<0.26.0',
 'scipy==1.7.1',
 'seaborn==0.11.1',
 'statsmodels==0.13.2']

entry_points = \
{'console_scripts': ['unpast = unpast.run_unpast:main']}

setup_kwargs = {
    'name': 'unpast',
    'version': '0.1.9.6.1',
    'description': 'A novel method for unsupervised patient stratification.',
    'long_description': '# UnPaSt\n\nUnPaSt is a novel method for identification of differentially expressed biclusters.\n\n<img src="https://apps.cosy.bio/unpast/assets/DESMOND2_steps2.png"  height="350">\n\n## Cite\nUnPaSt preprint [https://arxiv.org/abs/2408.00200](https://arxiv.org/abs/2408.00200).\n\nCode: [https://github.com/ozolotareva/unpast_paper/](https://github.com/ozolotareva/unpast_paper/)\n\n## Web server\n[Run UnPaSt at CoSy.Bio server](https://apps.cosy.bio/unpast/)\n\n## Install\n![Tests status](https://github.com/ozolotareva/unpast/actions/workflows/run_tests.yml/badge.svg)\n\n### Docker environment [to be updated]\nUnPaSt environment is available also as a Docker image.\n\n```bash\ndocker pull freddsle/unpast\ngit clone https://github.com/ozolotareva/unpast.git\ncd unpast\nmkdir -p results\n\n# running UnPaSt with default parameters and example data\ncommand="python unpast/run_unpast.py --exprs unpast/tests/scenario_B500.exprs.tsv.gz --basename results/scenario_B500"\ndocker run --rm -u $(id -u):$(id -g) -v "$(pwd)":/data --entrypoint bash freddsle/unpast -c "cd /data && PYTHONPATH=/data $command"\n```\n\n### Requirements: [to be updated]\n```\nPython (version 3.8.16):\n    fisher==0.1.9\n    pandas==1.3.5\n    python-louvain==0.15\n    matplotlib==3.7.1\n    seaborn==0.11.1\n    numba==0.51.2\n    numpy==1.22.3\n    scikit-learn==1.2.2\n    scikit-network==0.24.0\n    scipy==1.7.1\n    statsmodels==0.13.2\n    kneed==0.8.1\n\nR (version 4.3.1):\n    WGCNA==1.70-3\n    limma==3.42.2\n```\n\n### Installation tips [to be updated]\n\nIt is recommended to use "BiocManager" for the installation of WGCNA:\n```R\ninstall.packages("BiocManager")\nlibrary(BiocManager)\nBiocManager::install("WGCNA")\n```\n\n## Input\nUnPaSt requires a tab-separated file with features (e.g. genes) in rows, and samples in columns.\n* Feature and sample names must be unique.\n* At least 2 features and 5 samples are required.\n* Data must be between-sample normalized.\n\n### Recommendations: \n* It is recommended that UnPaSt be applied to datasets with 20+ samples.\n* If the cohort is not large (<20 samples), reducing the minimal number of samples in a bicluster (`min_n_samples`) to 2 is recommended. \n* If the number of features is small, using Louvain method for feature clustering instead of WGCNA and/or disabling feature selection by setting the binarization p-value (`p-val`) to 1 might be helpful.\n\n## Examples\n* Simulated data example. Biclustering of a matrix with 10000 rows (features) and 200 columns (samples) with four implanted biclusters consisting of 500 features and 10-100 samples each. For more details, see figure 3 and Methods [here](https://arxiv.org/abs/2408.00200).\n  \n```bash\nmkdir -p results;\n\n# running UnPaSt with default parameters and example data\npython -m unpast.run_unpast --exprs unpast/tests/scenario_B500.exprs.tsv.gz --basename results/scenario_B500\n\n# with different binarization and clustering methods\npython -m unpast.run_unpast --exprs unpast/tests/scenario_B500.exprs.tsv.gz --basename results/scenario_B500 --binarization ward --clustering Louvain\n\n# help\npython run_unpast.py -h\n```\n* Real data example. Analysis of a subset of 200 samples randomly chosen from TCGA-BRCA dataset, including consensus biclustering and visualization:\n  [jupyter-notebook](https://github.com/ozolotareva/unpast/blob/main/notebooks/UnPaSt_examples.ipynb).\n  \n## Outputs\n`<basename>.[parameters].biclusters.tsv` - A `.tsv` file containing the identified biclusters with the following structure:\n\n- * the first line starts with `#`, storing the parameters of UnPaSt\n- * the second line contains the column headers.\n- * each subsequent line represents a bicluster with the following columns:\n  - **SNR**: Signal-to-noise ratio of the bicluster, calculated as the average SNR of its features.\n  - **n_genes**: Number of genes in the bicluster.\n  - **n_samples**: Number of samples in the bicluster.\n  - **genes**: Space-separated list of gene names.\n  - **samples**: Space-separated list of sample names.\n  - **direction**: Indicates whether the bicluster consists of up-regulated ("UP"), down-regulated ("DOWN"), or both types of genes ("BOTH").\n  - **genes_up**, **genes_down**: Space-separated lists of up- and down-resulated genes respectively.\n  - **gene_indexes**: 0-based index of the genes in the input matrix.\n  - **sample_indexes**: 0-based index of the samples in the input matrix.\n\nAlong with the biclustering result, UnPaSt creates three files with intermediate results in the output folder `out_dir`:\n  - `<basename>.[parameters].binarized.tsv` with binarized input data.\n  - `<basename>.[parameters].binarization_stats.tsv` provides binarization statistics for each processed feature.\n  - `<basename>.[parameters].background.tsv` stores background distributions of SNR values for each evaluated bicluster size.\nThese files can be used to restart UnPaSt with the same input and seed from the feature clustering step and skip time-consuming feature binarization. \n\n## Versions\nUnPaSt version used in PathoPlex paper: [UnPaSt_PathoPlex.zip](https://github.com/ozolotareva/unpast_paper/blob/main/paper/UnPaSt_PathoPlex.zip)\n',
    'author': 'Olga Zolotareva (ozolotareva)',
    'author_email': 'None',
    'maintainer': 'Olga Zolotareva (ozolotareva)',
    'maintainer_email': 'None',
    'url': 'https://github.com/ozolotareva/unpast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
