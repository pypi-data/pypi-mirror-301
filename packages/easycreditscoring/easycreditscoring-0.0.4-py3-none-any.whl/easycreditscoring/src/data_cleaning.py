import numpy as np
import pandas as pd
import re

# Pre-Processing
from sklearn.impute import KNNImputer
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.base import BaseEstimator, TransformerMixin


class DataCleaner():

    def __init__(self, df, target_column):

        self.df = df
        self.target_column = target_column

    def select_train(self):
        train_columns = self.df.columns.tolist()
        train_columns = [x for x in train_columns if x != self.target_column]

        return train_columns

    def clean_non_numerical(self, columns=[]):
        for column in columns:
            # Remove non-numeric characters
            self.df[column] = self.df[column].apply(lambda x: re.sub(r'[^0-9.]', '', str(x)))
            # Replace hex values with 10x numbers
            self.df[column] = self.df[column].apply(
                lambda x: int(x, 16) if isinstance(x, str) and x.startswith('0x') else x)
            # Replace empty strings with NaN
            self.df[column] = self.df[column].replace('', np.nan)
            # Convert dtype to float
            self.df[column] = self.df[column].astype(float)
            # Convert negatives like '-1' to NaN
            # df[df[column]<0] = df[df[column]<0].replace('', np.nan)
            # Convert dtype to float and coerce errors to NaN (invalid strings to NaN)
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')

        return self.df

    def categorical_to_onehot(self, columns=[]):
        for column in columns:
            unique_types = self.df[column].dropna().str.split(',').explode().str.strip().unique()

            # For each of value types:
            for i in self.df[column].value_counts().head(9).index[1:]:
                # Create a new column
                # Set value = 1 if the value type is present in the initial cell value, 0 otherwise
                self.df[column + "_" + i] = self.df[column].str.contains(i, na=False).astype(float)

            # Delete the original column after creating binary columns
            del self.df[column]
        return self.df

    def exists_or_not(self, columns=[]):
        for column in columns:
            # Replace empty strings with 0
            self.df[column] = self.df[column].replace('', 0)
            # Replace all other values with 1
            self.df.loc[self.df[column] != 0, column] = 1.0
            self.df[column] = self.df[column].astype(float)

        return self.df

    def select_missing_values(self, dataframe):
        selected_columns = dataframe.columns[dataframe.isna().any()].tolist()

        return selected_columns

    def knn_impute(self, n=5):

        # Apply KNN imputation to the specified column
        imputer = KNNImputer(missing_values=np.nan, n_neighbors=n)

        train_columns = self.select_train()
        selected_columns = self.select_missing_values(self.df[train_columns])

        self.df[selected_columns] = imputer.fit_transform(self.df[selected_columns])

        return self.df

    def remove_outliers(self, threshold):

        train_columns = self.select_train()

        ids = []
        for column in train_columns:
            z = np.abs(stats.zscore(self.df[column]))
            outlier_ids = np.where(z > threshold)[0]

            ids.extend(outlier_ids)

        ids = list(set(ids))
        self.df = self.df.drop(ids)

        return self.df


class ReduceVIF(BaseEstimator, TransformerMixin):
    def __init__(self, thresh=10):
        # Values between 5 and 10 can be considered acceptable.
        # Values above 10 are to be removed.
        self.thresh = thresh

    def fit(self, X, y=None):
        print('ReduceVIF fit')
        return self

    def transform(self, X, y=None):
        print('ReduceVIF transform')
        columns = X.columns.tolist()
        return ReduceVIF.calculate_vif(X, self.thresh)

    @staticmethod
    def calculate_vif(X, thresh=5.0):
        # Taken from https://stats.stackexchange.com/a/253620/53565 and modified
        dropped = True
        while dropped:
            variables = X.columns
            dropped = False
            vif = [variance_inflation_factor(X[variables].values, X.columns.get_loc(var)) for var in X.columns]

            max_vif = max(vif)
            if max_vif > thresh:
                maxloc = vif.index(max_vif)
                print(f'Dropping {X.columns[maxloc]} with vif={max_vif}')
                X = X.drop([X.columns.tolist()[maxloc]], axis=1)
                dropped = True
        return X
