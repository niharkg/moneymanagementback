import tensorflow as tf
import numpy as np

# Train the user's prediction model for a category
def train_category_spending_model(months, spendings):
    # x and y are placeholders for our training data
    x = tf.placeholder("float")
    y = tf.placeholder("float")
    # w is the variable storing our values. It is initialised with starting "guesses"
    # w[0] is the "a" in our equation, w[1] is the "b"
    w = tf.Variable([0.0, spendings[0]], name="w")
    # Our model of y = a*x + b
    y_model = tf.multiply(x, w[0]) + w[1]
    # Our error is defined as the square of the differences
    error = tf.square(y - y_model)
    # The Gradient Descent Optimizer does the heavy lifting
    train_op = tf.train.GradientDescentOptimizer(0.00001).minimize(error)
    # Normal TensorFlow - initialize values, create a session and run the model
    model = tf.global_variables_initializer()
    with tf.Session() as session:
        session.run(model)
        for i in range(20000):
            x_value = months[i%len(months)]
            y_value = spendings[i%len(months)]
            session.run(train_op, feed_dict={x: x_value, y: y_value})
        w_value = session.run(w)
        predictions = []
        for index in range(len(spendings)):
            pred = (tf.multiply(w_value[0], float(months[index])) + w_value[1]).eval()
            pred = round(pred, 2)
            predictions.append(pred)
        return[months, spendings, predictions]
