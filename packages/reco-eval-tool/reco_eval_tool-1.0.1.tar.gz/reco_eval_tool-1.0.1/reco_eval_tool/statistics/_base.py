import os
import pandas as pd
from ..visualization import *
from ..path import *
from ..utils import *

COUNT = 'Count'
RATIO = 'Ratio'

def single_feature_analysis(df, column, is_drop_na=True, path=None):
	"""
	Analyze the single feature
	:param df: DataFrame
	:param column: column name
	:param is_drop_na: drop the rows with no value
	:return: analysis
	"""
	if path is None:
		path = get_output_dir()
	bar_graph_path = path + f'/{column}_bar_plot.png'
	pie_graph_path = path + f'/{column}_pie_plot.png'
	distribution_result_path = path + f'/{column}_distribution.csv'
	
	if is_drop_na:
		df = drop_na(df, [column])
	feature_analysis = df.groupby(column)[column].value_counts().reset_index(name=COUNT)
	total_count = feature_analysis[COUNT].sum()
	feature_analysis[RATIO] = feature_analysis[COUNT] / total_count

	bar_plot(data=feature_analysis, xlabel=column, ylabel=COUNT, title=f'Distribution of {column}', path=bar_graph_path)
	pie_plot(data=feature_analysis, labels=feature_analysis[column], sizes=feature_analysis[COUNT], title=f'Distribution of {column}', path=pie_graph_path)

	save_df_to_csv(feature_analysis, distribution_result_path)
	return feature_analysis


def pivot_table(df, column1, column2, is_drop_na=True, path=None):
	"""
	Create a pivot table for two columns
	:param df: DataFrame
	:param column1: column name
	:param column2: column name
	:param is_drop_na: drop the rows with no value
	:param path: path to save the result
	:return: analysis
	"""
	if path is None:
		path = get_output_dir()
	pivot_count_path = path + f'/{column1}_{column2}_pivot_count_plot.png'
	pivot_ratio_path = path + f'/{column1}_{column2}_pivot_ratio_plot.png'
	result_path = path + f'/{column1}_{column2}_pivot_table.csv'

	if is_drop_na:
		df = drop_na(df, [column1, column2])

	pivot_analysis = df.groupby([column1, column2]).size().reset_index(name=COUNT)
	pivot_analysis = pivot_analysis.sort_values(by=COUNT, ascending=False)
	total_count = pivot_analysis[COUNT].sum()
	pivot_analysis[RATIO] = pivot_analysis[COUNT] / total_count
	pivot_bar_plot(data=pivot_analysis, index=column1, columns=column2, values=COUNT, title=f'Count distribution of {column1} and {column2}', path=pivot_count_path)
	pivot_bar_plot(data=pivot_analysis, index=column1, columns=column2, values=RATIO, title=f'Ratio distribution of {column1} and {column2}', path=pivot_ratio_path)
	save_df_to_csv(pivot_analysis, result_path)
	return pivot_analysis


def feature_shift_analysis(df, column1, column2, is_drop_na=True, path=None):
	"""
	Analyze the shift of two columns
	:param df: DataFrame
	:param column1: column name
	:param column2: column name
	:param is_drop_na: drop the rows with no value
	:param path: path to save the result
	:return: analysis
	"""
	COLUMN1_TOTAL = f'{column1}_Total'
	COLUMN1_SHIFT_RATIO = f'{column1}_shift_ratio'
	SHIFT = 'Shift'

	if path is None:
		path = get_output_dir()
	shift_count_path = path + f'/{column1}_{column2}_detail_shift_count_plot.png'
	shift_ratio_path = path + f'/{column1}_{column2}_detail_shift_ratio_plot.png'
	overall_shift_graph_path = path + f'/{column1}_{column2}_overall_shift_ratio_plot.png'
	overall_shift_path = path + f'/{column1}_{column2}_overall_shift_table.csv'
	detail_shift_path = path + f'/{column1}_{column2}_detail_shift_table.csv'

	if is_drop_na:
		df = drop_na(df, [column1, column2])

	df[SHIFT] = df[column1] != df[column2]
	overall_shift = df[SHIFT].value_counts().reset_index(name=COUNT)
	overall_shift[RATIO] = overall_shift[COUNT] / overall_shift[COUNT].sum()
	pie_plot(data=overall_shift, labels=overall_shift[SHIFT], sizes=overall_shift[COUNT], title=f'Overall shift distribution of {column1} and {column2}', path=overall_shift_graph_path)
	save_df_to_csv(overall_shift, overall_shift_path)

	shift_analysis = df.groupby([SHIFT, column1, column2]).size().reset_index(name=COUNT)
	shift_analysis = shift_analysis.sort_values(by=COUNT, ascending=False)
	# total_count = shift_analysis[COUNT].sum()
	# shift_analysis[RATIO] = shift_analysis[COUNT] / total_count

	column1_df = shift_analysis.groupby([column1])[COUNT].sum().reset_index()
	column1_df = column1_df.rename(columns={COUNT: COLUMN1_TOTAL})
	shift_analysis = pd.merge(shift_analysis, column1_df, on=column1, how='left')
	shift_analysis[COLUMN1_SHIFT_RATIO] = shift_analysis[COUNT] / shift_analysis[COLUMN1_TOTAL]

	pivot_bar_plot(data=shift_analysis, index=column1, columns=column2, values=COUNT, title=f'Count distribution of {column1} and {column2}', path=shift_count_path)
	# pivot_bar_plot(data=shift_analysis, index=column1, columns=column2, values=RATIO, title=f'Ratio distribution of {column1} and {column2}', path=shift_ratio_path)
	pivot_bar_plot(data=shift_analysis, index=column1, columns=column2, values=COLUMN1_SHIFT_RATIO, title=f'Shift ratio distribution of {column1} and {column2}', path=shift_ratio_path)
	
	save_df_to_csv(shift_analysis, detail_shift_path)
	return shift_analysis

def calculate_shift_ratio(df, column1, column2):
	column1_df = df.groupby([column1])[COUNT].sum().reset_index()
	column1_df = column1_df.rename(columns={COUNT: f'{column1}_Total'})
	df = pd.merge(df, column1_df, on=column1_df, how='left')
	RATIO = f'{column1}_shift_ratio'
	df[RATIO] = df[COUNT] / df[f'{column1}_Total']
	return df

