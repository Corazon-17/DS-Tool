import streamlit as st  

from sklearn.tree import DecisionTreeClassifier

def decision_tree():
	max_depth = None
	col1, col2, col3 = st.columns(3)
	criterion = col1.selectbox(
			"Criterion",
			["gini", "entropy", "log_loss"],
			0, 
			key="dt_criterion"
		)

	min_samples_split = col2.number_input(
			"Min. Samples Split",
			2, 20, 2,
			key="dt_min_samples_split"
		)

	min_samples_leaf = col3.number_input(
			"Min. Samples Leaf",
			1, 20, 1,
			key="dt_min_samples_leaf"
		)

	col1, col2, col3, _ = st.columns([2,1.33,3.33,3.33])
	col2.markdown("#")
	auto_max_depth = col2.checkbox("None", True, key="dt_auto_max_depth")
	if auto_max_depth:
		max_depth = col1.text_input(
			"Max Depth",
			None,
			key="dt_max_depth_none",
			disabled=True
		)
	else:
		max_depth = col1.number_input(
			"Max Depth",
			1, 20, 7,
			key="dt_max_depth"
		)

	random_state = col3.number_input(
			"Random State",
			0, 1000000, 0,
			key="lr_random_state"
		)

	max_depth = None if auto_max_depth else max_depth
	model = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=random_state)

	return model