import json
import csv
from pathlib import Path
import exercise1 as e1

# load JSON file and make proteinList of ProteinEntry objects
fldr = Path(__file__).parent
file = fldr / 'uniprot_protein_list.json'
f = open(file, 'r')
d = json.load(f)
p_list = e1.make_proteinList(d)


col_names = ['primaryAccession', 'proteinName', 'geneName', 
             'organism_scientificName', 'sequence_length', 'sequence_mass',
             'function']

# write to CSV file
csvfile = fldr / 'proteins.csv'
with open(csvfile, 'w', newline = '') as p_file:
    w = csv.writer(p_file)
    w.writerow(col_names)
    
    # iterate through proteinList and add data
    for p in p_list:
        r = []
        r = [p.primaryAccession, p.proteinName, p.geneName,
             p.organism.get('scientificName'), p.sequence.get('length'), 
             p.sequence.get('mass'), p.function]
        w.writerow(r)


