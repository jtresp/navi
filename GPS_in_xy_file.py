import serial
import pynmea2
import time
import math
import csv

def get_gps_coordinates(serial_port):
    """
    Reads GPS coordinates from the given serial port.
    
    :param serial_port: The serial port connected to the GPS device
    :return: Tuple containing latitude and longitude
    """
    try:
        data = serial_port.readline().decode('ascii', errors='replace')
        if data.startswith('$GPGGA'):
            msg = pynmea2.parse(data)
            lat = msg.latitude
            lon = msg.longitude
            return lat, lon
    except Exception as e:
        print(f"Error reading GPS data: {e}")
    return None, None

def convert_to_cartesian(lat, lon, lat_ref, lon_ref, R=6371000):
    """
    Converts latitude and longitude to Cartesian coordinates.
    
    :param lat: Latitude
    :param lon: Longitude
    :param lat_ref: Reference latitude
    :param lon_ref: Reference longitude
    :param R: Radius of the Earth in meters
    :return: Tuple containing x and y coordinates in meters
    """
    x = R * (math.radians(lon) - math.radians(lon_ref)) * math.cos(math.radians(lat_ref))
    y = R * (math.radians(lat) - math.radians(lat_ref))
    return x, y

def main():
    # Adjust the serial port and baud rate to match your GPS device's configuration
    serial_port = '/dev/ttyUSB0'  # Example for Linux
    baud_rate = 9600
    output_file = 'gps_coordinates.csv'

    # Open the CSV file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])  # Write header
        
        coordinates = []

        try:
            with serial.Serial(serial_port, baud_rate, timeout=1) as port:
                print("Reading GPS coordinates...")
                
                # Get initial coordinates
                lat1, lon1 = None, None
                while lat1 is None or lon1 is None:
                    lat1, lon1 = get_gps_coordinates(port)
                    time.sleep(0.1)  # Retry after a short delay if no data is received
                
                print(f"Initial coordinates: Latitude = {lat1}, Longitude = {lon1}")
                lat_ref, lon_ref = lat1, lon1  # Set reference coordinates

                # Convert initial coordinates to Cartesian and save
                x1, y1 = convert_to_cartesian(lat1, lon1, lat_ref, lon_ref)
                coordinates.append((x1, y1))
                writer.writerow([x1, y1])
                print(f"Initial coordinates in Cartesian: x = {x1}, y = {y1}")
                
                # Continuous tracking
                while True:
                    # Wait for 1 second
                    time.sleep(1)
                    
                    # Get new coordinates
                    lat2, lon2 = None, None
                    while lat2 is None or lon2 is None:
                        lat2, lon2 = get_gps_coordinates(port)
                        time.sleep(0.1)  # Retry after a short delay if no data is received
                    
                    print(f"New coordinates: Latitude = {lat2}, Longitude = {lon2}")
                    
                    # Convert new coordinates to Cartesian and save
                    x2, y2 = convert_to_cartesian(lat2, lon2, lat_ref, lon_ref)
                    coordinates.append((x2, y2))
                    writer.writerow([x2, y2])
                    print(f"New coordinates in Cartesian: x = {x2}, y = {y2}")

        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")

if __name__ == "__main__":
    main()
