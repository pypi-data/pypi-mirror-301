import numpy as np
import pyvisa
import sys
import pandas
import time
import datetime
import os
# import PowerMeterClass
# import PowerSupplyClass
# import MultimeterClass
# import InstrumentClass
# import DCBiasingSupplyClass

def WriteReadMe(additonal_string, Freq1, Freq2, 
	TestType = "Unknown",
	Drain = None,
	Gate = None,
	InputPower = None,
	OutputPower = None,
	RFInput = None,
	Sampler1 = None,
	Sampler2 = None,
	OpAmp = None):

	

	# now = datetime.datetime.now().strftime("%m-%d-%y_%H%M%S")
	path = "./README/"
	try:
		os.mkdir(path)
	except FileExistsError:
		pass
	filename = "README_" + TestType + ".md"
	f = open(path + filename,"a")

	f.write("These tests were run for frequencies between" + str(Freq1) + " MHz and " + str(Freq2) + " MHz\n")

	if Drain:
		f.write("<h2>Drain  DC Power Supply</h2>\n")
		f.write("Drain instrument was " + Drain.IDN + "</br>\n")
		f.write("Drain channel was " + Drain.channel + "</br>\n")
		f.write("Starting conditions for the Drain was current limit of "
			+ Drain.instr.query("CURR:LIM?")
			+ " and voltage set to "
			+ Drain.instr.query("VOLT?")
			+ "</br>\n")

	if Gate:
		f.write("<h2>Gate DC Power Supply</h2>\n")
		f.write("Gate instrument was " + Gate.IDN +  "</br>\n")
		f.write("Gate channel was " + Gate.channel +"</br>\n")
		f.write("Starting conditions for the Gate was current limit of "
			+ Gate.instr.query("CURR:LIM?")
			+ " and voltage set to "
			+ Gate.instr.query("VOLT?")
			+ "</br>\n")

	if InputPower:
		f.write("<h2>Input Power Meter</h2>")
		f.write("Input Power Meter instrument was " + InputPower.IDN + "</br>\n")
		if InputPower.HP:
			f.write("The cal factor file was " + InputPower.CalFile)
		if InputPower.RS:
			f.write("The average samples are set to " + InputPower.AvgSamples)

	if OutputPower:
		f.write("<h2>Output Power Meter</h2>\n")
		f.write("Output Power Meter instrument was " + OutputPower.IDN + "</br>\n")
		if OutputPower.HP:
			f.write("The cal factor file was " + OutputPower.CalFile)
		if OutputPower.RS:
			f.write("The average samples are set to " + OutputPower.AvgSamples)

	if RFInput:
		f.write("<h2>RF Input Power Supply</h2>\n")
		f.write("Output Power Meter instrument was " + RFInput.IDN + "</br>\n")

	if Sampler1:
		f.write("<h2>Multimeter for Sampler 1</h2>\n")
		f.write("multimeter for sampler 1 instrument was " + Sampler1.IDN + "</br>\n")

	if Sampler2:
		f.write("<h2>Multimeter for Sampler 2</h2>\n")
		f.write("multimeter for sampler 2 instrument was " + Sampler2.IDN + "</br>\n")

	if OpAmp:
		f.write("<h2>Multimeter for Op Amp Output</h2>\n")
		f.write("multimeter for Op Amp Output instrument was " + OpAmp.IDN + "</br>\n")

	f.write("<h2>Additional</h2>\n")
	f.write(additonal_string)

	f.close

	return

class InstrumentClass():

	"""
	Base instrument class class. 

	Parameters
	---------- 
	port: int
		the port number of gpib connection 
	channel = None: int
		used with instrument with more than one channel 
	ConnectionType = 'GPIB1'
	"""

	def __init__(self, port, ConnectionType, timeout, channel = None):
		self.port = str(port)
		self.ConnectionType = ConnectionType
		self.IDN = ""
		self.instr = None
		self.timeout=timeout

		if channel:
			channel = str(channel)

		self.channel = channel

		#Run functions
		self.InstrumentConnection()

	def InstrumentConnection(self):
		rm = pyvisa.ResourceManager()
		#rm.list_resources()

		print('Attempting connection to port ' + self.port +'... ', end='')
		try:
			self.instr = rm.open_resource(self.ConnectionType + '::' + self.port + '::INSTR')
			self.instr.timeout=self.timeout
		except:
			print('Attempt to connection to ' + self.ConnectionType + '::' + self.port + '::INSTR')
			print('connection unsuccessful')
			return

		self.IDN = self.instr.query("*IDN?").rstrip()
		print('Instrument Identified as ' + self.IDN + "...", end='')
		print('connection successful\n')
		self.connected = 1

class PowerSupplyClass(InstrumentClass):

	def __init__(self, port, ConnectionType = 'GPIB0', timeout = 10000):
		InstrumentClass.__init__(self,port, ConnectionType, timeout)
		self.SetUp()

	def SetUp(self):
		self.instr.write("POW -60 DBM")
		self.instr.write("OUTP:STAT OFF")

	def SetPower(self, PowerLevel, UnitType = "DBM"):
		self.instr.write("POW " + str(PowerLevel) + " " + UnitType)
		time.sleep(.2)

	def SetFrequency(self, Frequency, UnitType = "GHZ"):
		self.instr.write("FREQ " + str(Frequency) + " " + UnitType)
		time.sleep(.2)

	def close(self):
		self.instr.write('OUTP:STAT OFF')
		self.instr.close()
		self.instr = None

class PowerMeterClass(InstrumentClass):

	def __init__(self, port, ConnectionType = 'GPIB1', CalFile = None, AvgSamples = 0, timeout = 10000):
		InstrumentClass.__init__(self,port, ConnectionType, timeout)
		self.CalFile = CalFile
		self.AvgSamples = AvgSamples
		self.CalData = None
		self.CalReferenceFactor = 100
		self.CalFreq = None
		self.HP = False
		self.RS = False

		print('Identified as ' + str(self.IDN))

		if "HEWLETT-PACKARD" in self.IDN:
			self.SetUpHP_PowerMeter()
			self.HP = True

		elif "ROHDE" in self.IDN:
			self.SetUpRS_PowerMeter(AvgSamples)
			self.RS = True

		else:
			print('Connection type unknown. Connect manually')

	def SetUpHP_PowerMeter(self):
		print('Attempting HP power meter set up... ', end='')
		if (self.CalFile):
			try:
				self.CalData = pandas.read_csv(self.CalFile, sep ='\t')
				print("set up sucessful\n")
			except:
				print("set up failed\n")
				exit()
		else:
			print("No Cal File. HP requires Cal File.")

	def SetUpRS_PowerMeter(self, AvgSamples):
		print('Attempting Keysite power meter set up... ', end='')
		self.instr.write('CAL1:ZERO:AUTO ONCE')
		time.sleep(2)
		self.instr.write('UNIT:POW DBM')
		print(self.instr.query('SYST:ERR:ALL?'))
		self.instr.write('FORMAT ASCII')
		print("set up complete")

	def SetCalFreq_HP(self, Freq):

		#This aligns with a text file of the format: Freq column1 and cal factor column 2
		if (self.CalData['Freq']==(Freq)).any():
			self.CalReferenceFactor = self.CalData[self.CalData['Freq']==(Freq)]['Percent']
			self.CalFreq = Freq
			self.instr.write("KB" + str(self.CalReferenceFactor) + "EN")
		elif (Freq == None):
			print("There is no frequency defined. Please set up Cal Frequency.")
		else:
			flooridx = np.abs(self.CalData['Freq'].astype(float) - Freq).argmin()
			# flooridx = int(np.floor(Freq))
			P1 = self.CalData['Percent'][flooridx].astype(float) 
			P2 = self.CalData['Percent'][flooridx+1].astype(float) 
			F1 = self.CalData['Freq'][flooridx].astype(float) 
			F2 = self.CalData['Freq'][flooridx+1].astype(float) 
			self.CalReferenceFactor = P1 + (P2-P1)*(F2-F1)*float(Freq)
			self.CalFreq = Freq
			self.instr.write("KB" + str(self.CalReferenceFactor) + "EN")

	def MeasurePower(self, Freq):
		if self.HP:
			#Check Calibration
			if Freq != self.CalFreq:
				self.SetCalFreq_HP(Freq)
				time.sleep(1)
			return self.instr.query("MEAS1?").rstrip()

		elif self.RS:
			self.instr.write('SENS:FREQ ' + str(Freq) + 'e9')
			self.instr.write('INIT:IMM')
			while int(self.instr.query('STAT:OPER:COND?')) >0: pass
			return self.instr.query('FETCH?').rstrip()
		else:
			print("Unrecognized Power Meter")
			exit()

	def close(self):
		self.instr.close()
		self.instr = None

class MultimeterClass(InstrumentClass):
	
	def __init__(self, port, ConnectionType = 'GPIB0', timeout = 10000, channel = None, Sampler= None):
		InstrumentClass.__init__(self,port, ConnectionType, timeout, channel=channel)
		
		if Sampler:
			self.SamplerNumber = Sampler

	def MeasureDC(self, QueryType = "VOLT"):
		try:
			MeasurementQuery = "MEAS:" + QueryType +":DC?"
			return self.instr.query(MeasurementQuery)
		except:
			self.instr.write('INIT IMM')
			meaurement = np.mean(float(self.instr.query('FETCH?')))
			self.instr.write('*RST')
			self.instr.write('CONF:VOLT:DC AUTO')
			return meaurement
	
	def close(self):
		self.instr.close()
		self.instr = None

class DCPowerSupply(InstrumentClass):

	def __init__(self, port, ConnectionType = 'GPIB0', timeout = 10000, channel = None, SupplyType=None):
		InstrumentClass.__init__(self,port, ConnectionType, timeout, channel=channel)
		self.writable = False
		self.gate = False
		self.drain = False
		self.channel = channel

		if SupplyType == 'Gate':
			self.gate = True
		elif SupplyType == 'Drain':
			self.drain = True
		else:
			print("Unrecognizable Supply Type. Ending Program.")
			exit()

	def MeasureDC(self, Channel = None, QueryType = "VOLT"):
		if not(Channel):
			Channel = self.channel
	   # the other option for query type is CURR
		
		MeasurementQuery = "MEAS:SCAL:" + QueryType +":DC? (@" + str(Channel) + ")"
		return self.instr.query(MeasurementQuery)

	def SetDC(self, SetVal, Channel = None, WriteType = "VOLT"):
		if not(Channel):
			Channel = self.channel
		if not(self.writable):
			if (self.drain):
				print("There is an attempt to change Drain Voltage through the program. Please ensure the Drain is on Port: " + str(self.port) + " before continuing")
				print("Drain Suuply IDN is: " + str(self.IDN))
				if Channel is not None:
					print("Drain channel is " + str(Channel))
					user_input = input("Enter 'q' to quit or ENTER to continue: ")
					if user_input == 'q':
						sys.exit("You chose to quit the program. ")
					else:
						self.writable = True
			elif self.gate:
				print("There is an attempt to change Gate Voltage through the program. Please ensure the Gate is on Port: " + str(self.port) + " before continuing")
				print("Gate Supply IDN is: " + self.IDN)
				if Channel:
					print("Gate channel is " + str(Channel))
					user_input = input("Enter 'q' to quit or ENTER to continue: ")
					if user_input == 'q':
						sys.exit("You chose to quit the program. ")
					else:
						self.writable = True
			else:
				print("There is an attempt to change Port: " + str(self.port) + " voltage.\nThe connection type is unknown. Please double check before continuing")
				if Channel:
					print("The channel is " + str(Channel))
				user_input = input("Enter 'q' to quit or ENTER to continue: ")
				if user_input == 'q':
					sys.exit("You chose to quit the program. ")
				else:
					self.writable = True

		MeasurementQuery = WriteType +":LEV " + str(SetVal) + ", (@" + str(Channel) + ")"
		self.instr.write(MeasurementQuery)

	def close(self):
		self.instr.close()
		self.instr = None
