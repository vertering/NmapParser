"""The Nmap XML output is unreadable and not usable by Excel. This script parses one or more XML files into an Excel
sheet. Note, in order to show hosts that are down, nmap should run with the -v flag In order to run this xlswriter
must be installed: pip install xlsxwriter. Usage of the script is: python NmapParser.py nmap1.xml nmap2.xml """

from xml.etree import ElementTree as et
import sys
import xlsxwriter

header_result = ["IP", "Hostname", "Protocol", "Port", "Open", "Protocol name", "Protocol product"]
result_list = []
result_list.append(header_result)
headerHosts = ["IP", "Hostname"]
up_hosts = []
up_hosts.append(headerHosts)
down_hosts = []
down_hosts.append(headerHosts)
for argument in sys.argv[1:]:
    tree = et.parse(argument)
    root = tree.getroot()
    for host in root.iter("host"):
        status = host.find("status").attrib
        if (status["state"]) == "up":
            address = host.find("address").attrib["addr"]
            hostname = None
            for host_names in host.find("hostnames"):
                if "name" in host_names.attrib:
                    hostname = host_names.attrib["name"]
            upHost = (address, hostname)
            up_hosts.append(upHost)
            for ports in host.findall("ports"):
                # For host element and port sub element without any ports
                if not ports.findall("port"):
                    result = (address, hostname, None, None, None, None, None)
                    result_list.append(result)
                # For host element and port sub element with ports
                else:
                    for port in ports.findall("port"):
                        protocol = port.attrib["protocol"]
                        portId = port.attrib["portid"]
                        state = None
                        protocol_name = None
                        protocol_product = None
                        for filtered in port.findall("state"):
                            state = filtered.attrib["state"]
                        for service in port.findall("service"):
                            protocol_name = service.attrib["name"]
                            if "product" in service.attrib:
                                protocol_product = service.attrib["product"]
                        result = (address, hostname, protocol, portId, state, protocol_name, protocol_product)
                        result_list.append(result)
        if (status["state"]) == "down":
            address = host.find("address").attrib["addr"]
            hostname = None
            if host.find("hostnames") is not None:
                for host_names in host.find("hostnames"):
                    if "name" in host_names.attrib:
                        hostname = host_names.attrib["name"]
            down_host = (address, hostname)
            down_hosts.append(down_host)
workbook = xlsxwriter.Workbook('NmapParser.xlsx')
worksheet = workbook.add_worksheet("Results")
rowNumber = 3
for result in result_list:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
worksheet = workbook.add_worksheet("Hosts up")
rowNumber = 3
for result in up_hosts:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
worksheet = workbook.add_worksheet("Hosts down")
rowNumber = 3
for result in down_hosts:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
workbook.close()
