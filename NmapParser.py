"""The Nmap XML output is unreadable and not usable by Excel. This script parses one or more XML files into an Excel
sheet. Note, in order to show hosts that are down, nmap should run with the -v flag In order to run this xlswriter
must be installed: pip install xlsxwriter. Usage of
the script is: python NmapParser.py nmap1.xml nmap2.xml """

from xml.etree import ElementTree as Et
import sys
import xlsxwriter

headerResult = ["IP", "Hostname", "Protocol", "Port", "Open", "Version"]
resultList = []
resultList.append(headerResult)
headerHosts = ["IP", "Hostname"]
upHosts = []
upHosts.append(headerHosts)
downHosts = []
downHosts.append(headerHosts)
for argument in sys.argv[1:]:
    tree = Et.parse(argument)
    root = tree.getroot()
    for host in root.iter("host"):
        status = host.find("status").attrib
        if (status["state"]) == "up":
            address = host.find("address").attrib["addr"]
            hostname = None
            protocol = None
            portId = None
            state = None
            version = None
            for hostNames in host.find("hostnames"):
                if "name" in hostNames.attrib:
                    hostname = hostNames.attrib["name"]
            upHost = (address, hostname)
            upHosts.append(upHost)
            for ports in host.findall("ports"):
                # For host element and port sub element without any ports
                if not ports.findall("port"):
                    result = (address, hostname, protocol, portId, state, version)
                    resultList.append(result)
                # For host element and port sub element with ports
                else:
                    for port in ports.findall("port"):
                        protocol = port.attrib["protocol"]
                        portId = port.attrib["portid"]
                        for filtered in port.findall("state"):
                            state = filtered.attrib["state"]
                        for name in port.findall("service"):
                            if "product" in name.attrib:
                                version = name.attrib["product"]
                        result = (address, hostname, protocol, portId, state, version)
                        resultList.append(result)
        if (status["state"]) == "down":
            address = host.find("address").attrib["addr"]
            hostname = None
            if host.find("hostnames") is not None:
                for hostNames in host.find("hostnames"):
                    if "name" in hostNames.attrib:
                        hostname = hostNames.attrib["name"]
            downHost = (address, hostname)
            downHosts.append(downHost)
workbook = xlsxwriter.Workbook('NmapParser.xlsx')
worksheet = workbook.add_worksheet("Results")
rowNumber = 3
for result in resultList:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
worksheet = workbook.add_worksheet("Hosts up")
rowNumber = 3
for result in upHosts:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
worksheet = workbook.add_worksheet("Hosts down")
rowNumber = 3
for result in downHosts:
    worksheet.write_row("C" + str(rowNumber), result)
    rowNumber += 1
workbook.close()
