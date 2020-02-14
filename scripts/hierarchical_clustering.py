#!/bin/env python3

import argparse
import pandas as pd
from sklearn.preprocessing import normalize
import scipy.cluster.hierarchy as shc
from scipy.cluster.hierarchy import fcluster

parser = argparse.ArgumentParser()
parser.add_argument('--source', help='File to load')
args = parser.parse_args()
file = args.source

# Load data from .json or .json.gz file
data = pd.read_table(file, index_col=0, header=None).T

# Use column headers as labels
labels = data.columns

# Get data as numpy array and transpose
values = data.values.transpose()

# Normalize the data
values = normalize(values)

# Perform clustering
linkage = shc.linkage(values, method='ward')

# Generate a list of dendrogram cutoff values
cutoff_values = [int(100 * c) / 100 for c in linkage[:, 2]]

# Generate cluster assignments at different cutoff values
cluster_assignments = [fcluster(linkage, c, criterion='distance') for c in cutoff_values]

# Write results to stdout
cluster_assignments = pd.DataFrame(cluster_assignments, index=cutoff_values, columns=labels)
print(cluster_assignments.to_csv(sep='\t', index=True))

### known issue: result may include a very large number of redundant lines
### temporarily solving by piping the output through uniq (in docket_study)