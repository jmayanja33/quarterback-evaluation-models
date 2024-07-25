from tensorflow import keras
from keras.api.callbacks import EarlyStopping
from matplotlib import pyplot as plt
from Data.columns import dependent_variables
from Models.model import Model
import pandas as pd

# Set seed
keras.utils.set_random_seed(33)


class ANN(Model):

    def __init__(self, dependent_variable):
        model_type = "ANN"
        super().__init__(dependent_variable, model_type)

        # Initialize a regressor or classifier
        self.metric = None
        self.activation = None
        self.loss = None
        self.initialize_model()

    def initialize_model(self):
        """Function to initialize a model"""
        # Initialize a regressor model
        if dependent_variables[self.dependent_variable] == "regression":
            self.metric = "root_mean_squared_error"
            self.activation = None
            self.loss = "mean_squared_error"

        # Initialize a classifier
        else:
            self.metric = "accuracy"
            self.activation = "softmax"
            self.loss = "categorical_crossentropy"

        # Create model
        self.model = keras.Sequential([
            keras.layers.InputLayer(shape=(len(self.X_train.columns),)),
            keras.layers.Dense(16, activation='relu', name='hidden1'),
            keras.layers.Dense(16, activation='relu', name='hidden2'),
            keras.layers.Dense(1, name='output', activation=self.activation)
        ])

    def fit(self):
        """Function to find the best parameters with gridsearch CV and then fit a model"""
        self.logger.info(f"Fitting model for {self.model_type} {self.dependent_variable} model")

        # Setup early stopping
        early_stop = EarlyStopping(monitor="val_loss", mode="min", verbose=1, patience=3)

        # Compile and fit model
        self.model.compile(optimizer='adam', loss=self.loss, metrics=[self.metric])
        self.model.fit(self.X_train, self.y_train, epochs=2000, batch_size=2048, verbose=1,
                       validation_data=(self.X_test, self.y_test), callbacks=[early_stop])

        # Evaluate model
        self.plot_training_losses()
        predictions = self.model.predict(self.X_test)
        self.summary_report(predictions)

        # Save model
        self.save_model()

    def plot_training_losses(self):
        """Function to plot training losses"""
        self.logger.info("Plotting training losses")

        # Generate data
        losses = pd.DataFrame(self.model.history.history)

        # Plot data
        plt.figure(figsize=(10, 10))
        plt.plot(losses["loss"], label="Loss")
        plt.plot(losses["val_loss"], label="Val. Loss")
        plt.title(f"{self.dependent_variable} Training Loss")
        plt.legend()

        # Save figure
        plt.savefig(f"{self.dependent_variable}/TrainingStats/TrainingLoss.png")

    def save_model(self):
        """Function to save a model"""
        self.logger.info(f"Saving {self.model_type} {self.dependent_variable} model")
        self.model.save(f"{self.dependent_variable}/model.keras")

