"""
The Nmap XML output is unreadable and not usable by Excel. This script parses one or more XML files into an Excel
sheet called NmapParser.xlsx
Usage of the script is: python NmapParser.py nmap1.xml nmap2.xml
"""

from xml.etree import ElementTree as Et
import sys
import xlsxwriter

resultList = []
header = ["IP", "Hostname", "Protocol", "Port", "Open", "Version"]
resultList.append(header)
for argument in sys.argv[1:]:
    tree = Et.parse(argument)
    root = tree.getroot()
    for host in root.iter("host"):
        up = host.find("status").attrib
        if (up["state"]) == "up":
            address = host.find("address").attrib["addr"]
            hostname = None
            for hostnames in host.find("hostnames"):
                if "name" in hostnames.attrib:
                    hostname = hostnames.attrib["name"]
            for ports in host.findall("ports"):
                for port in ports.findall("port"):
                    protocol = port.attrib["protocol"]
                    portid = port.attrib["portid"]
                    state = None
                    for filter in port.findall("state"):
                        state = filter.attrib["state"]
                    version = None
                    for name in port.findall("service"):
                        if "product" in name.attrib:
                            version = name.attrib["product"]
                    result = (address, hostname, protocol, portid, state, version)
                    resultList.append(result)
workbook = xlsxwriter.Workbook('NmapParser.xlsx')
worksheet = workbook.add_worksheet()
rowNumber = 3
for result in resultList:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
workbook.close()
