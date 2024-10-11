from lassoview import LPARefine
from pairview import NNLSDeconvolution
from pairPotProc import process_files
from AUCell import AUCell_UCAssign
import pandas as pd
import anndata as ad


def lassoView(selected,adata,use_model,do_correct=True,function="anndata"):
    result=LPARefine(selected=selected,adata=adata,use_model=use_model,do_correct=do_correct,function=function)
    return result

def lassoView(selected,adata,do_correct=True,function="anndata"):
    result=LPARefine(selected=selected,adata=adata,do_correct=do_correct,function=function)
    return result

def pairView(selected,scfile,spfile,function="anndata"):
    result=NNLSDeconvolution(selected=selected, scfile=scfile, spfile=spfile,function=function)
    return result

def lassoProc(path):
    result=process_files(path=path)
    return result

def pairProc(adata:ad.AnnData, db:pd.DataFrame, celltype:str, alpha=10e-30, gene_col='official gene symbol'):
    result=AUCell_UCAssign(adata=adata,db=db,celltype=celltype,alpha=alpha,gene_col=gene_col)
    return result

def downLd(dataset_id,path="./"):
    #还没写
    return dataset_id