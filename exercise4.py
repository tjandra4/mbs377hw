import yaml
import json
import xmltodict
from pathlib import Path

# load JSON file and make proteinList of ProteinEntry objects
fldr = Path(__file__).parent
file = fldr / 'uniprot_protein_list.json'
f = open(file, 'r')
d = json.load(f)

# write to YAML
yamlfile = fldr / 'proteins.yaml'

with open(yamlfile, 'w') as y:
    yaml.dump(d, y, sort_keys = False, explicit_start = True, 
              explicit_end = True)