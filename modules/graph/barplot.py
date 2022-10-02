import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def barplot(data):
	num_var = utils.get_numerical(data, add_hypen=True)
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)

	col1, col2, col3, col4 = st.columns([2.7, 2.7, 2.7, 1.9])
	cat = col1.selectbox(
				"Categorical Variable",
				low_cardinality,    
				key="bar_cat_var"
			)

	num = col2.selectbox(
				"Numerical Variable",
				num_var,
				key="bar_num_var"
			)

	hue = col3.selectbox(
				"Hue",
				low_cardinality,   
				key="bar_hue"
			)

	orient = col4.selectbox(
				"Orientation",
				["Vertical", "Horizontal"],
				key="bar_orient"
			)

	col1, col2, col3, _ = st.columns([1.5, 1.8, 1.5, 5.5])
	set_title = col1.checkbox("Title", key="bar_set_title")
	set_errorbar = col2.checkbox("Error Bar", True, key="bar_errorbar")
	annot = col3.checkbox("Annotate", key="bar_annotate")

	if cat != "-" and num != "-":
		fig, ax = plt.subplots()

		hue = None if (hue == "-") else hue
		errorbar = ("ci", 95) if set_errorbar else None

		if set_title:
			default_title = f"{num} by {cat}"

			if hue:
				default_title = f"{num} by {cat} and {hue}"

			title = st.text_input(
					"Input title",
					default_title,
					key="bar_title"
				)

			ax.set_title(title)

		if orient == "Vertical":
			try:
				data[cat] = data[cat].astype(int)
			except:
				pass
			ax = sns.barplot(data=data, x=cat, y=num, hue=hue, errorbar=errorbar)
		else:
			data[cat] = data[cat].astype(str)
			order = sorted(data[cat].unique())
			ax = sns.barplot(data=data, x=num, y=cat, hue=hue, order=order, errorbar=errorbar)

		if annot:
			if orient == "Vertical":
				for bar in ax.patches:
					ax.annotate(format("{:.3f}".format(bar.get_height())),
				            (bar.get_x()+0.5*bar.get_width(),
				            bar.get_height()), ha='center', va='center',
				            size=11, xytext=(0, 8),
				            textcoords='offset points'
				        )
			else:
				for rect in ax.patches:
					plt.text(1.05*rect.get_width(), 
							rect.get_y()+0.5*rect.get_height(),
				            '%.3f' % float(rect.get_width()),
				            ha='center', va='center'
				        )

		st.pyplot(fig)