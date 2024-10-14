import os
import pandas as pd
from ..visualization import *
from ..path import *
from ..utils import *


def custom_sample(df, sample_filter, sample_count=None, breakdown_column=None, sample_columns=None, output_file_name=None, random_state=None):
	"""
	Custom sample the dataframe
	:param df: input dataframe
	:param sample_filter: sample filter
	:param sample_count: sample size
	:param breakdown_column: breakdown column
	:param sample_columns: sample columns
	:param output_file_name: output name
	:param random_state: random state
	return: sample dataframe
	"""
	sample_filter = " & ".join([f"{k} == {v}" for k, v in sample_filter.items()])
	if sample_columns is None:
		sample_columns = df.columns.tolist()
	if sample_count is None:
		sample_count = 20
		print(f">>>> Sample size is not specified, use default value {sample_count}")
	path = get_output_dir()
	if output_file_name is None:
		sample_result_path = path + f'/{sample_filter}_sampled_{sample_count}.csv'
	else:
		sample_result_path = path + f'/{output_file_name}.csv'

	# sample based on breakdown_column 
	if breakdown_column is not None:
		sample_df = df[sample_columns].groupby(breakdown_column).apply(lambda x: x.query(sample_filter).sample(sample_count, random_state=random_state)).reset_index(drop=True)
	else:
		sample_df = df[sample_columns].query(sample_filter).sample(sample_count, random_state=random_state)
	save_df_to_csv(sample_df, sample_result_path)
	return sample_df