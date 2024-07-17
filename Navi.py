
import serial
import sys
import time
import gpscalculatemodule as GPSCalc
Zeichen = 0
Laenge = 0
Qualitaet = 0
Satelliten = 0

Hoehe = 0.0
Breitengrad = 0.0
Laengengrad = 0.0
global Last_Breite
global Last_Laenge

Input = ""
Uhrzeit = ""
Checksumme = ""

def location():
	period=30
	#timestamp=time.monotonic()
	while True:
		#timestamp+=period
		#time.sleep(timestamp- time.monotonic())
		time.sleep(period)
		gps(serial_port)
		
def gps(serial_port):
	"""
	Liest GPS-Daten vom angegebenen seriellen Port und extrahiert GPVTG-Daten.
	:param serial_port: Pfad zum seriellen Port (z. B. '/dev/ttyUSB0')
	"""
	count=0
	try:
		ser = serial.Serial(serial_port, 9600, timeout=1)
		#print('GPS-Daten von gelesen:', {serial_port} )

		while True:
			line = ser.readline().decode('utf-8').strip()
			#if line.startswith('$GPVTG'):
				# Extrahiere Geschwindigkeitsinformationen aus GPVTG-Daten
			#	data = line.split(',')
			#	speed_knots = float(data[7])
			#	speed_kph = speed_knots * 1.852  # Umrechnung von Knoten in km/h
				


			#elif line.startswith('$GPGGA'):
			if line.startswith('$GPGGA'):
				# Extrahiere Positionsdaten aus GPGGA-Daten
				data = line.split(',')
				latitude = data[2]
				longitude = data[4]
				# Uhrzeit herausfiltern
				Uhrzeit = data[1]
				Uhrzeit = Uhrzeit[0:2] + ":" + Uhrzeit[2:4] + ":" + Uhrzeit[4:6]
				# Laengen und Breitengrad herausfiltern und berechnen
				Breitengrad = int(float(data[2]) / 100)
				Laengengrad = int(float(data[4]) / 100)
			
				Breitenminute = float(data[2]) - (Breitengrad * 100)
				Laengenminute = float(data[4]) - (Laengengrad * 100)

				Breite = round(Breitengrad + (Breitenminute / 60), 6)
				Laenge = round(Laengengrad + (Laengenminute / 60), 6)

				print ('Breitengrad:------', Breite)
				print ('Laengengrad:------', Laenge)
				time.sleep(10)
				#if count == 10:              
				Last_Breite = Breite
				Last_Laenge = Laenge
					#count =0
				#	time.sleep(0.1)
				#	count+=1
				print ('Breitengraaad:', Last_Breite)
				print ('Laengengraaad:', Last_Laenge)
				distance,angle,x,y = GPSCalc.calc(Breite,Laenge,Last_Breite,Last_Laenge)
				print ('distance,angle,x,y:',distance,angle,x,y)


	except serial.SerialException:
		print('Fehler beim Oeffnen des seriellen Ports {serial_port}. Stelle sicher, dass das Geraet angeschlossen ist.')
	finally:
		ser.close()
	

def read_gps_data(serial_port):
	"""
	Liest GPS-Daten vom angegebenen seriellen Port und extrahiert GPVTG-Daten.
	:param serial_port: Pfad zum seriellen Port (z. B. '/dev/ttyUSB0')
	"""
	try:
		ser = serial.Serial(serial_port, 9600, timeout=1)
		print('GPS-Daten von gelesen:', {serial_port} )

		while True:
			line = ser.readline().decode('utf-8').strip()
			if line.startswith('$GPVTG'):
				# Extrahiere Geschwindigkeitsinformationen aus GPVTG-Daten
				data = line.split(',')
				speed_knots = float(data[7])
				speed_kph = speed_knots * 1.852  # Umrechnung von Knoten in km/h
				

			elif line.startswith('$GPGGA'):
				# Extrahiere Positionsdaten aus GPGGA-Daten
				data = line.split(',')
				latitude = data[2]
				longitude = data[4]
				# Uhrzeit herausfiltern
				Uhrzeit = data[1]
				Uhrzeit = Uhrzeit[0:2] + ":" + Uhrzeit[2:4] + ":" + Uhrzeit[4:6]
				# Laengen und Breitengrad herausfiltern und berechnen
				Breitengrad = int(float(data[2]) / 100)
				Laengengrad = int(float(data[4]) / 100)
			
				Breitenminute = float(data[2]) - (Breitengrad * 100)
				Laengenminute = float(data[4]) - (Laengengrad * 100)

				Breite = round(Breitengrad + (Breitenminute / 60), 6)
				Laenge = round(Laengengrad + (Laengenminute / 60), 6)

				# Signalqualitaet herausfiltern
				Qualitaet = int(data[6])

				# Anzahl der Satelliten herausfiltern
				Satelliten = int(data[7])

				# Hoehe herausfiltern
				Hoehe = float(data[9])
			
				# Checksumme auslesen
				Checksumme = data[14]

				#print('Positionsdaten - Breitengrad:', latitude)
				#print('Laengengrad:', longitude)
				#print(data)
				# Ausgabe
				#print Input
				#print ""
				#print ('Laenge des Datensatzes:', Laenge_Daten, "Zeichen"
				print ('Uhrzeit:', Uhrzeit)
				print ('Geschwindigkeit:', {speed_kph},' km/h')
				print ('Breitengrad:', Breite, 'Grad', data[3])
				print ('Laengengrad:', Laenge, 'Grad', data[5])
				print ('Hoehe ueber dem Meeresspiegel:', Hoehe, data[10])
				print ('GPS-Qualitaet:', Qualitaet)
				print ('Anzahl der Satelliten:', Satelliten)
				print ('Checksumme:', Checksumme)
				print ('-------------------------------------------')



	except serial.SerialException:
		print('Fehler beim Oeffnen des seriellen Ports {serial_port}. Stelle sicher, dass das Geraet angeschlossen ist.')
	finally:
		ser.close()

# Seriellen Port angeben (entsprechend anpassen)
serial_port = '/dev/ttyACM0'

# GPS-Daten lesen und GPVTG-Informationen extrahieren
#read_gps_data(serial_port)
gps(serial_port)
#location()
#time.sleep(10)
