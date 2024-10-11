import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,BatchNormalization
from tensorflow.keras.optimizers import Adam, Nadam, AdamW
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ReduceLROnPlateau


import pandas as pd


# Pre-Processing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import CategoricalNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelBinarizer

# Metrics
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import RocCurveDisplay

from abc import ABC, abstractmethod

class ModelPipeLine:

    def __init__(self, X_train, Y_train, X_test, Y_test):
        self.X_train = X_train
        self.Y_train = Y_train
        self.X_test = X_test
        self.Y_test = Y_test

        self.performance = "Light"

        self.base_models = {"LogRegression": LogRegression,
                            "DecisionTree": DecisionTree,
                            "RandomForest": RandomForest,
                            "GradientBoost": GradientBoost,
                            "Bayes": Bayes,
                            "NeuralNet": NeuralNet
                            }

    def scaling(self):
        scaler = MinMaxScaler()

        X_train_scaled = scaler.fit_transform(self.X_train)
        X_test_scaled = scaler.transform(self.X_test)

        self.X_train = pd.DataFrame(X_train_scaled, columns=self.X_train.columns)
        self.X_test = pd.DataFrame(X_test_scaled, columns=self.X_test.columns)

    def oversample(self):
        # SMOTE oversampling
        smote = SMOTE(sampling_strategy='auto', random_state=42)
        self.X_train, self.Y_train = smote.fit_resample(self.X_train, self.Y_train)

    def model_fit(self, abstract_model):
        abstract_model.fit(self.X_train, self.Y_train)
        return abstract_model

    def model_predict(self, abstract_model):
        Y_pred = abstract_model.predict_proba(self.X_test)
        Y_pred_df = pd.DataFrame(Y_pred)
        Y_pred_df["grade"] = Y_pred_df.idxmax(axis=1)
        Y_pred_classes = Y_pred_df["grade"]
        return Y_pred, Y_pred_classes

    def show_results(self, Y_pred_classes):
        matrix = confusion_matrix(self.Y_test, Y_pred_classes)
        print("Accuracy: ", matrix.diagonal() / matrix.sum(axis=1))
        disp = ConfusionMatrixDisplay(matrix)
        disp.plot()

    def showROC(self, Y_pred, class_id):
        label_binarizer = LabelBinarizer().fit(self.Y_train)
        y_onehot_test = label_binarizer.transform(self.Y_test)
        y_onehot_test.shape  # (n_samples, n_classes)

        display = RocCurveDisplay.from_predictions(
            y_onehot_test[:, class_id],
            Y_pred[:, class_id],
            name=f"Class #{class_id} vs the rest",
            color="darkorange",
            plot_chance_level=True,
        )
        _ = display.ax_.set(
            xlabel="False Positive Rate",
            ylabel="True Positive Rate",
            title="One-vs-Rest ROC curve",
        )

        micro_roc_auc_ovr = roc_auc_score(
            self.Y_test,
            Y_pred,
            multi_class="ovr",
            average="micro",
        )

        print(f"Micro-averaged One-vs-Rest ROC AUC score:\n{micro_roc_auc_ovr:.2f}")


class ClassicModel(ABC):

    def __init__(self, performance, shape):
        self.set_model(performance="Light", shape=shape)
        self.performance = performance

    def fit(self, X_train, Y_train):
        print("\n Using model: ", self.model)
        self.model.fit(X_train, Y_train)
        return self.model

    def predict_proba(self, X_test):
        Y_pred = self.model.predict_proba(X_test)
        return Y_pred

    @abstractmethod
    def set_model(self) -> None:
        pass


# Model Zoo

class LogRegression(ClassicModel):
    def set_model(self, performance, shape):
        self.model = LogisticRegression(solver='lbfgs', max_iter=3000, random_state=42)

    # Custom scorer function (convert it to work with make_scorer)
    def custom_scorer(estimator, X, Y):
        # Get predicted probabilities from the model
        y_pred_probs = estimator.predict_proba(X)

        # Return custom loss (as a positive value, since scorers maximize)
        return custom_loss_np(y, y_pred_probs)


class DecisionTree(ClassicModel):
    def set_model(self, performance, shape):
        self.model = tree.DecisionTreeClassifier()


class RandomForest(ClassicModel):
    def set_model(self, performance, shape):
        performance_levels = {
            "Light": {'n_estimators': 1, 'random_state': 42},
            "Medium": {'n_estimators': 50, 'random_state': 42},
            "High": {'n_estimators': 1000, 'random_state': 42}
        }
        self.model = RandomForestClassifier(**performance_levels[performance])


class GradientBoost(ClassicModel):
    def set_model(self, performance, shape):
        performance_levels = {
            "Light": {'n_estimators': 3, 'learning_rate': 1.0, 'max_depth': 3, 'random_state': 42},
            "Medium": {'n_estimators': 10, 'learning_rate': 1e-1, 'max_depth': 8, 'random_state': 42},
            "High": {'n_estimators': 20, 'learning_rate': 5e-2, 'max_depth': 10, 'random_state': 42},
        }
        self.model = GradientBoostingClassifier(**performance_levels[performance])


class Bayes(ClassicModel):
    def set_model(self, performance, shape):
        self.model = CategoricalNB()


class NeuralNet(ClassicModel):
    def set_model(self, performance, shape):
        self.performance = performance
        self.performance_levels = {
            "Light": {'epochs': 20, 'learning_rate': 1e-3},
            "Medium": {'epochs': 100, 'learning_rate': 1e-3},
            "High": {'epochs': 500, 'learning_rate': 1e-3},
        }

        model = Sequential([
            Dense(512, input_dim=shape, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.25),
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            Dense(3, activation='softmax')
        ])

        try:
            Economy
        except NameError:
            loss_function = "sparse_categorical_crossentropy"
        else:
            loss_function = Economy.custom_loss_tf

        model.compile(optimizer=Adam(learning_rate=self.performance_levels[performance]["learning_rate"]),
                      # loss='sparse_categorical_crossentropy',
                      loss=loss_function,
                      metrics=['accuracy'])

        self.model = model

    def fit(self, X_train, Y_train):
        X_train_tr, X_val, Y_train_tr, Y_val = train_test_split(
            X_train, Y_train, test_size=0.1, random_state=42)

        early_stopping = EarlyStopping(monitor='val_accuracy',
                                       patience=60,
                                       mode="auto",
                                       restore_best_weights=True)

        reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                      factor=0.5,  # Learning rate reduced by half if no improvement
                                      patience=10,  # Wait 10 epochs before reducing learning rate
                                      min_lr=1e-6,  # Minimum learning rate set
                                      verbose=1)

        history = self.model.fit(
            x=X_train_tr,
            y=Y_train_tr,
            validation_data=(X_val, Y_val),
            batch_size=1024,
            epochs=self.performance_levels[self.performance]["epochs"],
            verbose=0,
            callbacks=[early_stopping, reduce_lr])

    def predict_proba(self, X_test):
        Y_pred = self.model.predict(X_test)
        return Y_pred