#FDRest.py
import os
import re
import sys
import collections
import argparse
import tables
import itertools 
import scipy
import matplotlib
import csv
import glob

import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.sparse as sp_sparse
import scipy.io as sio

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from multiprocessing import Pool
from collections import defaultdict
from scipy import sparse
from scipy.sparse import csr_matrix
from scipy.cluster.hierarchy import dendrogram, linkage

from pySpade.utils import get_logger, get_num_processes, read_annot_df, read_sgrna_dict, load_data

logger = get_logger(logger_name=__name__)

def FDR_estimation(FILE_DIR,
                    DISTRI_DIR,
                    BIN,
                    OUTPUT_DF):
    
    logger.info('Loading files.')
    gene_seq = np.load(FILE_DIR + 'Trans_genome_seq.npy', allow_pickle=True)
    if len(gene_seq) != len(set(gene_seq)):
        logger.critical('Duplication of mapping genes. Duplicates are removed in the analysis.')
    unique_elements, counts = np.unique(gene_seq, return_counts=True)
    duplicate_elements = unique_elements[counts > 1]

    #read the plotting annotation
    annot_df_dup = read_annot_df()
    #There are many non-coding genes duplication in the annot_df, only keep one.
    annot_df = annot_df_dup.drop_duplicates(subset='gene_names', keep='first')

    #Load the background files
    down_A = np.load(DISTRI_DIR + 'Down_dist_gamma-%s-A.npy'%(str(BIN)))
    down_B = np.load(DISTRI_DIR + 'Down_dist_gamma-%s-B.npy'%(str(BIN)))
    down_C = np.load(DISTRI_DIR + 'Down_dist_gamma-%s-C.npy'%(str(BIN)))
    up_A = np.load(DISTRI_DIR + 'Up_dist_gamma-%s-A.npy'%(str(BIN)))
    up_B = np.load(DISTRI_DIR + 'Up_dist_gamma-%s-B.npy'%(str(BIN)))
    up_C = np.load(DISTRI_DIR + 'Up_dist_gamma-%s-C.npy'%(str(BIN)))

    #Load background distribution and calculate Singificane score for each iteration
    cpm_mean = np.load(DISTRI_DIR + 'Cpm_mean-%s.npy'%(str(BIN)))
    cpm_matrix = sio.loadmat(DISTRI_DIR + 'A-cpm-%s'%(str(BIN)))['matrix']
    
    #rand_down_file = sio.loadmat(DISTRI_DIR + '%s-down_log-pval'%(str(BIN)))
    rand_down_file = sio.loadmat(DISTRI_DIR + 'A-down_log-pval-%s'%(str(BIN)))
    rand_down_matrix = []
    rand_down_matrix = sp_sparse.vstack(rand_down_file['matrix'])
    iter_num, gene_num = rand_down_matrix.shape

    #rand_up_file = sio.loadmat(DISTRI_DIR + '%s-up_log-pval'%(str(BIN)))
    rand_up_file = sio.loadmat(DISTRI_DIR + 'A-up_log-pval-%s'%(str(BIN)))
    rand_up_matrix = []
    rand_up_matrix = sp_sparse.vstack(rand_up_file['matrix'])
    iter_num, gene_num = rand_up_matrix.shape

    #generate global df 
    df_column_list = [
        'idx', 'gene_names', 'chromosome', 'pos', 'strand', 
        'color_idx', 'chr_idx', 
        'region', 'num_cell', 'bin',
        'log(pval)-hypergeom', 'Significance_score', 'fc_by_rand_dist_cpm', 'cpm_perturb', 'cpm_bg']
    global_hits_df = pd.DataFrame(columns=df_column_list)

    logger.info('Start analysis.')
    
    #Global hits analysis for each iteration 
    for e in np.arange(iter_num):
        if (e % 25 == 0):
            logger.info('Finished ' + str(e) + ' iterations.')
        #Calculate the direction (up or down regulated) for each gene
        fc_cpm = (np.asarray(cpm_matrix.tocsr().todense())[e] + 0.01)/(cpm_mean + 0.01)
        up_idx = np.where(np.array(fc_cpm) > 1)[0]
        down_idx = np.where(np.array(fc_cpm) < 1)[0]

        #Calculate the overlap genes with annot_df, and only save the information on those genes.
        unique_elements, unique_indices = np.unique(gene_seq, return_index=True)
        up_keep_genes = list(set(annot_df['gene_names']).intersection(set(gene_seq[up_idx]))) #up-regulated genes found in both annotation file and transcriptome df
        up_keep_genes_idx = sorted(list(unique_indices[np.where(np.isin(unique_elements, up_keep_genes))[0]]))
        down_keep_genes = list(set(annot_df['gene_names']).intersection(set(gene_seq[down_idx])))
        down_keep_genes_idx = sorted(list(unique_indices[np.where(np.isin(unique_elements, down_keep_genes))[0]]))

        #Calculate p-value adj for gamma distribution
        down_padj_list = []
        num_processes = get_num_processes()
        with Pool(processes=num_processes) as p:
            for down_padj in p.starmap(scipy.stats.gamma.logsf, zip(
                -np.asarray(rand_down_matrix.tocsr().todense())[e][down_keep_genes_idx],
                down_A[down_keep_genes_idx],
                down_B[down_keep_genes_idx], 
                down_C[down_keep_genes_idx])
            ):
                down_padj_list.append(down_padj)
        
        down_p_hypergeom = np.asarray(rand_down_matrix.tocsr().todense())[e][down_keep_genes_idx]
        down_hit_fc_list = fc_cpm[down_keep_genes_idx]
        down_cpm = np.asarray(cpm_matrix.tocsr().todense())[e][down_keep_genes_idx]
        down_cpm_bg = cpm_mean[down_keep_genes_idx]
        #emp_pval_down = np.sum(np.asarray(rand_down_matrix.tocsr()[:, down_keep_genes_idx].todense()) < np.asarray(rand_down_matrix.tocsr().todense())[e][down_keep_genes_idx], axis=0) / iter_num

        up_padj_list = []
        with Pool(processes=num_processes) as p:
            for up_padj in p.starmap(scipy.stats.gamma.logsf, zip(
                -np.asarray(rand_up_matrix.tocsr().todense())[e][up_keep_genes_idx],
                up_A[up_keep_genes_idx],
                up_B[up_keep_genes_idx], 
                up_C[up_keep_genes_idx])
            ):
                up_padj_list.append(up_padj)
        
        up_p_hypergeom = np.asarray(rand_up_matrix.tocsr().todense())[e][up_keep_genes_idx]
        up_hit_fc_list = fc_cpm[up_keep_genes_idx]
        up_cpm = np.asarray(cpm_matrix.tocsr().todense())[e][up_keep_genes_idx]
        up_cpm_bg = cpm_mean[up_keep_genes_idx]
        #emp_pval_up = np.sum(np.asarray(rand_up_matrix.tocsr()[:, up_keep_genes_idx].todense()) < np.asarray(rand_up_matrix.tocsr().todense())[e][up_keep_genes_idx], axis=0) / iter_num
        
        #save to csv file: down-regulation gene 
        global_gene_series = annot_df[annot_df['gene_names'].isin(gene_seq[down_keep_genes_idx])].set_index('idx').sort_index()
        global_gene_series['region'] = e
        global_gene_series['num_cell'] = BIN
        global_gene_series['bin'] = BIN
        global_gene_series['log(pval)-hypergeom'] = down_p_hypergeom
        global_gene_series['Significance_score'] = down_padj_list
        global_gene_series['fc_by_rand_dist_cpm'] = down_hit_fc_list
        #global_gene_series['pval-empirical'] = emp_pval_down
        global_gene_series['cpm_perturb'] = down_cpm
        global_gene_series['cpm_bg'] = down_cpm_bg
        global_gene_series['idx'] = global_gene_series.index
        #global_hits_df = global_hits_df.append(global_gene_series)
        global_hits_df = pd.concat([global_hits_df, global_gene_series], ignore_index=True)

        #save to csv file: up-regulation gene 
        global_gene_series = annot_df[annot_df['gene_names'].isin(gene_seq[up_keep_genes_idx])].set_index('idx').sort_index()
        global_gene_series['region'] = e
        global_gene_series['num_cell'] = BIN
        global_gene_series['bin'] = BIN
        global_gene_series['log(pval)-hypergeom'] = up_p_hypergeom
        global_gene_series['Significance_score'] = up_padj_list
        global_gene_series['fc_by_rand_dist_cpm'] = up_hit_fc_list
        #global_gene_series['pval-empirical'] = emp_pval_up
        global_gene_series['cpm_perturb'] = up_cpm
        global_gene_series['cpm_bg'] = up_cpm_bg
        global_gene_series['idx'] = global_gene_series.index
        #global_hits_df = global_hits_df.append(global_gene_series)
        global_hits_df = pd.concat([global_hits_df, global_gene_series], ignore_index=True)

    global_hits_df = global_hits_df.reindex(columns=df_column_list)
    rem_dup_global_hits_df = global_hits_df[~global_hits_df['gene_names'].isin(duplicate_elements)]

    if OUTPUT_DF.endswith('.csv'):
        rem_dup_global_hits_df.to_csv(OUTPUT_DF)
    else:
        rem_dup_global_hits_df.to_csv(OUTPUT_DF + '.csv')

    logger.info('Job is done.')
    
if __name__ == '__main__':
    pass
