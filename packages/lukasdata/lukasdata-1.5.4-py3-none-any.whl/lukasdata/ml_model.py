import os
from lukasdata.keras_input import keras_input
from matplotlib import pyplot as plt

class ml_model():
    def __init__(self,model,keras_input) -> None:
        self.model=model
        self.input=keras_input
        self.history=None
    def compile(self):
        self.model.compile(optimizer="adam")
    def fit(self,epochs,batch_size):
        self.history=self.model.fit(self.input.x_train, self.input.y_train, epochs=epochs, batch_size=batch_size, validation_data=(self.input.x_test, self.input.y_test))
    def save(self,file_name):
        os.chdir("C:/Users/lukas/Desktop/bachelor/models")
        self.model.save(file_name)
    def plot_metric(history,metrics_list):
        metrics_values_list=[]
        for metric in metrics_list:
            metrics_values_list.append(history.history[metric])
        for index,metric in enumerate(metrics_values_list):
            print(index)
            plt.subplot(1,2,1+index)
            plt.plot(metric,label=metrics_list[index])
            plt.title(metrics_list[index])
        plt.tight_layout()
        plt.show()   
    def init_input(self,group_name="idnr",entry_len=10,y_column_name="subsidized"):
        self.input=keras_input(self.df)
        self.input.create_grouped(group_name)
        self.input.create_array_from_grouped_df()
        self.input.create_y(y_column_name,entry_len)
        self.input.padding(entry_len)
        self.input.train_test_split()
    