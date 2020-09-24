import requests
import re
import csv
from requests.auth import HTTPBasicAuth

url = "http://192.168.0.1/NetworkMap.asp"

# Example credentials
user = "admin"
password = "password"

# Exclude local IP addresses
NOIP = True

data_from_file = []

# Import existing data from output file
try:
    with open('output.csv', newline='') as file_input:
        file_reader = csv.reader(file_input, delimiter=',')
        for row in file_reader:
            data_from_file.append(row)
except:
    pass

data = requests.get(url, auth=HTTPBasicAuth(user, password))
matches = re.findall(r'\".+\",\".+\",\".+\"', data.text)

with open('output.csv', mode='w', newline='') as file_output:
    file_writer = csv.writer(file_output, delimiter=',')

    devices = []
    for match in matches:
        devices.append(match.replace("\"", "").split(","))

    # Remove local ip addresses
    for device in devices:
        if NOIP:
            device.pop(1)

    # Write existing devices
    for device in data_from_file:
        file_writer.writerow(device)

    # Write new devices
    for device in devices:
        if device not in data_from_file:
            file_writer.writerow(device)
