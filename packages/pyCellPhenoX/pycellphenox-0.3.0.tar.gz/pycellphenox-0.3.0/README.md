
<img height="200" align="right" src="https://github.com/fanzhanglab/pyCellPhenoX/blob/163014ba1b31243a1aac4c27e0611a34c1495efe/logo/https://github.com/fanzhanglab/pyCellPhenoX/blob/main-clone/logo/cellphenoX_logo_banner.png">

[![PyPI](https://img.shields.io/pypi/v/pyXcell.svg)][pypi]
[![Status](https://img.shields.io/pypi/status/pyXcell.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/pyXcell)][python version]
[![License](https://img.shields.io/pypi/l/pyXcell)][license] 

We introduce pyCellPhenoX.

<img width="100%" align="center" src="https://github.com/fanzhanglab/pyCellPhenoX/blob/163014ba1b31243a1aac4c27e0611a34c1495efe/media/CellPhenoX.png?raw=true">

> Figure 1. Insert figure description here

## Installation
You can install _pyCellPhenoX_ from PyPI:

``` bash
pip install pyCellPhenoX
```

**conda** ([link](https://anaconda.org/conda-forge/pyCellPhenoX)):
``` bash 
# install pyCellPhenoX from conda-forge
conda install -c conda-forge pyCellPhenoX
```

**github** ([link](https://github.com/fanzhanglab/pyCellPhenoX)):
``` bash
# install pyCellPhenoX directly from github
git clone git@github.com:fanzhanglab/pyCellPhenoX.git
```

### Dependencies/ Requirements
When using pyCellPhenoX please ensure you are using the following dependency versions or requirements
``` python 
python = "^3.9"
pandas = "^2.2.3"
numpy = "^2.1.1"
xgboost = "^2.0"
numba = ">=0.54"
shap = "^0.46.0"
scikit-learn = "^1.5.2"
matplotlib = "^3.9.2"
statsmodels = "^0.14.3"
```
To check if you have the right depenencies please run the following:
#### Check Python Version
``` bash
python --version
```

#### Check individual package versions
``` bash 
pip show {package} | grep Version
```
> Replace {package} with the name of the package you want to check (e.g., pandas, numpy, etc.). This will display the installed version of the package.

### Virtual Environment

If any of the versions are not compatible with your working environment, please set up a virtual environment using one of the following methods: **conda/mamba**, **pip**, or **poetry**.

#### Conda and Mamba

To create a virtual environment using **conda** or **mamba**, follow these steps:

1. **Create the environment:**
   ```bash
   conda create --name {name_the_environment} 
    ```
2. **Activate the environment:**
   ```bash
   conda activate {name_the_environment} 
    ```
3. **Install the requirements.txt:**
   ```bash
   conda install -f requirements.txt
    ```

#### PIP
To create a virtual environment using **PIP** follow these steps:

1. **Create the environment:**
   ```bash
   python -m venv {name_the_environment} 
    ```
2. **Activate the environment:**
- on Windows
   ```bash
   {name_the_environment}\Scripts\activate
    ```
- on macOS
   ```bash
   source {name_the_environment}\bin\activate
    ```
3. **Install the requirements.txt:**
   ```bash
   pip install -r requirements.txt
    ```


## Tutorials
Please see the [Command-line Reference] for details. Additonally, please see [Walkthroughs] on the documentation page. 

## API
pyCellPhenoX has four major functions which are apart of the object:
1. split_data() - Split the data into training, testing, and validation sets 
2. model_train_shap_values() - Train the model using nested cross validation strategy and generate shap values for each fold/CV repeat
3. get_shap_values() - Aggregate SHAP values for each sample
4. get_intepretable_score() - Calculate the interpretable score based on SHAP values. 

Additional major functions associated with pyCellPhenoX are:
1. marker_discovery() - Identify markers correlated with the discriminatory power of the Interpretable Score.
2. nonNegativeMatrixFactorization() - Perform non Negative Matrix Factorization (NMF)
3. preprocessing() - Prepare the data to be in the correct format for CellPhenoX
4. principleComponentAnalysis() - Perform Principle Component Analysis (PCA)

Each function has uniqure arguments, see our [documentation] for more information

## Usage
- TODO

## License
Distributed under the terms of the [MIT license][license],
_pyCellPhenoX_ is free and open source software.

## Code of Conduct
For more information please see [Code of Conduct](CODE_OF_CONDUCT.md) or [Code of Conduct Documentation]

## Contributing
For more information please see [Contributing](CONTRIBUTING.md) or [Contributing Documentation]

## Issues
If you encounter any problems, please [file an issue] along with a detailed description. 

## Citation
If you have used `pyCellPhenoX` in your project, please use the citation below. 
``` 
@software{Young2024,
  author = {Young, Jade and Inamo, Jun and Zhang, Fan},
  title = {CellPhenoX: An eXplainable Cell-specific machine learning method to predict clinical Phenotypes using single-cell multi-omics},
  date = {2024},
  url = {https://github.com/fanzhanglab/pyCellPhenoX},
  version = {},
}
```
or 
``` 
@ARTICLE{Young2024,
  title    = "{CellPhenoX}: An eXplainable Cell-specific machine learning method to predict clinical Phenotypes using single-cell multi-omics",
  author   = "Young, Jade and Inamo, Jun and Zhang, Fan",
  journal  = "",
  volume   =  ,
  number   =  ,
  pages    = "",
  month    =  ,
  year     =  ,
  language = "en",
}
```

## Contact
Please contact [fanzhanglab@gmail.com](fanzhanglab@gmail.com) for
further questions or protential collaborative opportunities!

<!-- github-only -->

[license]: https://github.com/fanzhanglab/pyCellPhenoX/blob/main/LICENSE
[contributor guide]: https://github.com/fanzhanglab/pyCellPhenoX/blob/main/CONTRIBUTING.md
[file an issue]: https://github.com/fanzhanglab/pyCellPhenoX/issues/new
[command-line reference]: https://pyCellPhenoX.readthedocs.io/en/latest/usage.html
[pipi]: https://pypi.org/project/pip/
[pypi]: https://pypi.org/project/pyCellPhenoX/
[walkthroughs]: https://pyCellPhenoXreadthedocs.io/walkthroughs/single_cell_usage
[documentation]: https://pyCellPhenoXreadthedocs.io/
[Code of Conduct Documentation]: https://pyCellPhenoXreadthedocs.io/code_of_conduct
[Contributing Documentation]: https://pyCellPhenoXreadthedocs.io/contributing
