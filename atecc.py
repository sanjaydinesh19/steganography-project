from cryptoauthlib import *

#Default IP Config
cfg = cfg_ateccx08a_i2c_default()

#Initialize
if atcab_init(cfg) != Status.ATCA_SUCCESS:
	print("Init Failed")
	exit()

#Read Serial Number
serial = bytearray(9)
if atcab_read_serial_number(serial) == Status.ATCA_SUCCESS:
	print("ATECC Serial Number: ",serial.hex())
else:
	print("Failed to read Serial")

