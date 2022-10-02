import streamlit as st

from sklearn.ensemble import RandomForestClassifier

def random_forest():
	max_depth = None
	col1, col2, col3 = st.columns(3)
	n_estimators = col1.number_input(
			"Number of Estimators",
			1, 1000000, 100,
			key="rf_n_estimators"
		)

	criterion = col2.selectbox(
			"Criterion",
			["gini", "entropy", "log_loss"],
			0, 
			key="rf_criterion"
		)

	min_samples_split = col3.number_input(
			"Min. Samples Split",
			2, 20, 2,
			key="rf_min_samples_split"
		)

	col1, col2, col3, col4 = st.columns([3.33, 2,1.33,3.33])
	min_samples_leaf = col1.number_input(
			"Min. Samples Leaf",
			1, 20, 1,
			key="rf_min_samples_leaf"
		)

	col3.markdown("#")
	auto_max_depth =  col3.checkbox("Auto", True, key="rf_auto_max_depth")
	if auto_max_depth:
		max_depth = col2.text_input(
			"Max Depth",
			"None",
			key="rf_max_depth_none",
			disabled=True
		)
	else:
		max_depth = col2.number_input(
			"Max Depth",
			1, 20, 7,
			key="rf_max_depth"
		)

	random_state = col4.number_input(
			"Random State",
			0, 1000000, 0,
			key="rf_random_state"
		)

	max_depth = None if auto_max_depth else max_depth
	model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=random_state)

	return model