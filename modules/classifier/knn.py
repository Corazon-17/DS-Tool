import streamlit as st  

from sklearn.neighbors import KNeighborsClassifier

def knn():
	col1, col2, col3 = st.columns(3)
	n_neighbors = col1.number_input(
			"Number of Neighbors",
			1,100,3,   
			key="knn_neighbors"
		)
	weights = col2.selectbox(
			"Weight Function",
			["uniform", "distance"],
			key="knn_weight"
		)
	metric = col3.selectbox(
			"Distance Metric",
			["minkowski", "euclidean", "manhattan"]
		)

	model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, metric=metric)

	return model