# ChemWalker 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/computational-chemical-biology/chemwalker/blob/master/notebooks/basic_use_colab.ipynb)

<p align="center">
  <img src="https://github.com/computational-chemical-biology/chemwalker/blob/master/img/walker.gif" alt="logo"/>
</p>

ChemWalker is a python package to propagate spectral library match identities through candidate structures provided by _in silico_ fragmentation, using [random walk](https://github.com/jinhongjung/pyrwr).

## Installation

Install conda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

```
   
Create a dedicated conda environment and activate

```
conda env create -f environment.yml
conda activate chemwalker 
pip install git+https://github.com/computational-chemical-biology/ChemWalker.git
```

## Third party

ChemWalker was tested on [MetFrag2.3.-CL.jar](http://ccbl.fcfrp.usp.br/ccbl/MetFrag2.3-CL.jar), download MetFrag CL [here](https://ipb-halle.github.io/MetFrag/projects/metfragcl/). Old releases can be found [here](https://github.com/ipb-halle/MetFragRelaunched/releases).


## References

[Tiago Cabral Borelli, Gabriel Santos Arini, Luís G P Feitosa, Pieter C Dorrestein, Norberto Peporine Lopes, Ricardo R da Silva. Improving annotation propagation on molecular networks through random walks: introducing ChemWalker. Bioinformatics 2023, 39(3), btad078.](https://doi.org/10.1093/bioinformatics/btad078)

ChemWalker uses MetFrag for in silico annotation
[Wolf, S.; Schmidt, S.; Müller-Hannemann, M.; Neumann, S. In Silico Fragmentation for Computer Assisted Identification of Metabolite Mass Spectra. BMC Bioinformatics 2010, 11 (1), 148.](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-148)

ChemWalker uses the Fusion concept, proposed on MetFusion, for ranking improvement from spectral library.
[Gerlich, M.; Neumann, S. MetFusion: Integration of Compound Identification Strategies. J. Mass Spectrom. 2013, 48 (3), 291–298.](https://onlinelibrary.wiley.com/doi/abs/10.1002/jms.3123)

### License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details

