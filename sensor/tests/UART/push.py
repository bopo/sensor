import serial

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)

ser.read(10)
ser.readline() 
ser.readlines() 

ser.baudrate = 9600 #设置波特率
ser.isOpen() #看看这个串口是否已经被打开

# ValueError：参数错误
# SerialException：找不到设备或不能配置

ser.write("hello")
ser.close()


print(dir(ser))
