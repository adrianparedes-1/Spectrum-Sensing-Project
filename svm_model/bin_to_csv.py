import struct
import csv

# List of binary files to process (only signal + noise files)
signal_noise_files = [f"test_output_{i}.bin" for i in range(140)]

output_file = "sample_name.csv"  # CSV output file

# Complex number and sample rate
data_type = '2f'  # Each complex sample is a pair of 32-bit floats (real, imag)
sample_rate = 500_000
duration_ms = 80  # Duration of each waveform in ms

# Calculate the number of samples for 80 ms
num_samples_per_waveform = int(sample_rate * (duration_ms / 1000))  # Samples in 80 ms

# Initialize a list to store the complex samples for all files
all_waveforms = []

# Process each binary file
for input_file in signal_noise_files:
    with open(input_file, "rb") as bin_file:
        data = bin_file.read()

    # Calculate the total number of complex samples in the file
    total_samples = len(data) // struct.calcsize(data_type)

    # Check if the file contains enough data for the expected duration
    if total_samples < num_samples_per_waveform:
        print(f"Warning: {input_file} does not have enough samples for 8 ms")
        continue

    # Unpack the binary data into a list of complex samples (real, imag pairs)
    samples = struct.unpack(f'{total_samples * 2}f', data)

    # Store the waveforms for this file
    waveforms = []
    for start in range(0, num_samples_per_waveform * 2, 2):  # Process only the first 80 ms
        real = samples[start]
        imag = samples[start + 1]
        complex_number = complex(real, imag)
        waveforms.append(complex_number)

    # Append the waveform (for one file) as a column
    all_waveforms.append(waveforms)

# Write the data to a CSV file, where each column represents a different binary file
with open(output_file, "w", newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Transpose rows and columns to align data
    for row in zip(*all_waveforms):  # Zip to transpose the list and align columns correctly
        writer.writerow(row)

print(f"Data has been successfully converted to {output_file}")
