""" Functions that compute log-determinant term of the KL divergence for different covariance types. """

import torch

def logdet_covmat(covmat):
    """ Log determinant for full covariance matrix """
    return torch.logdet(covmat)

def logdet_precmat(precmat):
    """ Log determinant for full precision matrix """
    return -torch.logdet(precmat)

def logdet_diagvar(diagvar):
    """ Log determinant for diagonal covariance matrix (vector) """
    return diagvar.abs().log().sum().squeeze()

def logdet_scalarvar(scalarvar, dim):
    """ Log determinant for scalar variance """
    return dim * scalarvar.abs().log().squeeze()

def logdet_cholcov(cholcov):
    """ Log determinant for Cholesky covariance matrix """
    L = cholcov
    return L.diag().square().log().sum()

def logdet_kroncov(kroncov):
    """ Log determinant for Kronecker product of two matrices """
    U, V = kroncov
    return len(V) * logdet_covmat(U) + len(U) * logdet_covmat(V)

def logdet_cholkroncov(cholkroncov):
    LU, LV = cholkroncov
    """ Log determinant for Cholesky Kronecker covariance """
    return len(LV) * logdet_cholcov(LU) + len(LU) * logdet_cholcov(LV)


# Precision versions of the above functions:

def logdet_precmat(precmat):
    """ Log determinant for precision matrix """
    return -logdet_covmat(precmat)

def logdet_diagprec(diagprec):
    """ Log determinant for diagonal precision matrix """
    return -diagprec.abs().log().sum()

def logdet_scalarprec(scalarprec, dim):
    """ Log determinant for scalar precision """
    return -dim * scalarprec.log()

def logdet_cholprec(cholprec):
    """ Log determinant for Cholesky precision matrix """
    L = cholprec
    return -L.diag().square().log().sum()

def logdet_kronprec(kronprec):
    U, V = kronprec
    """ Log determinant for Kronecker product of two precision matrices """
    return len(V) * logdet_precmat(U) + len(U) * logdet_precmat(V)

def logdet_cholkronprec(cholkronprec):
    """ Log determinant for Cholesky Kronecker precision """
    LU, LV = cholkronprec
    return len(LV) * logdet_cholprec(LU) + len(LU) * logdet_cholprec(LV)

