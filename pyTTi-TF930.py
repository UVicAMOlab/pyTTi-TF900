import serial
import time
import csv



def get_freq(collection_period : int):
    """Gets the frequency and calls other helper function for plotting or logging the data

    Args:
        collection_period (int): How long the function will collect data for in seconds
        log_or_plot (bool): If given true the function will log the data in a csv,
        if given false the function will plot it on a graph and not log it

    Returns:
        int: acquired data points
    """
    try:
        filename = time.strftime("%Y-%m-%d-%H%M.%Ss")
        cur_time = time.time() # Takes the time
        collection_time = cur_time + collection_period
        starting_time = cur_time

        # Initialize output file
        header = ["Frequency(Hz)","Time(s)"]
        
        # Initialize serial port with device defaults from device manual
        s = serial.Serial("COM1" ,baudrate = 115200, stopbits = serial.STOPBITS_ONE , timeout = 1,parity=serial.PARITY_NONE, rtscts=True, dsrdtr = True)
        s.flush()

        # Initialize serial stream
        # send command to start receiving data
        s.write(b'E?\n\r')

        # Loop reading stream until time expires
        with open(filename+".csv", 'w', newline = '') as csvfile:
            f_writer = csv.DictWriter(csvfile, fieldnames = header)
            f_writer.writerow({"Frequency(Hz)":"Frequency(Hz)","Time(s)":"Time(s)"})
            while cur_time <= collection_time:
                # Reads the data off the counter
                byte_data = s.readline()                

                # Decodes readings from bytes to a string
                freq_data = byte_data.decode("utf-8") 

                # Convert alphanumeric reading to float
                freq_data = freq_data.replace("\r\n","")
                bs_10 = 10**int(freq_data[13])
                freq_data_fl = float(freq_data[:11]) * bs_10

                # Write freq_data_fl and time_col to output file 
                time_col = cur_time - starting_time
                
                #Write to file
                f_writer.writerow({"Frequency(Hz)":freq_data_fl,"Time(s)":time_col})

                cur_time = time.time()
                
        s.write(b'STOP\n\r') 
        print("done with no error")

    except serial.SerialException as e:
        s.write(b'STOP\n\r')
        print("raised Serial error didn't take all data"+ e)
    except IndexError:
        s.write(b'STOP\n\r')
        print("Switch to B")



get_freq(3600)