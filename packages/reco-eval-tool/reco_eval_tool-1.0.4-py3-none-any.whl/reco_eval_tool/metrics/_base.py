import pandas as pd
from ..utils import *
from ..path import *


def calculate_prf(df, ground_truth_colunm, predict_column, breakdown_column=None, is_drop_na=True):
	"""
	Calculate the precision, recall, F1 of the prediction
	:param df: input dataframe
	:param ground_truth_colunm: ground truth column
	:param predict_column: predict column
	:param breakdown_column: breakdown column
	:param is_drop_na: drop the rows with missing values in the ground_truth_colunm and predict_column
	"""
	# # check df is a pandas dataframe, ground_truth_colunm and predict_column, breakdown_column are in the df
	# assert isinstance(df, pd.DataFrame), "df should be a pandas dataframe"
	# assert ground_truth_colunm in df.columns, f"{ground_truth_colunm} should be in the dataframe"
	# assert predict_column in df.columns, f"{predict_column} should be in the dataframe"
	# if breakdown_column is not None:
	# 	assert breakdown_column in df.columns, f"{breakdown_column} should be in the dataframe"
	
	# remove rows with missing values in the two columns
	if is_drop_na:
		df = drop_na(df, [ground_truth_colunm, predict_column])

	# check the value of ground_truth_colunm and predict_column are in [0, 1]
	assert df[ground_truth_colunm].isin([0, 1]).all(), f"{ground_truth_colunm} should only contain 0 or 1"
	assert df[predict_column].isin([0, 1]).all(), f"{predict_column} should only contain 0 or 1"
	
	path = get_output_dir()
	if breakdown_column is None:
		prf_df = calculate_prf_single(df, ground_truth_colunm, predict_column)
		prf_df = prf_df.to_frame().T
		save_df_to_csv(prf_df, path + f'/{ground_truth_colunm}_{predict_column}_prf.csv')
	else:
		prf_df = df.groupby(breakdown_column).apply(lambda x: calculate_prf_single(x, ground_truth_colunm, predict_column)).reset_index()
		save_df_to_csv(prf_df, path + f'/{ground_truth_colunm}_{predict_column}_breakdown_{breakdown_column}_prf.csv')
	return prf_df


def calculate_prf_single(df, ground_truth_colunm, predict_column):
	"""
	Calculate the precision, recall, F1 of the prediction for a single group
	:param df: input dataframe
	:param ground_truth_colunm: ground truth column
	:param predict_column: predict column
	"""
	ground_truth = df[ground_truth_colunm].values.tolist()
	predict = df[predict_column].values.tolist()
	TP = 0
	FP = 0
	FN = 0
	for i in range(len(ground_truth)):
		if ground_truth[i] == 1 and predict[i] == 1:
			TP += 1
		elif ground_truth[i] == 0 and predict[i] == 1:
			FP += 1
		elif ground_truth[i] == 1 and predict[i] == 0:
			FN += 1
	TN = len(ground_truth) - TP - FP - FN
	if TP + FP == 0:
		precision = 0
	else:
		precision = TP / (TP + FP)
	if TP + FN == 0:
		recall = 0
	else:
		recall = TP / (TP + FN)
	if precision + recall == 0:
		f1 = 0
	else:
		f1 = 2 * precision * recall / (precision + recall)
	positive = sum(ground_truth)
	positive_ratio = positive / len(ground_truth)
	FPR = FP / (FP + TN)
	return pd.Series({'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN, 'precision': precision, 'recall': recall, 'f1': f1, 'positive': positive, 'positive_ratio': positive_ratio, 'FPR': FPR})
	