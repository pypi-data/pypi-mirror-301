import torch

from .logdet import *

# auto_kl_*_covmat
def auto_kl_covmat_covmat(mean1, covmat1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, M1) || M(v2, diag(v3)) )
    """
    mean_diff = mean1 - mean2
    return 0.5 * torch.log( 1 + (mean_diff.unsqueeze(0) @ torch.inverse(covmat1) @ mean_diff).squeeze())

def auto_kl_precmat_covmat(mean1, precmat1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, M1) || M(v2, diag(v3)) )
    """
    mean_diff = mean1 - mean2
    return 0.5 * torch.log( 1 + (mean_diff.unsqueeze(0) @ precmat1 @ mean_diff).squeeze())

def auto_kl_cholkroncov_covmat(mean1, cholkroncov1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T)) || M(v2, diag(v3)) )
    """
    mean_diff = mean1 - mean2
    LU1, LV1 = cholkroncov1
    LU1_inv, LV1_inv = torch.inverse(LU1), torch.inverse(LV1)
    U1_inv = LU1_inv.T @ LU1_inv
    V1_inv = LV1_inv.T @ LV1_inv
    covprec1 = torch.kron(U1_inv, V1_inv)

    return 0.5 * torch.log( 1 + (mean_diff.unsqueeze(0) @ covprec1 @ mean_diff)).squeeze()

# auto_kl_*_precmat
def auto_kl_covmat_precmat(mean1, covmat1, mean2):
    return auto_kl_covmat_covmat(mean1, covmat1, mean2)

def auto_kl_precmat_precmat(mean1, precmat1, mean2):
    return auto_kl_precmat_covmat(mean1, precmat1, mean2)

def auto_kl_cholkroncov_precmat(mean1, cholkroncov1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T)) || M(v2, M2))
    """
    return auto_kl_cholkroncov_covmat(mean1, cholkroncov1, mean2)

# auto_kl_*_
def auto_kl_covmat_diagvar(mean1, covmat1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, M1) || M(v2, diag(v3)) )
    """
    mean_diff = mean1 - mean2
    covmat1_diag = covmat1.diag()
    return 0.5 * (torch.sum(torch.log(covmat1_diag + mean_diff.square())) - logdet_covmat(covmat1))

def auto_kl_cholkroncov_diagvar(mean1, cholkroncov1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, M1) || M(v2, diag(v3)) )
    """
    mean_diff = mean1 - mean2
    LU1, LV1 = cholkroncov1
    covmat1_diag = torch.kron(LU1.square().sum(1), LV1.square().sum(1))

    return 0.5 * (torch.sum(torch.log(covmat1_diag + mean_diff.square())) - logdet_cholkroncov(cholkroncov1))

# auto_kl_*_diagprec
def auto_kl_covmat_diagprec(mean1, covmat1, mean2):
    return auto_kl_covmat_diagvar(mean1, covmat1, mean2)

# auto_kl_*_scalarvar
def auto_kl_covmat_scalarvar(mean1, covmat1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, M1) || M(v2, v3 I))
	"""
    d = mean1.size(0)
    mean_diff = mean1 - mean2
    total_variance = torch.trace(covmat1) + mean_diff.square().sum()
    return 0.5 * (d * torch.log(total_variance / d) - logdet_covmat(covmat1))

def auto_kl_cholkroncov_scalarvar(mean1, cholkroncov1, mean2):
    """ Compute KL with automatic optimal diagonal variance according to
        argmin_v3 KL( N(v1, M1) || M(v2, v3 I))
	"""
    d = mean1.size(0)
    LU, LV = cholkroncov1
    cov1_trace = LU.square().sum() * LV.square().sum()

    mean_diff = mean1 - mean2

    total_variance = cov1_trace + mean_diff.square().sum()
    return 0.5 * (d * torch.log(total_variance / d) - logdet_cholkroncov(cholkroncov1))

# auto_kl_*_scalarprec
def auto_kl_covmat_scalarprec(mean1, covmat1, mean2):
    return auto_kl_covmat_scalarvar(mean1, covmat1, mean2)

def auto_kl_cholkroncov_scalarprec(mean1, cholkroncov1, mean2):
    return auto_kl_cholkroncov_scalarvar(mean1, cholkroncov1, mean2)


def auto_kl(mean1, cov_type1, cov1, mean2, cov_type2):
    """ Compute KL with automatic optimal covariance according to
            argmin_cov2 KL( N(mean1, cov1) || N(mean2, cov2))
        and constrained by type of covariance (cov_type2)
    """
    func_name = f"auto_kl_{cov_type1}_{cov_type2}"

    func = globals()[func_name]

    mean_diff = mean1 - mean2

    return func(mean1, cov1, mean2)


