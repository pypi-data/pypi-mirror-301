import numpy as np
import pandas as pd
import time


class Ensembling:

    def __init__(self, model_zoo, base_models, model_list=["LogRegression"]):
        self.model_list = model_list
        self.base_models = base_models
        self.model_zoo = model_zoo

    def runEnsemble(self,performance,shape):
        result = []

        Y_preds = []
        for model_name in self.model_list:
            model = self.base_models[model_name](performance=performance,shape=shape)

            start = time.time()
            model = self.model_zoo.model_fit(model)
            Y_pred, Y_pred_classes = self.model_zoo.model_predict(model)
            end = time.time()

            Y_preds.append(Y_pred)
            result.append({"Model": model_name,
                           "Class_probabilities": Y_pred,
                           "Classes": Y_pred_classes,
                           "Elapsed_Time": end - start,
                           })

        # Averaging results
        Y_pred = np.mean(Y_preds, axis=0)
        Y_pred_df = pd.DataFrame(Y_pred)
        Y_pred_df["grade"] = Y_pred_df.idxmax(axis=1)
        Y_pred_classes = Y_pred_df["grade"]

        return Y_pred, Y_pred_classes, result
