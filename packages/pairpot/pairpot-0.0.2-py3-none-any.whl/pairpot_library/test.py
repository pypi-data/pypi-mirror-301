#source ~/Browser/bin/activate
import lassoview
import pairview
import numpy as np
import anndata as ad

file_sc="/home/rzh/stpair/backend/pairpot_library/pairpot_library/sc1.h5ad"
file_sp="/home/rzh/stpair/backend/pairpot_library/pairpot_library/sp1.h5ad"
selected=[list(range(1,200))]

# res=lassoview.LPARefine(file=file_sc,selected=selected)
# print(res)

res=pairview.NNLSDeconvolution(selected=selected,scfile=file_sc,spfile=file_sp)
print(res)