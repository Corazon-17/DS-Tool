import streamlit as st  
import streamlit.components.v1 as components

st.set_page_config(page_title="Home")

try:
	dataset = st.session_state["dataset"]
	list_data = st.session_state["list_data"] + dataset.list()
except:
	st.session_state["list_data"] = ["-"]
	list_data = st.session_state["list_data"]

st.title("Welcome to DS-Tool! 👋")
st.markdown("""
	DS-Tool is an open source app to help people to do some machine learning techniques 
	such as exploratory data, preprocessing and model building. The most interesting part
	about this app is that you can do all of those things **WITHOUT CODE**.
	""")

st.header("What Do We Have ? 🧐")
with st.expander("1. Dataset"):
	st.markdown("""
		
		- **Read Dataset**
		In this app, you can read multiple dataset from various sources. You can upload dataset
		from your computer, read dataset from github raw file url, and enter (or copy-paste)
		your dataset manually. We also provided some sample data in this app that you can use.

		- **Split Dataset**
		When building machine learning model, we usually need to split our dataset into training
		and test set (we also need validation set sometimes). That's why we also provide dataset
		splitter to deal with that problem.

		- **Download Dataset**
		You can also download your dataset again after doing some preprocessing or data cleaning.
		""")

with st.expander("2. Dataframe"):
	st.markdown("""
		
		- **Display**
		Display your dataset in dataframe structure, which is 2-dimensional table of rows and columns 
		much like a spreadsheet. 
		
		- **Information**
		Every important information you need to know about your dataset such as total column, column name,
		total of non-null values, percentage of null values, total of unique values, column data type and 
		memory needed to store your dataset.

		- **Statistics**
		Descriptive statistics include those that summarize the central tendency, dispersion and shape of 
		a dataset’s distribution.

		- **Correlation**
		Measure the size and direction of a relationship between two or more variables in your dataset.
		Here, you can use 3 different method to measure the correlation coefficient, i.e. pearson, kendall 
		and spearman. You can also display the correlation value in a table, heatmap and feature pair.

		- **Duplicate**
		Check if there's duplicate data in your dataset.

		- **Group**
		Group your data by variable(s) or column(s) and then apply aggregate function.
		""")

with st.expander("3. Exploratory Data"):
	st.markdown("""
		Exploratory Data Analysis (EDA) is used to analyze the data to discover trends and paterns, so we can get
		better understanding of the bigger picture and insights of the data. EDA is often performed with the help 
		of several data visualization techniques. 

		In this app, we provide some data visualization techniques that
		you can use to explore the data i.e. Bar Plot, Pie Plot, Count Plot, Histogram, Box Plot, Violin Plot, Scatter Plot, 
		Regression Plot and Line Plot.

		""")

with st.expander("4. Feature Engineering"):
	st.markdown("""
		Feature engineering is mandatory process to prepare an input data that best fits the machine learning algorithms, 
		by selecting, manipulating and transforming the most relevant features from existing data.  It helps to represent an 
		underlying problem to predictive models in a better way, which as a result, improve the accuracy of the model for 
		unseen data. 

		There are few feature engineering techniques that you can use in this app:


		- **Add/Modify**
		First technique you can do is adding or modify a feature. We have provided some method for you to do that, i.e. using
		mathematical operation between features, extracting pattern from text, or grouping variable values.

		- **Change Dtype**
		Data sometimes stored in the wrong type, therefore we need to change it first before further processing. Reducing 
		the bit length of a variable can also save more memory and speed up the training process. But we need to be careful 
		when doing this because we may lose information from that variable which results in lower accuracy.

		- **Imputation**
		Imputation is the process to deal with missing values. You can fill missing values in a variable with it's mean or 
		median value (for numerical variable), with it's mode (for categorical variable), or with a constant value you choose. 

		- **Encoding**
		Machine learning models require all input to be numeric, hence we need to encode all categorical variables. To do this,
		we have provided 3 feature encoding methods that is Ordinal Encoding, One-Hot Encoding and Target Encoding.

		- **Scaling**
		Feature scaling is the process of scaling the values of features in a dataset so that they will be in the same range of values.
		To do this, we have also provided 3 feature scaling methods that is Standard Scaling (Standardization), Min-Max Scaling and Robust Scaling

		- **Drop Column**
		Finally, you can drop or remove unnecessary variables from your dataset before feeding the dataset into machine learning model.

		""")


with st.expander("5. Pipeline"):
	st.markdown("""
		Do you remember that in machine learning, we split our dataset into training and test set. In the preprocessing step, we only working 
		with out training set. So how to ensure that we do exactly the same process for our test data? Yes, Pipeline. A pipeline is a linear 
		sequence of data preparation, modeling, and prediction to codify and automate the workflow it takes to produce a machine learning model. 

		In this app, we will only use pipeline in the preprocessing step. You can choose whether to add the feature engineering process
		into the pipeline or not, and then you can use the stored process in the pipeline to transform other data with the same process sequentially.

		""")

with st.expander("6. Model Building"):
	st.markdown("""
		After your dataset is ready, the next step is to build machine learning model. And after building a model, we can find out the performance of 
		our model using metrics. There are some different metrics that we can use depends on the problem we want to solve.

		In this app, currently we only provide some classification algorithm. We will add more algoritms soon, including other algorithms 
		to handle the different task or problem e.g. regression and clustering. 

		""")


def expander_label(idx):
	hvar = f"""<script>
				var elements = window.parent.document.querySelectorAll('.streamlit-expanderHeader');
				elements[{idx}].style.color = 'rgba(255, 255, 255, 1)';
				elements[{idx}].style.fontFamily = 'sans-serif';
				elements[{idx}].style.fontSize = 'large';
			</script>"""

	components.html(hvar, height=0, width=0)

for idx in range(6):
	expander_label(idx)