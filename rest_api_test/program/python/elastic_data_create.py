import sys, os
import xml.etree.ElementTree as ET
import json

class tc_data:
    def __init__(self, 
                 round,
                 ts_name,
                 tc_name,
                 status,
                 timestamp,
                 total_time,
                 http_method):
        self.round = round
        self.ts_name = ts_name
        self.ts_id = ts_name.split("::")[0]
        self.tc_name = tc_name
        self.tc_id = tc_name.split("::")[0]
        self.status = status
        self.timestamp = timestamp
        self.total_time = total_time
        self.http_method = http_method
        self.messages = []

    def __lshift__(self, other):
        assert self.ts_name == other.ts_name
        assert self.tc_name == other.tc_name
        assert self.round == other.round

        self.status = other.status
        self.timestamp = other.timestamp
        self.total_time += other.total_time
        return self

    def to_dict(self):
        return {
            "round": self.round,
            "idTS": self.ts_id,
            "nameTS": self.ts_name,
            "idTC": self.tc_id,
            "nameTC": self.tc_name,
            "status": self.status,
            "timestamp": self.timestamp,
            "totalTime": self.total_time,
            "httpMethod": self.http_method,
            "message": '\n'.join(filter(None, self.messages))
        }


test_suites = {
    "01": {
        "name": "GET",
        "tests": {
            "01": {
                "name": "GET neexistujici",
            },
            "02": {
                "name": "GET existujici",
            },
        }
    },
    "02": {
        "name": "POST",
        "tests": {
            "01": {
                "name": "POST validni",
            },
            "02": {
                "name": "POST nevalidni",
            },
        }
    },
    "03": {
        "name": "PUT",
        "tests": {
            "01": {
                "name": "PUT zmena uzivatele",
            },
        }
    },
    "04": {
        "name": "DELETE",
        "tests": {
            "01": {
                "name": "DELETE neexistujici",
            },
            "02": {
                "name": "DELETE existujici",
            },
        }
    }
}

def ts_tc_from_tk(tk_name):
    Id = tk_name.split("::")[0]
    Id = Id.split(".")
    ts = f"TS.{Id[1]}::{test_suites[Id[1]]['name']}"
    tc = f"TC.{Id[1]}.{Id[2]}::{test_suites[Id[1]]['tests'][Id[2]]['name']}"
    return ts, tc


if __name__ == "__main__":
    inter_dir = sys.argv[1] if len(sys.argv) > 1 else "../../soapui/test-output"
    out_file = "../rest-elastic.json"
    xml_file = "test_case_run_log_report.xml"
    TCs = {}
    for round in os.listdir(inter_dir):
        TCs[round] = {}
        root = ET.parse(os.path.join(inter_dir, round, xml_file)).getroot()
        for tk in root:
            ts,tc = ts_tc_from_tk(tk.attrib["name"])
            data = tc_data(round, ts, tc, tk.attrib["status"], tk.attrib["timestamp"], float(tk.attrib["totalTime"]), ts.split("::")[1])
            if tc not in TCs[round]:
                TCs[round][tc] = data
            else:
                TCs[round][tc] <<= data
            if len(tk) > 0: # messages are children of tk
                for message in tk:
                    TCs[round][tc].messages.append(message.text)
    out_data = [ tc.to_dict() for round in TCs.values() for tc in round.values() ]
    with open(out_file, "w") as f:
        json.dump(out_data, f, indent=4)
