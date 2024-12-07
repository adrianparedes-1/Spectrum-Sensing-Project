import zmq
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from collections import deque
import joblib

# Load the trained model and scaler
svm_model = joblib.load("svm_model_5k.joblib")
scaler = joblib.load("scaler_5k.joblib")

# Debug: Print scaler statistics to validate match with training data
print(f"Scaler Mean: {scaler.mean_}")
print(f"Scaler Scale: {scaler.scale_}")

# Configure ZMQ
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

print("Waiting for binary complex data...", flush=True)

# Buffer to accumulate 5k complex numbers
BUFFER_SIZE = 5000
buffer = deque(maxlen=BUFFER_SIZE)

def scale_sum_of_magnitudes(sum_of_magnitudes):
    """
    Scale the sum of magnitudes manually based on the training data's statistics.
    """
    # Use the scaler from the training data
    training_mean = scaler.mean_
    training_std = scaler.scale_

    # Ensure the value is a 2D array before applying the formula
    sum_of_magnitudes = np.array(sum_of_magnitudes).reshape(-1, 1)

    # Apply the standardization formula: (x - mean) / std
    scaled_value = (sum_of_magnitudes - training_mean) / training_std

    return scaled_value.flatten()  # Flatten to return a 1D array

try:
    while True:
        # Receive raw binary data
        try:
            message = socket.recv(flags=zmq.NOBLOCK)  # Non-blocking receive
        except zmq.Again:
            continue  # No message received, skip iteration

        # Convert binary data to np.complex64
        raw_complex = np.frombuffer(message, dtype=np.complex64)[0]  # Assume one complex number per message

        # Compute magnitude and add to buffer
        magnitude = np.abs(raw_complex)
        buffer.append(magnitude)

        # When buffer is full, process the data
        if len(buffer) == BUFFER_SIZE:
            # Sum the magnitudes
            sum_of_magnitudes = np.sum(buffer)

            # Scale the summed value
            scaled_sum = scale_sum_of_magnitudes(sum_of_magnitudes)

            # Predict using the trained SVM
            prediction = svm_model.predict(scaled_sum.reshape(-1, 1))

            if prediction[0] == 0:
                print("No Radar Signal", flush=True)
            elif prediction[0] == 1:
                print("Radar Signal Detected", flush=True)


            # Clear the buffer to accumulate the next set of 40k complex numbers
            buffer.clear()

except KeyboardInterrupt:
    print("Stopping the subscriber...", flush=True)
    socket.close()
    context.term()
