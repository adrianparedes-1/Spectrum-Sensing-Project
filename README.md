# Spectrum Sensing Project

The project focuses on **spectrum sensing** using **clustering machine learning models** implemented with a **Software-Defined Radio (SDR) kit**. The system dynamically monitors the radio frequency spectrum, detects active signals, and identifies unused channels. By leveraging machine learning, the solution adapts to changing RF environments, processes complex signal patterns, and ensures efficient spectrum usage. This has real-world applications in **telecommunications**, **cognitive radio**, and **IoT**, enabling dynamic spectrum access, interference detection, and optimized frequency allocation.

More details about the project can be found below:

## Transmitter
The transmitter flowchart was created with GNU Radio. The flowchart includes a signal source, a noise source, and a selector. The selector GUI allows for live toggling between signal + noise, noise, and signal during live transmission. The flowchart also assumes that you are using a USRP SDR Kit, but it can be substituted with another logic block if you choose to use a different SDR Kit. Alternatively, you may eliminate the USRP block for virtual testing.

## Receiver
There are two receiver flowcharts: one for training data collection, and another for live data reception. Both of these have similar structures, with the main difference being the output blocks. The offline data collection flowchart outputs the data to a binary file in complex form. There are two shell scripts that are running simultaneously while this is happening. The purpose of these shell scripts is to take snapshots of the main binary file at 80 ms intervals. The shell scripts can be simplified into just one script if desired. If you run both scripts, you will have 140 binary files that were created at 80 ms intervals from the original binary that is specified on the GNU Radio File Sink block. Now, run the Python script to organize this data into 140 columns in a .csv file. 

## SVM Model
Once you have the .csv, take a sample and randomize it so you can train the SVM model. This machine learning model aggregates the magnitudes from the complex numbers collected and divides them into two clusters: Signal Detected, or No Signal Detected. The SVM model will provide output Recall, Precision, and FPR. Now that the SVM model is trained, there will be .joblib files generated which can be loaded into the live integration program for real time detection. Now run the live receiver flowchart so the trained model can be deployed on the live data obtained by subscribing to the ZMQ block. 

## Result
Console output:

Radio Signal Present/No Radio Signal Detected
