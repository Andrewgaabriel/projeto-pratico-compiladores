import sys
import pandas as pd
import xml.etree.ElementTree as ET

# ENTRADAS
parsing = ET.parse('../inputs/GoldParser.xml')
root = parsing.getroot()