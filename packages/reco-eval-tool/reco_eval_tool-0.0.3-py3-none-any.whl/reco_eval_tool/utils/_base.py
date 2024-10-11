import pandas as pd

def save_df_to_csv(df, path):
	df.to_csv(path, index=False)
	print(f">>>> save dataframe result to {path}")


def drop_na(df, columns):
	"""
	Drop the rows with na value in the columns
	:param df: DataFrame
	:param columns: list of column names
	:return: DataFrame
	"""
	all_rows = df.shape[0]
	df = df.dropna(subset=columns)
	drop_rows = all_rows - df.shape[0]
	print(f'>>>> all rows = {all_rows}, drop rows = {drop_rows} in {columns}')
	return df