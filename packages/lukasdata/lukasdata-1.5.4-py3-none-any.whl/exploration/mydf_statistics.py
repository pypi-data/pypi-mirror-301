import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os 
from matplotlib import pyplot as plt
import pandas as pd
from datahandling.change_directory import chdir_root_search



#design als attribute von einem df
class statistics():
    def __init__(self) -> None:
        self.df=None
        #self.ndarray=df.to_numpy()
        self.name=None
        self.mean=None
        self.median=None
        self.std=None
        self.nan_percentages=None
        self.numeric_df=None
        self.stats_dict=None
        self.column_stats_df=None
        self.df_stats_df=None
        self.numeric_and_datetime=None
    def build_nan_percentages(self):
        nan_df=self.df.isna()
        nan_dict={}
        df_len=len(self.df)
        sums=nan_df.sum(axis=0)
        percentages=sums.apply(lambda x: x/df_len)
        return percentages
    def create_hist_figs(self):
        #os.chdir(r"C:\Users\Lukas\Desktop\bachelor\data\figures\hist")
        chdir_root_search("hist")
        if not os.path.exists(self.name):
            os.makedirs(self.name)
        os.chdir(self.name)    
        for col in self.numeric_and_datetime:
            values=self.numeric_and_datetime[col]
            #values=np.log(values)
            bins=sturges_rule(values)
            plt.plot(label='Hist', color='blue',bins=bins)
            #range as a quantile maybe
            plt.hist(values) #len(np.unique(values))
            plt.title(f'{col}')
            plt.savefig(f"hist_{col}.png")
            plt.close()

        
    def create_kde_figs(self,log=False):
        #os.chdir(r"C:\Users\Lukas\Desktop\bachelor\data\figures\kde")
        chdir_root_search("kde")
        if not os.path.exists(self.name):
            os.makedirs(self.name)
        os.chdir(self.name)    
        column_names=self.numeric_and_datetime.columns
        for column_name in column_names:
            data=self.numeric_and_datetime[column_name]
            if log:
                data=np.log(data)
            sns.kdeplot(data, bw_method='scott')
    
    # Add labels and a title
            plt.xlabel('Data values')
            plt.ylabel('Density')
            plt.title('Kernel Density Estimate (Gaussian kernel, Scott bandwidth)')
            plt.savefig(f"kde_{column_name}.png")
            plt.close()
      
    def corr_heatmap(self,treshold):
        #array=np.array(self.numeric_df)
        #columns=self.numeric_df.columns
        #columns = [f'{self.df.columns[i]}' for i in range(self.ndarray.shape[1])]
        
        #df = pd.DataFrame(array, columns=columns)
        # Compute correlation matrix
        corr_matrix = self.numeric_df.corr()
        corr_matrix=corr_matrix[np.abs(corr_matrix)>=treshold]
        
        # Create a heatmap
        plt.figure(figsize=(8, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
        #sns.heatmap(corr_matrix, cmap="viridis")
        plt.title('Correlation Heatmap')
        #plt.plot()
        plt.show()
    def __str__(self):
        string=f"Df stats:{self.df_stats_df} \n Column stats:{self.column_stats_df}"
        return(string)
        


class statistics_builder():
    def __init__(self,df,name,map=None) -> None:
        self.df=df

        self.name=name
        if map!=None:
            self.map=map
        else:
            map={}
            for column in self.df.columns:
                map[column]=float
            self.map=map
        self.statistics=statistics()
    def build_statistics(self):
        self.statistics.df=self.df
        self.statistics.numeric_df=self.df.to_numeric()
        self.statistics.name=self.name
        self.statistics.numeric_and_datetime=self.df.to_dtype(self.map)
        descrpition=self.statistics.df.describe()
        #self.statistics.description=descrpition
        self.statistics.mean=descrpition.loc["mean"]
        self.statistics.min=descrpition.loc["min"]
        self.statistics.max=descrpition.loc["max"]
        self.statistics.std=descrpition.loc["std"]
        self.statistics.nan_percentages=self.statistics.build_nan_percentages()
        self.statistics.column_stats_dict={"mean":self.statistics.mean,"min":self.statistics.min,"max":self.statistics.max,"std":self.statistics.std,"nan_percentages":self.statistics.nan_percentages}
        df=pd.DataFrame(self.statistics.column_stats_dict)
        self.statistics.column_stats_df=df[df.isna().sum(axis=1)<4]
        self.statistics.df_stats_df=self.statistics.df.shape
        return self.statistics

def sturges_rule(data):
    n = len(data)
    return int(np.ceil(np.log2(n) + 1))

#grouped statistics
#groupby compcat und dann describe oder ausgewählte statistikn printen
#kann auch multiple columns nehmen
#value counts bei kategorialen daten
#kann ich irgendwie factor forcen?
#nan ppercentags im description df?
#factorization



