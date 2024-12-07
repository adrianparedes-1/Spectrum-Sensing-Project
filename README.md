# Spectrum Sensing Project





## Receiver
There are two receiver flowcharts: one for training data collection, and another for live data reception. Both of these have similar structures, with the main difference being the output blocks. The offline data collection flowchart outputs the data to a binary file in complex form. There are two shell scripts that are running simultaneously while this is happening. The purpose of these shell scripts is to take snapshots of the main binary file at 80 ms intervals. The shell scripts can be simplified into just one script if desired. If you run both scripts, you will have 140 binary files that were created at 80 ms intervals from the original binary that is specified on the GNU Radio File Sink block. Now, run the Python script to organize this data into 140 columns in a .csv file. Once you have the .csv, take a sample and randomize it so you can train the SVM model. Now that the SVM model is trained, it is time to run the live receiver flowchart so the trained model can be deployed on the live data obtained by subscribing to the ZMQ block. 


## Transmitter
The transmitter flowchart was created with GNU Radio. The flowchart includes a signal source, a noise source, and a selector. The selector GUI allows for live toggling between signal + noise, noise, and signal during live transmission. The flowchart also assumes that you are using a USRP SDR Kit, but it can be substituted with another logic block if you choose to use a different SDR Kit. Alternatively, you may eliminate the USRP block for virtual testing.


## Result
Console output:

Radio Signal Present/No Radio Signal Detected
