import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def countplot(data):
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)

	col1, col2, col3 = st.columns([4,4,2])
	var = col1.selectbox(
				"Categorical Variable",
				low_cardinality,    
				key="count_var"
			)

	hue = col2.selectbox(
				"Hue",
				low_cardinality,   
				key="count_hue"
			)

	orient = col3.selectbox(
				"Orientation",
				["Vertical", "Horizontal"],
				key="count_orient"
			)

	col1, col2, _ = st.columns([1.5,1.5,7])
	set_title = col1.checkbox("Title", key="count_set_title")
	annot = col2.checkbox("Annotate", True, key="count_annot")

	if var != "-":
		fig, ax = plt.subplots()

		if hue == "-":
			hue = None

		if set_title:
			title = st.text_input(
					"Input title",
					f"{var} Count",
					key="count_title"
				)

			ax.set_title(title)
			ax.title.set_position([.5, 1.5])

		if orient == "Vertical":
			ax = sns.countplot(data=data, x=var, hue=hue)
		else:
			ax = sns.countplot(data=data, y=var, hue=hue)

		if annot:
			if orient == "Vertical":
				for bar in ax.patches:
					ax.annotate(format(int(bar.get_height())),
				            (bar.get_x()+0.5*bar.get_width(),
				            bar.get_height()), ha='center', va='center',
				            size=11, xytext=(0, 8),
				            textcoords='offset points'
			            )
			else:
				for rect in ax.patches:
					plt.text(1.05*rect.get_width(), 
							rect.get_y()+0.5*rect.get_height(),
				            '%d' % int(rect.get_width()),
				            ha='center', va='center'
			            )

		st.pyplot(fig)