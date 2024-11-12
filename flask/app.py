from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/search_flights', methods=['POST'])
def search_flights():
    config_file_path = "config.in"
    headers = {}

    with open(config_file_path, "r") as f:
        for line in f:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()

    xml_request_body = request.data.decode("utf-8")
    
    response = requests.post("https://stagingxml.ypsilon.net:11024", headers=headers, data=xml_request_body)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        flight_info = []
        for flight in root.findall(".//flight"):
            dep_apt = flight.get("depApt")
            dst_apt = flight.get("dstApt")
            dep_date = flight.get("depDate")
            flight_info.append(f"Departure: {dep_apt}, Destination: {dst_apt}, Date: {dep_date}")
        
        return jsonify({"success": True, "flights": flight_info})

    else:
        return jsonify({"success": False, "error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
