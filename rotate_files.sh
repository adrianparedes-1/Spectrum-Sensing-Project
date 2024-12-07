#!/bin/bash

# Configuration
base_filename="test_output"
output_dir="/c/Users/adrian/Documents/GNURadio"  # Ensure the correct path
max_size=320000  # 80 ms of data in bytes (adjust as needed)
max_files=70  # Maximum number of files to create
index=0  # Starting index for file naming
offset=0  # Byte offset to track position in the file

echo "Starting data capture..."

while [[ $index -lt $max_files ]]; do
    file_path="${output_dir}/${base_filename}.bin"
    output_file="${output_dir}/${base_filename}_${index}.bin"

    # Check if the file exists and has enough data
    if [[ -f "$file_path" ]]; then
        file_size=$(stat -c%s "$file_path")

        # Ensure there is enough new data to extract an 80 ms chunk
        if [[ $file_size -ge $((offset + max_size)) ]]; then
            echo "Extracting 80 ms of data to ${output_file}"

            # Extract the 80 ms chunk using dd
            dd if="$file_path" of="$output_file" bs=1 skip="$offset" count="$max_size" status=none

            # Update the offset for the next chunk
            offset=$((offset + max_size))

            # Increment the file index
            index=$((index + 1))
        else
            echo "Waiting for more data..."
            sleep 0.1  # Adjust sleep interval as needed
        fi
    else
        echo "Waiting for file creation..."
        sleep 0.1
    fi
done

echo "Data capture complete. Reached the limit of $max_files files."
