import streamlit as st  
import pandas as pd

from modules import utils

def info(data):
	st.header("Dataset Information")
	
	row, col = data.shape
	info = pd.DataFrame({
				"Column": data.columns,
				"Non-Null": data.count(axis=0).to_list(),
				"Null Percentage": [f"{x:.2f} %" for x in data.isna().sum()/row*100],
				"Unique": utils.get_nunique(data),
				"Dtype": utils.get_dtypes(data)
			})

	dtypes = info.Dtype.value_counts()
	mem = data.memory_usage(deep=True).sum()
	if mem < 1024:
		mem = F"{mem}+ bytes"
	if mem < 1048576:
		mem = F"{(mem/1024).round(2)}+ KB"
	else:
		mem = f"{(mem/1024/1024).round(2)}+ MB"


	st.text(f"""
			{type(data)}
			RangeIndex: {row} entries, 0 to {row-1}
			Data columns (total {col} columns)
		""")
	st.dataframe(info)
	st.text(f"""
			dtypes: {", ".join([f"{i}({v})" for i, v in dtypes.items()])}
			memory usage: {mem}
		""")