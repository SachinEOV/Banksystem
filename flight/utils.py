from lxml import etree

def create_flight_request_xml(data):
    """
    Create the XML structure for the flight request based on the input data.
    """
    fare_request = etree.Element("fareRequest", da="true")

    vcrs = etree.SubElement(fare_request, "vcrs")
    etree.SubElement(vcrs, "vcr").text = "BA"

    etree.SubElement(fare_request, "fareTypes", xmlns="http://ypsilon.net/shared")
    etree.SubElement(fare_request, "tourOps")

    flights = etree.SubElement(fare_request, "flights")
    etree.SubElement(flights, "flight", depApt=data["dep_apt"], dstApt=data["dst_apt"], depDate=data["dep_date"])
    if data.get("return_date"):
        etree.SubElement(flights, "flight", depApt=data["dst_apt"], dstApt=data["dep_apt"], depDate=data["return_date"])

    paxes = etree.SubElement(fare_request, "paxes")
    for pax in data.get("passengers", []):
        etree.SubElement(
            paxes,
            "pax",
            surname=pax["surname"],
            firstname=pax["firstname"],
            dob=pax["dob"],
            gender=pax["gender"],
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
    return xml_request_body
