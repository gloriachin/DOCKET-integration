#!/bin/env python3

import argparse
import pandas as pd
import common.transform as transform
import common.file_io as io


def main(file,
         sep=None,
         comment=None,
         index_col=None,
         header_row=None,
         rows_out='rows_out.json.gz',
         cols_out='cols_out.json.gz'):

    assert isinstance(file, str)

    # Read data as a data frame
    data = pd.read_csv(file, sep=sep, comment=comment, index_col=index_col, header=header_row)

    # Drop columns with missing data
    data.dropna(axis=1, inplace=True)

    # Get row and column labels
    row_labels = list(data.index)
    col_labels = list(data.columns)

    # Convert to list of lists for subsequent processing
    data = data.values

    # Get data row-wise and column-wise in json format
    rowwise_data = transform.tabular2json(data, row_labels, col_labels, by_col=False, pad_rows=False)
    colwise_data = transform.tabular2json(data, row_labels, col_labels, by_col=True, pad_rows=True)

    # Write row-wise json
    io.write_json(rowwise_data, rows_out)

    # Write column-wise json
    io.write_json(colwise_data, cols_out)

    return rowwise_data, colwise_data


if __name__ == '__main__':
    # Parse command-line inputs
    parser = argparse.ArgumentParser()

    # File IO arguments
    parser.add_argument('--infile', help='File to load')
    parser.add_argument('--sep', help='Delimiter to use', default='\t')
    parser.add_argument('--comment', help='Comment line character', default=r'#')
    parser.add_argument('--index_col', help='Index of column to use as row labels', default=None)
    parser.add_argument('--header_row', help='Index of row to use as column labels', default=None)
    parser.add_argument('--rows_out', help='Output file for row data', default='rows_out.json.gz')
    parser.add_argument('--cols_out', help='Output file for column data', default='cols_out.json.gz')
    args = parser.parse_args()

    main(args.infile,
         sep=args.sep,
         comment=args.comment,
         index_col=None if args.index_col is None else int(args.index_col),
         header_row=None if args.header_row is None else int(args.header_row),
         rows_out=args.rows_out,
         cols_out=args.cols_out)
