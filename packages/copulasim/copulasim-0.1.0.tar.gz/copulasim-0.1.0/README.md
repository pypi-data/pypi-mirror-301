# Copula

`Copula` is a Python library that helps you to create simple simulated sets of copulas

## Features
- denisty function of a gaussian copula given two data sets
- generate samples from a copula, given an empirical cdf

the functions you have access too are:

* copula_density(u, R)
- get the density function of the copula 
- u: multivatiate time series
* copula_likelihood(R_f, u)
- likleyhood function that gives back the likihood function -> used for get_cov 
* get_cov(u_ecdf)
- get back the cov matrix, which was fit with the ML estimation and an optimizer from the scipy package
- needs an empirical cdf as input
* sampling_gaussian_copula(R, n_samples)
- get n samples from a gaussian copula, given a cov matrix (get the cov with the get_cov function)

## Installation

Install via pip:

```bash
pip install copulasim