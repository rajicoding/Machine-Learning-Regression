class Univariate():
    import pandas as pd
    def quanqual(dataset):
        quan=[]
        qual=[]
        # Check columns one by one using for loop
        for columnName in dataset.columns:
            if(dataset[columnName].dtype=="O"):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan,qual
# Function to display frequency, relative_frequency and cummulative sum of the mentioned column   
    def freqtable(columnName,dataset):
        import pandas as pd
        freq_table = pd.DataFrame(columns=["Unique_values","frequency","relative_frequency","cumsum"])
        freq_table["Unique_values"] = dataset[columnName].value_counts().index
        freq_table["frequency"] = dataset[columnName].value_counts().values
        freq_table["relative_frequency"] = (freq_table["frequency"]/dataset[columnName].count())
        # dividing it  by dataset[columnName].count() will update the count according to number of values in the mentioned column  
        freq_table["cumsum"] = freq_table["relative_frequency"].cumsum()
        return freq_table
# Function to display univariate analysis of the given dataset   
    def univariate(dataset,quan):
        import pandas as pd
        import numpy as np
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR",
                                         "1.5rule","Lower","Upper","Min","Max"],columns=quan)
        for columnName in quan:
            descriptive.loc["Mean",columnName] = dataset[columnName].mean()
            descriptive.loc["Median",columnName] = dataset[columnName].median() 
            descriptive.loc["Mode",columnName] = dataset[columnName].mode()[0]
            descriptive.loc["Q1:25%",columnName] = dataset.describe()[columnName]["25%"]
            descriptive.loc["Q2:50%",columnName] = dataset.describe()[columnName]["50%"]
            descriptive.loc["Q3:75%",columnName] =  dataset.describe()[columnName]["75%"]
            descriptive.loc["Q4:100%",columnName] =  dataset.describe()[columnName]["max"]
            descriptive.loc["99%",columnName] =  np.percentile(dataset[columnName],99)
            descriptive.loc["IQR",columnName] = descriptive[columnName]["Q3:75%"] - descriptive[columnName]["Q1:25%"]
            descriptive.loc["1.5rule",columnName] = 1.5*descriptive[columnName]["IQR"]
            descriptive.loc["Lower",columnName] = descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5rule"]
            descriptive.loc["Upper",columnName] = descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5rule"] 
            descriptive.loc["Min",columnName] =  dataset.describe()[columnName]["min"]
            descriptive.loc["Max",columnName] =  dataset.describe()[columnName]["max"]
            descriptive.loc["skew",columnName] =  dataset[columnName].skew()
            descriptive.loc["kurtosis",columnName] =  dataset[columnName].kurtosis()
            descriptive.loc["Var",columnName] =  dataset[columnName].var()
            descriptive.loc["Std",columnName] =  dataset[columnName].std()
        return descriptive
# function to check missing values in quantitative columns from the dataset and replace them with median
    def quan_missingvalues(dataset,quan):
        for columnName in quan:
            if(dataset[columnName].isna().sum()>0):
                dataset.fillna({columnName:dataset[columnName].median()},inplace=True)
        return dataset
# Function to check missing values in categorical columns from the dataset and replace them with mode
    def qual_missingvalues(dataset,qual):
        for columnName in qual:
            if(dataset[columnName].isna().sum()>0):
                dataset.fillna({columnName:dataset[columnName].mode()[0]},inplace=True)
        return dataset
    
#Function to display columns which has lower and upper bound outliers
    def outliercolumns(quan,descriptive):
         lower = []
         upper = []
         for columnName in quan:
             if(descriptive[columnName]["Min"]<descriptive[columnName]["Lower"]):
                 lower.append(columnName)
             if(descriptive[columnName]["Max"]>descriptive[columnName]["Upper"]):
                 upper.append(columnName)
         return lower, upper
# Function to replace the outlier values with lower or upper bound value
    def replaceoutliers(dataset,descriptive,lower,upper,quan):
        for columnName in lower:
            dataset.loc[dataset[columnName] < descriptive.loc["Lower", columnName], columnName] = descriptive.loc["Lower", columnName]
        for columnName in upper:
            dataset.loc[dataset[columnName]>descriptive.loc["Upper",columnName], columnName]=descriptive.loc["Upper", columnName]
        return Univariate.univariate(dataset,quan)
# returning univariate analysis to check if min and max values of the outlier columns are replaced with lower and upper bound