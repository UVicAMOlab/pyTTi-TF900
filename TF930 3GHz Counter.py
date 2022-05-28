import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import pandas as pde

FILENAME = time.strftime("%Y-%m-%d-%H%M.%Ss")

def get_freq(collection_period : int):
    """Gets the frequency and calls other helper function for plotting or logging the data

    Args:
        collection_period (int): How long the function will collect data for in seconds
        log_or_plot (bool): If given true the function will log the data in a csv,
        if given false the function will plot it on a graph and not log it

    Returns:
        int: acquired data points
    """
    cur_time = time.time() # Takes the time
    starting_time = cur_time
    data = []
    time_collected = []
    df_list = []
    collection_time = cur_time + collection_period
    s = serial.Serial("COM1" ,baudrate = 115200, stopbits = serial.STOPBITS_ONE , timeout = 1,parity=serial.PARITY_NONE, rtscts=True, dsrdtr = True)
    s.flushInput()
    s.flushOutput()
    s.write(b'E?\n\r')

    while cur_time <= collection_time:
        byte_data = s.readline()
            #Reads the data off the counter
        cur_time = time.time()    
        freq_data = byte_data.decode("utf-8")
            #Decodes readings from bytes to a string
        freq_data = freq_data.replace("\r\n","")
        bs_10 = 10**int(freq_data[13])
        freq_data_fl = float(freq_data[:11]) * bs_10
        data.append(freq_data_fl)
        time_collected.append(cur_time-starting_time)
        s.write(b'N?\n\r')
            #Skips to the next reading  
    df_list.append(data)
    df_list.append(time_collected)
    dbf = pde.DataFrame(df_list, index = ["Frequency","Time"]).T
    dbf.to_csv("{}.csv".format(FILENAME), index = False , header = True)
    s.write(b'STOP\n\r') 

get_freq(30)