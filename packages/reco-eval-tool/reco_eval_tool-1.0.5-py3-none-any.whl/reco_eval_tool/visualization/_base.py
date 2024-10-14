import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def bar_plot(data, xlabel=None, ylabel=None, title=None, path=None):
	"""Plot a bar plot."""
	# show number on the bar
	ax = sns.barplot(x=xlabel, y=ylabel, data=data)
	for p in ax.patches:
		p.set_height(p.get_height())
		ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), ha='center', va='bottom')
	plt.title(title)
	if path:
		plt.savefig(path)
		print(f">>>> Plot saved at {path}")
	else:
		print(">>>> No path provided, plot will not be saved.")


def pie_plot(data, labels=None, sizes=None, title=None, path=None):
	"""Plot a pie plot."""
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')
	plt.title(title)
	if path:
		plt.savefig(path)
		print(f">>>> Plot saved at {path}")
	else:
		print(">>>> No path provided, plot will not be saved.")


def pivot_bar_plot(data, index=None, columns=None, values=None, title=None, path=None):
	"""Plot a bar plot."""
	# show number on the bar
	data = data.pivot(index=index, columns=columns, values=values)
	ax = data.plot(kind='bar', stacked=False)
	for p in ax.patches:
		p.set_height(p.get_height())
		if 'ratio' in values.lower():
			ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d%%' % int(p.get_height() * 100), ha='center', va='bottom')
		else:
			ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), ha='center', va='bottom')
	plt.title(title)
	if path:
		plt.savefig(path)
		print(f">>>> Plot saved at {path}")
	else:
		print(">>>> No path provided, plot will not be saved.")



if __name__ == '__main__':
	import pandas as pd
	data = {'Market': ['en_us', 'en_us', 'zh_cn'], 'Prediction': [0, 1, 0], 'Count': [1, 1, 2]}
	df = pd.DataFrame(data)
	# single_bar_plot(df, 'Prediction', 'Count', 'Distribution of Prediction', 'Prediction_distribution.png')
	pivot_bar_plot(df, 'Market', 'Prediction', 'Distribution of Prediction', 'Prediction_distribution.png')