import os, sys

properties = ("sla", "slaGET", "login", "loginDELETE")

LONG_SLA = 7000
SHORT_SLA = 10

runsets = [
    (LONG_SLA, LONG_SLA, "mladyPTE", "mladyPTE"),
    (SHORT_SLA, LONG_SLA, "mladyPTE", "mladyPTE"),
    (LONG_SLA, SHORT_SLA, "mladyPTE", "mladyPTE"),
    (SHORT_SLA, SHORT_SLA, "mladyPTE", "mladyPTE"),
    (LONG_SLA, LONG_SLA, "mladyPTE", "mlady"),
]

def gen_pargs(runset):
    return [f"-P{p[0]}={p[1]}" for p in zip(properties, runset)]

if __name__ == "__main__":
    soap_path = os.getenv('SOAPUI_HOME')
    if soap_path is None:
        print("SOAPUI_HOME not set")
        sys.exit(1)
    soap_path = os.path.join(soap_path, 'bin', 'testrunner.bat')
    try:
        outdir = sys.argv[1]
    except IndexError:
        outdir = "test-output"
    args = [soap_path ,"-rMI"]

    for round, runset in enumerate(runsets,1):
        pargs = gen_pargs(runset)
        os.system(" ".join(args + pargs + [f"-f{outdir}/{round:02}", "REST-SamPrace-soapui-project.xml"]))
