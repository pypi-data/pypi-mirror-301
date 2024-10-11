import tensorflow as tf

import numpy as np



class UnitEconomy:
    """
    Clients with Poor credit score are rejected (i.e. no loan is issued).
    Depending on the correctness of risk evaluation each approved client results in the given profit or loss in arbitrary currency units (ACU):

    - Poor client evaluated as Standard yields loss of ACU 200.
    - Poor client evaluated as Good yields loss of ACU 400.

    - Standard client evaluated as Standard yields profit of ACU 50.
    - Standard client evaluated as Good yields profit of ACU 30.

    - Good client evaluated as Standard yields profit of ACU 70.
    - Good client evaluated as Good yields profit of ACU 100.

    - Each client evaluation regardless of outcome costs ACU 5.
    """

    def __init__(self, **kwargs):
        self.eval_cost = kwargs["eval_cost"]
        self.poor_as_standard = kwargs["poor_as_standard"]
        self.poor_as_good = kwargs["poor_as_good"]
        self.standard_as_standard = kwargs["standard_as_standard"]
        self.standard_as_good = kwargs["standard_as_good"]
        self.good_as_standard = kwargs["good_as_standard"]
        self.good_as_good = kwargs["good_as_good"]

        """
        COST-BENEFIT MATRIX:

        Actual type | Evaluated as Poor | Evaluated as Standard | Evaluated as Good
        ___________________________________________________________________________

        Poor        |        -5         |       -5-200          |      -5-400
        ___________________________________________________________________________

        Standard    |        -5         |       -5+50           |      -5+30
        ___________________________________________________________________________

        Good        |        -5         |       -5+70           |      -5+100
        ___________________________________________________________________________        
        """

        self.cost_benefit_matrix = np.array(
            [[-self.eval_cost, -self.eval_cost + self.poor_as_standard, -self.eval_cost + self.poor_as_good],
             [-self.eval_cost, -self.eval_cost + self.standard_as_standard, -self.eval_cost + self.standard_as_good],
             [-self.eval_cost, -self.eval_cost + self.good_as_standard, -self.eval_cost + self.good_as_good]])

    # NumPy version of custom loss function
    def custom_loss_np(self, Y_true, Y_pred):
        """
        Custom loss function to compute the profit or loss based on the cost-benefit matrix using NumPy.

        Args:
        Y_true: true class labels as a NumPy array (0 = Poor, 1 = Standard, 2 = Good)
        Y_pred: predicted class probabilities as a NumPy array (shape: [n_samples, n_classes])

        Returns:
        A scalar representing the average loss across all examples.
        """

        # Ensure Y_true is an integer array
        Y_true = np.squeeze(Y_true.astype(int))

        # Create one-hot encoding for true labels
        Y_true_one_hot = np.eye(len(self.cost_benefit_matrix))[Y_true]

        # Calculate expected loss
        expected_loss = np.sum(Y_pred * np.dot(Y_true_one_hot, self.cost_benefit_matrix), axis=1)

        return -np.mean(expected_loss)

    # TensorFlow version of custom loss function
    def custom_loss_tf(self, Y_true, Y_pred):
        """
        Custom loss function to compute the profit or loss based on the cost-benefit matrix.

        Args:
        Y_true: true class labels (0 = Poor, 1 = Standard, 2 = Good)
        Y_pred: predicted class probabilities or labels

        Returns:
        A scalar representing the total loss across all examples.
        """

        cost_benefit = tf.constant(self.cost_benefit_matrix, dtype=tf.float32)

        # Get the predicted class by taking the argmax (index of the highest probability)
        Y_pred_labels = tf.argmax(Y_pred, axis=1, output_type=tf.int32)

        # Ensure y_true is an integer tensor
        Y_true = tf.squeeze(tf.cast(Y_true, tf.int32))
        Y_true_one_hot = tf.one_hot(Y_true, depth=3)

        # Stack y_true and y_pred_labels into pairs: shape (batch_size, 2)
        indices = tf.stack([Y_true, Y_pred_labels], axis=1)

        expected_loss = tf.reduce_sum(Y_pred * tf.matmul(Y_true_one_hot, cost_benefit), axis=1)
        expected_loss = tf.cast(expected_loss, tf.float32)

        return -tf.reduce_mean(expected_loss)