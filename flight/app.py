from flask import Flask, jsonify, request
import requests
from lxml import etree
from flask_cors import CORS
import config_init

app = Flask(__name__)
CORS(app)

@app.route('/api/search_flights', methods=['POST'])
def search_flights():
    print("Request received:")
    print(request.json)
    data = request.json  # Receive input from the frontend
    dep_apt = data.get("dep_apt")
    dst_apt = data.get("dst_apt")
    dep_date = data.get("dep_date")
    return_date = data.get("return_date")
    passengers = data.get("passengers", [])

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

    fare_request = etree.Element("fareRequest", da="true")

    vcrs = etree.SubElement(fare_request, "vcrs")
    etree.SubElement(vcrs, "vcr").text = "BA"

    etree.SubElement(fare_request, "fareTypes", xmlns="http://ypsilon.net/shared")
    etree.SubElement(fare_request, "tourOps")

    flights = etree.SubElement(fare_request, "flights")
    etree.SubElement(flights, "flight", depApt=dep_apt, dstApt=dst_apt, depDate=dep_date)
    if return_date:
        etree.SubElement(flights, "flight", depApt=dst_apt, dstApt=dep_apt, depDate=return_date)

    paxes = etree.SubElement(fare_request, "paxes")
    for pax in passengers:
        etree.SubElement(
            paxes,
            "pax",
            surname=pax.get("surname"),
            firstname=pax.get("firstname"),
            dob=pax.get("dob"),
            gender=pax.get("gender"),
        )

    etree.SubElement(fare_request, "paxTypes")

    options = etree.SubElement(fare_request, "options")
    etree.SubElement(options, "limit").text = "20"
    etree.SubElement(options, "offset").text = "0"
    wait_on_list = etree.SubElement(options, "waitOnList")
    etree.SubElement(wait_on_list, "waitOn").text = "ALL"

    coses = etree.SubElement(fare_request, "coses")
    etree.SubElement(coses, "cos").text = "E"

    xml_request_body = etree.tostring(fare_request, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    print("API Request URL:", api_url)
    print("API Request Headers:", headers)
    print("API Request Body:", xml_request_body.decode())  # Decode bytes to string

    try:
        response = requests.post(api_url, headers=headers, data=xml_request_body)
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)}), 500

    if response.status_code == 200:
        try:
            root = etree.fromstring(response.content)
            print(etree.tostring(root, pretty_print=True).decode())
            flight_info = []

            namespaces = {"shared": "http://ypsilon.net/shared"}
            for fare in root.xpath("//fare", namespaces=namespaces):
                print("Fare Element: ", etree.tostring(fare, pretty_print=True).decode())
                dep_apt = fare.get("depApt")
                dst_apt = fare.get("dstApt")
                dep_date = fare.get("date")
                fare_id = fare.get("fareId")
                ticket_timelimit = fare.get("ticketTimelimit")
                class_code = fare.get("class")

                flight_info.append({
                    "fare_id": fare_id,
                    "departure_airport": dep_apt,
                    "destination_airport": dst_apt,
                    "departure_date": dep_date,
                    "ticket_timelimit": ticket_timelimit,
                    "class": class_code
                })

            return jsonify({"success": True, "flights": flight_info})
        except etree.XMLSyntaxError as e:
            return jsonify({"success": False, "error": "Failed to parse XML response"}), 500
    else:
        return jsonify({"success": False, "error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
