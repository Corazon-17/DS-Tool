import streamlit as st

from sklearn.svm import SVC

def svm():
	gamma, degree = "scale", 3

	col1, col2, col3 = st.columns(3)
	C = col1.number_input(
			"C",
			0.01, 1000.0, 1.0, 0.01,
			format="%f",
			key="svm_c"
		)

	kernel = col2.selectbox(
			"Kernel",
			["linear", "poly", "rbf", "sigmoid"],
			2, # default value index (rbf)
			key="svm_kernel"
		)

	tol = col3.number_input(
			"Tolerance (ε)",
			0.000001, 170.0, 0.001, 0.001,
			format="%f",
			key="svm_tol"
		)

	col1, col2, col3 = st.columns(3)
	if kernel != "linear":
		gamma = col1.selectbox(
				"Gamma",  
				["scale", "auto", "value"],
				key="svm_gamma"
			)

		if gamma == "value":
			gamma_val = col2.number_input(
					"Gamma Value",
					0.000001, 1000000.0, 0.1, 0.01,
					key="svm_gamma_val"
				)

			gamma = gamma_val

			if kernel == "poly":
				degree = col3.number_input(
						"Polinomial Degree",
						1, 100, 3, 1,
						key="svm_degree"
					)

		else:
			if kernel == "poly":
				degree = col2.number_input(
						"Polinomial Degree",
						1, 100, 3, 1,
						key="svm_degree"
					)

	model = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, tol=tol)

	return model