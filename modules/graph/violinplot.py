import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 

from modules import utils

def violinplot(data):
	num_var = utils.get_numerical(data, add_hypen=True)
	low_cardinality = utils.get_low_cardinality(data, add_hypen=True)

	col1, col2, col3, col4 = st.columns([2.7, 2.7, 2.7, 1.9])
	num = col1.selectbox(
			"Numerical Variable",
			num_var,
			key="violin_num_var"
		)

	cat = col2.selectbox(
			"Categorical Variable",
			low_cardinality,    
			key="violin_cat_var"
		)
	
	hue = col3.selectbox(
			"Hue",
			low_cardinality,   
			key="violin_hue"
		)

	orient = col4.selectbox(
			"Orientation",
			["Vertical", "Horizontal"],
			index=1,
			key="violin_orient"
		)

	col1, col2, col3, _ = st.columns([1.5, 1.5, 1.5, 5.5])
	set_title = col1.checkbox("Title", key="violin_set_title")
	dodge = col2.checkbox("Dodge", True, key="violin_dodge")
	split = col3.checkbox("Split", key="violin_split")

	if num != "-":
			fig, ax = plt.subplots()

			cat = None if (cat == "-") else cat
			hue = None if (hue == "-") else hue
			if cat == hue:
				split = False 

			if set_title:
				default_title = f"Violinplot of {num} by {cat}"

				if hue:
					default_title = f"Violinplot of {num} by {cat} and {hue}"

				title = st.text_input(
						"Input title",
						default_title,
						key="violin_title"
					)

				ax.set_title(title)

			if orient == "Vertical":
				if cat:
					ax = sns.violinplot(data=data, x=cat, y=num, hue=hue, dodge=dodge, split=split)
				else:
					ax = sns.violinplot(data=data, y=num, hue=hue, dodge=dodge, split=split)
			else:
				if cat:
					data[cat] = [str(cat) for cat in data[cat]]
					ax = sns.violinplot(data=data, x=num, y=cat, hue=hue, dodge=dodge, split=split)
				else:
					ax = sns.violinplot(data=data, x=num, hue=hue, dodge=dodge, split=split)

			st.pyplot(fig)