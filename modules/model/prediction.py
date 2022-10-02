import streamlit as st  
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from modules import utils
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

def prediction(dataset, models):
	show = False
	col1, col2, col3 = st.columns(3)
	model_opt = col1.selectbox(
		"Select Model",
		models.list_name()
		)

	data_opt = col2.selectbox(
		"Select Data",
		dataset.list_name()
		)

	target_var = col3.selectbox(
		"Target Variable",
		models.target_var
		)

	if st.checkbox("Show Result"):
		data = dataset.get_data(data_opt)
		X, y = utils.split_xy(data, target_var)
		y_pred = models.get_prediction(model_opt, X)

		col1, col2 = st.columns(2)
		result_opt = col1.selectbox(
				"Result",
				["Target Value", "Accuracy", "Precision", "Recall", 
				 "F1-Score", "Classification Report", "Confusion Matrix"]
			)

		if y.nunique() > 2:
			multi_average = col2.selectbox(
					"Multiclass Average",
					["micro", "macro", "weighted"],
					key="prediction_multi_average"
				)
		else:
			multi_average = "binary"

		show_result(y, y_pred, result_opt, multi_average)

def show_result(y, y_pred, result_opt, multi_average):
	if result_opt in ["Accuracy", "Precision", "Recall", "F1-Score"]:
		metric_dict = {
				"Accuracy": accuracy_score(y, y_pred),
				"Precision": precision_score(y, y_pred, average=multi_average),
				"Recall": recall_score(y, y_pred, average=multi_average),
				"F1-Score": f1_score(y, y_pred, average=multi_average)
			}

		result = metric_dict.get(result_opt)
		st.metric(result_opt, result)

	elif result_opt == "Target Value":
		result = pd.DataFrame({
				"Actual": y,
				"Predicted": y_pred
			})

		st.dataframe(result)

	elif result_opt == "Classification Report":
		result = classification_report(y, y_pred)

		st.text("`"+result)

	elif result_opt == "Confusion Matrix":
		cm = confusion_matrix(y, y_pred)

		fig, ax = plt.subplots()
		ax = sns.heatmap(
				cm, annot=True, 
				fmt='.4g',
				xticklabels=np.unique(y_pred),
				yticklabels=np.unique(y_pred)
			)

		ax.set_title(result_opt)
		ax.set_xlabel("Predicted Label")
		ax.set_ylabel("Actual Label")

		st.pyplot(fig)