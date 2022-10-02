import streamlit as st

from sklearn.linear_model import LogisticRegression

def log_reg():
	col1, col2, col3 = st.columns(3)
	with col1:
		penalty = st.selectbox(
				"Penalty",
				["none", "l2", "l1", "elasticnet"],
				1, # default value index (rbf)
				key="lr_penalty"
			)

		solver = st.selectbox(
				"Penalty",
				["newton-cg", "lbfgs", "liblinear", "sag", "saga"],
				1, # default value index (rbf)
				key="lr_solver"
			)

	with col2:
		C = st.number_input(
				"C",
				0.01, 1000.0, 1.0, 0.01,
				format="%f",
				key="lr_c"
			)

		max_iter = st.number_input(
				"Max Iteration",
				1, 1000000, 100,
				key="lr_max_iter"
			)

	with col3:
		tol = st.number_input(
				"Tolerance (ε)",
				0.000001, 170.0, 0.0001, 0.0001,
				format="%f",
				key="lr_tol"
			)

		random_state = st.number_input(
				"Random State",
				0, 1000000, 0,
				key="lr_random_state"
			)

	model = LogisticRegression(penalty=penalty, C=C, tol=tol, solver=solver, max_iter=max_iter, random_state=random_state)

	return model