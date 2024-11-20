import sys
import xml.etree.ElementTree as ET
import json

if __name__ == "__main__":
    inter_dir = sys.argv[1] if len(sys.argv) > 1 else "../../soapui/test-output"
    out_file = "rest-elastic.json"