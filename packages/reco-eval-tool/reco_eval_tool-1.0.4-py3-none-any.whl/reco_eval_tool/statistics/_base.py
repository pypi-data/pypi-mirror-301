import os
import pandas as pd
from ..visualization import *
from ..path import *
from ..utils import *

COUNT = 'Count'
RATIO = 'Ratio'
SHIFT = 'Shift'
GROUP_TOTAL = 'group_total'
GROUP_RATIO = 'group_ratio'
TOTAL_RATIO = 'total_ratio'
COLUMN1_COLUMN2 = 'column1_column2'

def single_feature_analysis(df, column, is_drop_na=True):
	"""
	Analyze the single feature
	:param df: DataFrame
	:param column: column name
	:param is_drop_na: drop the rows with no value
	:return: analysis
	"""
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


def pivot_table(df, column1, column2, is_drop_na=True):
	"""
	Create a pivot table for two columns
	:param df: DataFrame
	:param column1: column name
	:param column2: column name
	:param is_drop_na: drop the rows with no value
	:param path: path to save the result
	:return: analysis
	"""

	
	path = get_output_dir()
	pivot_count_path = path + f'/{column1}_{column2}_pivot_count.png'
	pivot_group_ratio_path = path + f'/{column1}_{column2}_pivot_group_ratio.png'
	pivot_total_ratio_path = path + f'/{column1}_{column2}_pivot_total_ratio.png'
	pivot_result_path = path + f'/{column1}_{column2}_pivot_table.csv'

	if is_drop_na:
		df = drop_na(df, [column1, column2])

	pivot_analysis = df.groupby([column1, column2]).size().reset_index(name=COUNT)
	pivot_analysis = pivot_analysis.sort_values(by=COUNT, ascending=False)
	total_count = pivot_analysis[COUNT].sum()
	pivot_analysis[TOTAL_RATIO] = pivot_analysis[COUNT] / total_count

	column1_df = pivot_analysis.groupby([column1])[COUNT].sum().reset_index()
	column1_df = column1_df.rename(columns={COUNT: GROUP_TOTAL})
	pivot_analysis = pd.merge(pivot_analysis, column1_df, on=column1, how='left')
	pivot_analysis[GROUP_RATIO] = pivot_analysis[COUNT] / pivot_analysis[GROUP_TOTAL]

	group_pivot_analysis = pivot_analysis.copy()
	group_pivot_analysis[COLUMN1_COLUMN2] = group_pivot_analysis[column1].astype(str) + "&" + group_pivot_analysis[column2].astype(str)
	pivot_bar_plot(data=pivot_analysis, index=column1, columns=column2, values=COUNT, title=f'Count of {column1} and {column2}', path=pivot_count_path)
	pivot_bar_plot(data=pivot_analysis, index=column1, columns=column2, values=GROUP_RATIO, title=f'Group Ratio  {column2}', path=pivot_group_ratio_path)
	pie_plot(data=group_pivot_analysis, labels=group_pivot_analysis[COLUMN1_COLUMN2], sizes=group_pivot_analysis[COUNT], title=f'Total Ratio of {column1} + {column2}', path=pivot_total_ratio_path)

	save_df_to_csv(pivot_analysis, pivot_result_path)
	return pivot_analysis


def feature_shift_analysis(df, column1, column2, gen_pivot_table=True, is_drop_na=True):
	"""
	Analyze the shift of two columns
	:param df: DataFrame
	:param column1: column name
	:param column2: column name
	:param gen_pivot_table: generate pivot table
	:param is_drop_na: drop the rows with no value
	:param path: path to save the result
	:return: analysis
	"""
	if gen_pivot_table:
		pivot_table(df, column1, column2, is_drop_na)

	path = get_output_dir()
	overall_shift_graph_path = path + f'/{column1}_{column2}_shift_ratio_plot.png'
	overall_shift_path = path + f'/{column1}_{column2}_shift_table.csv'

	if is_drop_na:
		df = drop_na(df, [column1, column2])

	df[SHIFT] = df[column1] != df[column2]
	overall_shift = df[SHIFT].value_counts().reset_index(name=COUNT)
	overall_shift[RATIO] = overall_shift[COUNT] / overall_shift[COUNT].sum()
	pie_plot(data=overall_shift, labels=overall_shift[SHIFT], sizes=overall_shift[COUNT], title=f'Shift of {column1} and {column2}', path=overall_shift_graph_path)
	save_df_to_csv(overall_shift, overall_shift_path)

	return overall_shift


