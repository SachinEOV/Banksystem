from flask import Flask, jsonify, request
import requests
from lxml import etree
from flask_cors import CORS
import config_init
from utils import create_flight_request_xml  

app = Flask(__name__)
CORS(app)

@app.route('/api/search_flights', methods=['POST'])
def search_flights():
    print("Request received:")
    print(request.json)
    data = request.json  

    headers = {
        "Authorization": config_init.authorization_header,
        "api-version": b'3.91',
        "accessmode": config_init.accessmode,
        "accessid": config_init.accessid,
        "Cache-Control": config_init.cache_control,
        "authmode": config_init.authmode,
        "Content-Type": config_init.content_type,
    }

    api_url = config_init.api_url
    if not api_url:
        return jsonify({"success": False, "error": "API URL not found in config file"}), 500

    xml_request_body = create_flight_request_xml(data)

    print("API Request URL:", api_url)
    print("API Request Headers:", headers)
    print("API Request Body:", xml_request_body.decode())

    try:
        response = requests.post(api_url, headers=headers, data=xml_request_body)
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)}), 500

    if response.status_code == 200:
        try:
            root = etree.fromstring(response.content)
            print("Full XML Response:")
            print(etree.tostring(root, pretty_print=True).decode())  

            flight_info = []
            namespaces = {"shared": "http://ypsilon.net/shared"}

            for fare in root.xpath("//fare", namespaces=namespaces):
                print("Fare Element:", etree.tostring(fare, pretty_print=True).decode())
                
                dep_apt = fare.get("depApt")
                dst_apt = fare.get("dstApt")
                dep_date = fare.get("date")
                fare_id = fare.get("fareId")
                ticket_timelimit = fare.get("ticketTimelimit")
                class_code = fare.get("class")
                cos = fare.get("cos")

                # Append flight info
                flight_info.append({
                    "fare_id": fare_id,
                    "departure_airport": dep_apt,
                    "destination_airport": dst_apt,
                    "departure_date": dep_date,
                    "ticket_timelimit": ticket_timelimit,
                    "class": class_code,
                    "cos": cos,
                })

            return jsonify({"success": True, "flights": flight_info})
        except etree.XMLSyntaxError as e:
            return jsonify({"success": False, "error": "Failed to parse XML response"}), 500
    else:
        return jsonify({"success": False, "error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
