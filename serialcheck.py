import serial

# Open serial port
ser = serial.Serial('COM5', 9600, timeout=1)  # Adjust the port and baudrate as needed

# Write data to the serial port
ser.write(b'Hello, World!')

# Read data from the serial port
line = ser.readline().decode('utf-8').rstrip()
print(line)

# Close the serial port
ser.close()
