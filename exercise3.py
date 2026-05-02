import json
import xmltodict
from pathlib import Path

# load JSON file and make proteinList of ProteinEntry objects
fldr = Path(__file__).parent
file = fldr / 'uniprot_protein_list.json'
f = open(file, 'r')
d = json.load(f)

# create one root
root = {}
root['data'] = d

# write to XML file
xmlfile = fldr / 'proteins.xml'
with open(xmlfile, 'w') as x:
    x.write(xmltodict.unparse(root, pretty = True))

