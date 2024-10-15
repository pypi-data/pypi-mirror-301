import scipy.stats as stats
import numpy as np
import scipy 


def copula_density(u, R):
    
    phi_inv = stats.norm.ppf(u)
    
    pre_term = 1/np.sqrt(np.linalg.det(R))
    
    R_inv = np.linalg.inv(R)
    d = R.shape[0]
    R_I = R_inv - np.eye(d)
    
    dot_product = np.dot(phi_inv, np.dot(R_I, phi_inv))
    
    expo = np.exp(-0.5 * np.einsum('ij,ij->i', phi_inv, np.dot(phi_inv, R_I)))
    
    return pre_term*expo

def copula_likelihood(R_f, u):
    
    d = u.shape[1]
    R = R_f.reshape((d, d))
    
    R = (R + R.T) / 2
    np.fill_diagonal(R, 1)
    
    if np.any(np.linalg.eigvals(R) <= 0):
        return np.inf


    R_inv = np.linalg.inv(R)
    I = np.eye(d)
    
    phi_inv = stats.norm.ppf(u)
    
    diff = np.dot(phi_inv, R_inv - I)
    dot = np.einsum('ij,ij->i', phi_inv, diff)
    log_det_R = np.log(np.linalg.det(R))
    
    # Sum over observations to get a scalar
    neg_log_likelihood = (1/2) * (log_det_R + np.sum(dot))
    return neg_log_likelihood


def get_cov(u_ecdf):
    
    R_start = np.eye(2).flatten()

    result = scipy.optimize.minimize(
        copula_likelihood,
        R_start,
        args=(u_ecdf,),
        method='BFGS'
    )
    
    return result.reshape(2,2)

def sampling_gaussian_copula(R, n_samples):

    d = R.shape[0]
    
    L = np.linalg.cholesky(R)
    
    samples_start = np.random.normal(size = (n_samples, d))
    
    samples_corr = np.dot(samples_start, L.T)
    
    u_samples = stats.norm.cdf(samples_corr)
    
    return u_samples



