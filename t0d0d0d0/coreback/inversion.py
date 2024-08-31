from fastapi import Depends
from t0d0d0d0.coreback.uow import UnitOfWork, infra


def anonuow(infra:infra):
    return lambda:UnitOfWork(infra=infra)

def uowdep(infra:infra):
    return Depends(anonuow(infra=infra))
