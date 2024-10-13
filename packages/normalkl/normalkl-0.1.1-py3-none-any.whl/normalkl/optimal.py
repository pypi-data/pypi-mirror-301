import torch

# optimal_*_diagvar
def optimal_covmat_diagvar(mean_diff, covmat1):
    """ Compute optimal diagonal variance of
        argmin_v3 KL( N(v1, M1) || M(v2, diag(v3)) )
    """
    return covmat1.diag() + mean_diff.square()

def optimal_cholkroncov_diagvar(mean_diff, cholkroncov1):
    """ Compute optimal diagonal variance of
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T)) || M(v2, diag(v3)) )
    """
    LU1, LV1 = cholkroncov1
    covmat1_diag = torch.kron(LU1.square().sum(1), LV1.square().sum(1))
    return covmat1_diag + mean_diff.square()

# optimal_*_diagprec
def optimal_covmat_diagprec(mean_diff, covmat1):
    """ Compute optimal diagonal precision of
        argmin_v3 KL( N(v1, M1) || M(v2, diag(v3)^{-1}) )
    """
    return 1 / (covmat1.diag() + mean_diff.square())

def optimal_cholkroncov_diagprec(mean_diff, cholkroncov1):
    """ Compute optimal diagonal variance of
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T)) || M(v2, diag(v3)) )
    """
    LU1, LV1 = cholkrncov1
    covmat1_diag = torch.kron(LU1.square().sum(1), LV1.square().sum(1))
    return 1 / (covmat1_diag + mean_diff.square())

# optimal_*_scalarvar
def optimal_covmat_scalarvar(mean_diff, covmat1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, covmat1) || M(v2, v3 I))
    """
    return (torch.trace(covmat1) + mean_diff.square().sum()) / len(mean_diff)

def optimal_precmat_scalarvar(mean_diff, precmat1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, precmat1^{-1}) || M(v2, v3 I))
    """
    return (torch.trace(torch.inverse(precmat1)) + mean_diff.square().sum()) / len(mean_diff)

def optimal_diagvar_scalarvar(mean_diff, diagvar1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, diagvar1) || M(v2, v3 I))
    """
    return (torch.sum(diagvar1) + mean_diff.square().sum()) / len(mean_diff)

def optimal_diagprec_scalarvar(mean_diff, diagprec1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, diagprec1) || M(v2, v3 I))
    """
    return (torch.sum(1/diagprec1) + mean_diff.square().sum()) / len(mean_diff)

def optimal_scalarvar_scalarvar(mean_diff, scalarvar1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, scalarvar1 I ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    return (d * scalarvar1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_scalarprec_scalarvar(mean_diff, scalarprec1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, scalarprec1^{-1} I ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    return (d * scalarprec1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_identity_scalarvar(mean_diff, _ignore):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, I ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    return (mean_diff.square().sum()) / len(mean_diff)

def optimal_cholcov_scalarvar(mean_diff, cholcov1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, L1 L1^T ) || M(v2, v3 I))
    """
    trace1 = cholcov.square().sum()
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_cholprec_scalarvar(mean_diff, cholcov1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, L1 L1^T ) || M(v2, v3 I))
    """
    trace1 = torch.inverse(cholcov1).square().sum()
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_kroncov_scalarvar(mean_diff, kroncov1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, (U1 kron V1) ) || M(v2, v3 I))
    """
    U1, V1 = kroncov1
    trace1 = torch.trace(U1) * torch.trace(V1)
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_kronprec_scalarvar(mean_diff, kronprec1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, (U1 kron V1) ) || M(v2, v3 I))
    """
    U1, V1 = kronprec1
    trace1 = torch.trace(torch.inverse(U1)) * torch.trace(torch.inverse(V1))
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_cholkroncov_scalarvar(mean_diff, cholkroncov1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T) ) || M(v2, v3 I))
    """
    LU1, LV1 = cholkroncov1
    trace1 = LU1.square().sum() * LV1.square().sum()
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_cholkronprec_scalarvar(mean_diff, cholkronprec1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T) ) || M(v2, v3 I))
    """
    LU1_inv, LV1_inv = cholkronprec1
    LU1, LV1 = torch.inverse(LU1_inv), torch.inverse(LV1_inv)
    trace1 = LU1.square().sum() * LV1.square().sum()
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_diagcovrowcol_scalarvar(mean_diff, diagcovrowcol1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, diag(a) kron diag(b) ) || M(v2, v3 I))
    """
    a, b = diagcovrowcol1
    trace1 = torch.outer(a, b).sum()
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_diagcovrow_scalarvar(mean_diff, diagcovrow1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, diag(a) kron diag(1) ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    d1 = diagcovrow1.size(0)
    d2 = d // d1
    trace1 = diagcovrow1.sum() * d2
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)

def optimal_diagcovcol_scalarvar(mean_diff, diagcovcol1):
    """ Compute optimal scalar variance of
        argmin_v3 KL( N(v1, diag(1) kron diag(b) ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    d2 = diagcovcol1.size(0)
    d1 = d // d2
    trace1 = d1 * diagcovcol1.sum()
    return (trace1 + mean_diff.square().sum()) / len(mean_diff)


# optimal_*_scalarprec
def optimal_covmat_scalarprec(mean_diff, covmat1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, covmat1) || M(v2, v3 I))
    """
    return len(mean_diff) / (torch.trace(covmat1) + mean_diff.square().sum()) 

def optimal_precmat_scalarprec(mean_diff, precmat1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, precmat1^{-1}) || M(v2, v3 I))
    """
    return len(mean_diff) / (torch.trace(torch.inverse(precmat1)) + mean_diff.square().sum()) 

def optimal_diagvar_scalarprec(mean_diff, diagvar1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, diagvar1) || M(v2, v3 I))
    """
    return len(mean_diff) / (torch.sum(diagvar1) + mean_diff.square().sum()) 

def optimal_diagprec_scalarprec(mean_diff, diagprec1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, diagprec1) || M(v2, v3 I))
    """
    return len(mean_diff) / (torch.sum(1/diagprec1) + mean_diff.square().sum()) 

def optimal_scalarprec_scalarprec(mean_diff, scalarvar1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, scalarvar1 I ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    return len(mean_diff) / (d * scalarvar1 + mean_diff.square().sum()) 

def optimal_scalarprec_scalarprec(mean_diff, scalarprec1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, scalarprec1^{-1} I ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    return len(mean_diff) / (d * scalarprec1 + mean_diff.square().sum()) 

def optimal_identity_scalarprec(mean_diff, _ignore):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, I ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    return len(mean_diff) / (mean_diff.square().sum()) 

def optimal_cholcov_scalarprec(mean_diff, cholcov1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, L1 L1^T ) || M(v2, v3 I))
    """
    trace1 = cholcov.square().sum(1)
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_cholprec_scalarprec(mean_diff, cholcov1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, L1 L1^T ) || M(v2, v3 I))
    """
    trace1 = torch.inverse(cholcov1).square().sum(1)
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_kroncov_scalarprec(mean_diff, kroncov1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, (U1 kron V1) ) || M(v2, v3 I))
    """
    U1, V1 = kroncov1
    trace1 = torch.trace(U1) * torch.trace(V1)
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_kronprec_scalarprec(mean_diff, kronprec1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, (U1 kron V1) ) || M(v2, v3 I))
    """
    U1, V1 = kronprec1
    trace1 = torch.trace(torch.inverse(U1)) * torch.trace(torch.inverse(V1))
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_cholkroncov_scalarprec(mean_diff, cholkroncov1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T) ) || M(v2, v3 I))
    """
    LU1, LV1 = cholkroncov1
    trace1 = LU1.square().sum() * LV1.square().sum()
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_cholkronprec_scalarprec(mean_diff, cholkronprec1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, (LU1 LU1^T kron LV1 LV1^T) ) || M(v2, v3 I))
    """
    LU1_inv, LV1_inv = cholkronprec1
    LU1, LV1 = torch.inverse(LU1_inv), torch.inverse(LV1_inv)
    trace1 = LU1.square().sum() * LV1.square().sum()
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_diagcovrowcol_scalarprec(mean_diff, diagcovrowcol1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, diag(a) kron diag(b) ) || M(v2, v3 I))
    """
    a, b = diagcovrowcol1
    trace1 = torch.outer(a, b).sum()
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 

def optimal_diagcovrow_scalarprec(mean_diff, diagcovrow1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, diag(a) kron diag(1) ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    d1 = diagcovrow1.size(0)
    d2 = d // d1
    trace1 = diagcovrow1.sum() * d2
    return len(mean_diff) / (trace1 + mean_diff.square().sum())

def optimal_diagcovcol_scalarprec(mean_diff, diagcovcol1):
    """ Compute optimal scalar precision of
        argmin_v3 KL( N(v1, diag(1) kron diag(b) ) || M(v2, v3 I))
    """
    d = mean_diff.size(0)
    d2 = diagcovcol1.size(0)
    d1 = d // d2
    trace1 = d1 * diagcovcol1.sum()
    return len(mean_diff) / (trace1 + mean_diff.square().sum()) 



def optimal_covariance(mean1, cov_type1, cov1, mean2, cov_type2):
    """ Find optimal cov2 that solves
            argmin_cov2 KL( N(mean1, cov1) || N(mean2, cov2))
    """
    func_name = f"optimal_{cov_type1}_{cov_type2}"

    func = globals()[func_name]

    mean_diff = mean1 - mean2

    return func(mean_diff, cov1)


