


import sklearn.datasets
import pandas as pd
import seaborn
import matplotlib.pyplot as plt

cal_housing = sklearn.datasets.fetch_california_housing()


cal_df = pd.DataFrame(cal_housing.data, columns = cal_housing.feature_names)
cal_target = cal_housing.target

# gets count, mean, std, quantiles for each variable
cal_df.describe()

seaborn.scatterplot(cal_df)
plt.hist(cal_df)