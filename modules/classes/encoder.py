import category_encoders as ce 

class Encoder:
    def __init__(self, strategy: str, column: str, ordinal_dict=None, drop_first=False, target_var=None):
        """
        Limitation:
            - Supported strategy: ordinal, onehot, target
            - Only accept 1 column (str)
        """
        self.strategy = strategy
        self.column = column
        self.ordinal_dict = ordinal_dict
        self.drop_first = drop_first
        self.target_var = target_var

    def fit(self, X, target=None):
        if self.strategy == "onehot":
            self.encoder = ce.OneHotEncoder(cols=self.column, return_df=True, use_cat_names=True)
            self.encoder.fit(X)
        
        elif self.strategy == "target":
            self.encoder = ce.TargetEncoder(cols=self.column, return_df=True)
            self.encoder.fit(X[self.column], X[self.target_var])

    def transform(self, X):
        X_temp = X.copy()

        if self.strategy == "ordinal":
            X_temp[self.column] = X_temp[self.column].replace(self.ordinal_dict)
       
        elif self.strategy == "onehot":
            X_temp = self.encoder.transform(X_temp)

            if self.drop_first:
                first_label = f"{self.column}_{X_temp[self.column].unique()[0]}"
                X_temp = X_temp.drop(first_label, axis=1)

        elif self.strategy == "target":
            X_temp[self.column] = self.encoder.transform(X_temp[self.column])

        return X_temp  

    def fit_transform(self, X):
        X_temp = X.copy()
        
        self.fit(X)
        X_temp = self.transform(X_temp)

        return X_temp