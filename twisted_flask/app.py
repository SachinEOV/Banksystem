from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from flask import Flask, jsonify, request
from lxml import etree
from flask_cors import CORS
import requests
import config_init


class FlightSearchApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.configure_routes()

    def configure_routes(self):
        @self.app.route('/api/search_flights', methods=['POST'])
        def search_flights():
            return self.handle_search_flights()

    def handle_search_flights(self):
        try:
            data = request.json 
            if not data:
                return jsonify({"success": False, "error": "No input data provided"}), 400

            dep_apt = data.get("dep_apt")
            dst_apt = data.get("dst_apt")
            dep_date = data.get("dep_date")
            return_date = data.get("return_date")
            passengers = data.get("passengers", [])

            xml_request_body = self.create_fare_request(dep_apt, dst_apt, dep_date, return_date, passengers)
            api_response = self.make_api_call(xml_request_body)

            return self.process_response(api_response)

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def create_fare_request(self, dep_apt, dst_apt, dep_date, return_date, passengers):
        """Builds the XML request body."""
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

        return etree.tostring(fare_request, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def make_api_call(self, xml_request_body):
        """Makes the API call to the external flight search service."""
        headers = {
            "Authorization": config_init.authorization_header,
            "api-version": "3.91",
            "accessmode": config_init.accessmode,
            "accessid": config_init.accessid,
            "Cache-Control": config_init.cache_control,
            "authmode": config_init.authmode,
            "Content-Type": config_init.content_type,
        }
        api_url = config_init.api_url
        if not api_url:
            raise ValueError("API URL not found in config file")

        response = requests.post(api_url, headers=headers, data=xml_request_body)
        print("Print Status Code:", response.status_code)
        print("Response Body:",response.content.decode())
        response.raise_for_status()
        return response

    def process_response(self, response):
        if response.status_code == 200:
            root = etree.fromstring(response.content)
            namespaces = {"shared": "http://ypsilon.net/shared"}
            flight_info = []

            for fare in root.xpath("//fare", namespaces=namespaces):
                flight_info.append({
                    "fare_id": fare.get("fareId"),
                    "departure_airport": fare.get("depApt"),
                    "destination_airport": fare.get("dstApt"),
                    "departure_date": fare.get("date"),
                    "ticket_timelimit": fare.get("ticketTimelimit"),
                    "class": fare.get("class"),
                    "cos": fare.get("cos"),
                })

            return jsonify({"success": True, "flights": flight_info})
        else:
            return jsonify({"success": False, "error": response.text}), response.status_code


class TwistedFlaskServer:

    def __init__(self, flask_app, port=5000):
        self.flask_app = flask_app
        self.port = port

    def start(self):
        resource = WSGIResource(reactor, reactor.getThreadPool(), self.flask_app)
        site = Site(resource)
        reactor.listenTCP(self.port, site)
        print(f"Twisted server is running on port {self.port}")
        reactor.run()


if __name__ == "__main__":
    # Create the Flask app
    flight_app = FlightSearchApp()

    # Start the Twisted server with Flask
    server = TwistedFlaskServer(flight_app.app, port=5000)
    server.start()
