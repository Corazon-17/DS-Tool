import streamlit as st  

from sklearn.neural_network import MLPClassifier

def perceptron():
	col1, col2, col3 = st.columns(3)
	with col1:
		hidden_size = st.number_input(
				"Hidden Layer Size",
				1,3,1,
				key="perceptron_hidden_size"
			)

		alpha = st.number_input(
				"Alpha",
				1e-6, 100.0, 1e-4,
				key="perceptron_alpha",
				format="%f"
			)

	with col2:
		activation = st.selectbox(
				"Activation Function",
				["identity", "logistic", "tanh", "relu"],
				index=3,
				key="perceptron_activation"
			)

		learning_rate = st.number_input(
				"Learning Rate",
				1e-6, 1.0, 1e-3,
				key="perceptron_lr",
				format="%f"
			)

	with col3:
		max_iter = st.number_input(
				"Max Iteration",
				1, 1000000, 200,
				key="perceptron_max_iter"
			)

		tol = st.number_input(
				"Tolerance (ε)",
				1e-8, 1.0, 1e-4,
				format="%f",
				key="perceptron_tol"
			)

	cols = st.columns(3)
	hidden_layer_sizes = []
	for i in range(int(hidden_size)):
		neuron_size = cols[i].number_input(
				f"Layer {i+1} Neuron Size",
				1, 10000, 100,
				key=f"percenptron_neuron_size_{i}"
			)

		hidden_layer_sizes.append(neuron_size)

	model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, alpha=alpha, learning_rate_init=learning_rate, max_iter=max_iter, tol=tol)

	return model