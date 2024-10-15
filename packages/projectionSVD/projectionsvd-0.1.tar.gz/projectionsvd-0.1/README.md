# projectionSVD (v0.1)
[![DOI](https://zenodo.org/badge/866019962.svg)](https://doi.org/10.5281/zenodo.13881622)\
`projectionSVD` is a small command-line program written in Python/Cython to project a dataset onto a principal component space based on genotype data. It takes binary PLINK files as genotype input and works with PCA output from programs like `PLINK` and `PCAone`. `projectionSVD` requires estimated allele frequencies, eigenvalues and SNP loadings to perform the projection.

## Usage
```bash
# Perform projection using PCAone output (use --pcaone for proper scaling)
projectionSVD --bfile new --freqs old.afreq --eigvals old.eigvals --loadings old.loadings --threads 32 --out new --pcaone

# Outputs eigenvectors of new dataset (new.eigvecs2)
```

### Options
* `--pcaone`, indicate that files are from PCAone to perform proper scaling
* `--freqs-col`, specify which column to use in frequency file (6)
* `--batch`, process projection in batches of specified number of SNPs
* `--raw`, only output eigenvectors without FID/IID

## Installation
```bash
git clone https://github.com/Rosemeis/projectionSVD.git
cd projectionSVD
pip3 install .

# The "projectionSVD" main caller will now be available
