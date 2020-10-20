# NmapParser
The Nmap XML output is unreadable and not usable by Excel. This script parses one or more XML files into an Excel
sheet. Note, in order to show hosts that are down, nmap should run with the -v flag In order to run this xlswriter
must be installed: pip install xlsxwriter. Usage of the script is: python NmapParser.py nmap1.xml nmap2.xml
