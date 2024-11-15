from flask import Flask, jsonify, request
import requests
from lxml import etree
from flask_cors import CORS
import config_init

app = Flask(__name__)
CORS(app)

@app.route('/api/search_flights', methods=['GET'])
def search_flights():
    headers = {
        "Authorization": config_init.authorization_header,  # Use the Base64 encoded value from config_init
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

    # Construct XML dynamically
    fare_request = etree.Element("fareRequest", da="true")

    # Add <vcrs> and <vcr>
    vcrs = etree.SubElement(fare_request, "vcrs")
    etree.SubElement(vcrs, "vcr").text = "BA"

    # Add <fareTypes>
    etree.SubElement(fare_request, "fareTypes", xmlns="http://ypsilon.net/shared")

    # Add <tourOps>
    etree.SubElement(fare_request, "tourOps")

    # Add <flights>
    flights = etree.SubElement(fare_request, "flights")
    etree.SubElement(flights, "flight", depApt="LON", dstApt="FRA", depDate="2024-12-05")
    etree.SubElement(flights, "flight", depApt="FRA", dstApt="LON", depDate="2024-12-12")

    # Add <paxes>
    paxes = etree.SubElement(fare_request, "paxes")
    etree.SubElement(paxes, "pax", surname="Tester", firstname="John", dob="1945-12-12", gender="M")
    etree.SubElement(paxes, "pax", surname="Tester", firstname="Jane", dob="1945-12-12", gender="F")

    # Add <paxTypes>
    etree.SubElement(fare_request, "paxTypes")

    # Add <options>
    options = etree.SubElement(fare_request, "options")
    etree.SubElement(options, "limit").text = "20"
    etree.SubElement(options, "offset").text = "0"
    wait_on_list = etree.SubElement(options, "waitOnList")
    etree.SubElement(wait_on_list, "waitOn").text = "ALL"

    # Add <coses> and <cos>
    coses = etree.SubElement(fare_request, "coses")
    etree.SubElement(coses, "cos").text = "E"

    # Serialize XML to string
    xml_request_body = etree.tostring(fare_request, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    try:
        response = requests.post(api_url, headers=headers, data=xml_request_body)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)}), 500

    if response.status_code == 200:
        try:
            root = etree.fromstring(response.content)
            namespaces = {'shared': 'http://ypsilon.net/shared'}
            flight_info = []

            for fare in root.xpath("//fare", namespaces=namespaces):
                dep_apt = fare.get("depApt")
                dst_apt = fare.get("dstApt")
                dep_date = fare.get("date")
                fare_id = fare.get("fareId")
                ticket_timelimit = fare.get("ticketTimelimit")
                class_code = fare.get("class")

                if dep_apt and dst_apt and dep_date:
                    flight_info.append({
                        "fare_id": fare_id,
                        "departure_airport": dep_apt,
                        "destination_airport": dst_apt,
                        "departure_date": dep_date,
                        "ticket_timelimit": ticket_timelimit,
                        "class": class_code
                    })

            if flight_info:
                return jsonify({"success": True, "flights": flight_info})
            else:
                return jsonify({"success": False, "error": "No flights found"}), 404
        except etree.XMLSyntaxError as e:
            return jsonify({"success": False, "error": "Failed to parse XML response"}), 500
    else:
        return jsonify({"success": False, "error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
