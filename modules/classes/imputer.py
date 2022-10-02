import pandas as pd

class Imputer:
    def __init__(self, strategy, columns=None, fill_value=None, group_col=None):
        """
        Limitation:
            - Supported strategy: mean, median, mode, constant
            - Columns must be defined when using group_col
            - Can only use 1 variable as group
        """

        self.strategy = strategy
        self.columns = columns
        self.fill_value = fill_value
        self.group_col = group_col
        self.unique_group_val = None

    def fit(self, X):
        if self.columns:
            if self.group_col:
                X = X[self.columns+[self.group_col]]
                self.unique_group_val = X[self.group_col].unique()
        else:
            X = X[columns]
        

        if self.strategy == "mean":
            self.__fill_mean(X)
        elif self.strategy == "median":
            self.__fill_median(X)
        elif self.strategy == "mode":
            self.__fill_mode(X)
        elif self.strategy == "constant":
            if self.columns:
                self.fill_value = {col: self.fill_value for col in self.columns}
            else:
                self.fill_value = self.fill_value


    def transform(self, X):
        X_temp = X.copy()

        if not self.group_col: # if group_val is empty
            X_temp[self.columns] = X_temp[self.columns].fillna(self.fill_value)
        else:
            for col in self.columns:
                for group_val in self.unique_group_val:
                    X_temp.loc[(X[col].isnull()) & (X_temp[self.group_col]==group_val), col] = self.fill_value[col][group_val]

        return X_temp

    def fit_transform(self, X):
        X_temp = X.copy()

        self.fit(X_temp)
        X_temp = self.transform(X_temp)

        return X_temp

    def __fill_mean(self, X):
        if not self.group_col:
            self.fill_value = X.mean(axis=0).to_dict()
        else:
            self.fill_value = X.groupby(self.group_col).agg("mean").to_dict()

    def __fill_median(self, X):
        if not self.group_col:
            self.fill_value = X.median().to_dict()
        else:
            self.fill_value = X.groupby(self.group_col).agg("median").to_dict()

    def __fill_mode(self, X):
        if not self.group_col:
            self.fill_value = X.mode().to_dict()
        else:
            self.fill_value = X.groupby(self.group_col).agg(pd.Series.mode).to_dict()