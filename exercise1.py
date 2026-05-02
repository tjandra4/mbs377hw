import json
from pydantic import BaseModel
from pathlib import Path


class ProteinEntry(BaseModel):
    primaryAccession: str
    organism: dict
    proteinName: str
    sequence: dict
    geneName: str
    function: str

# create list of ProteinEntry objects
def make_proteinList(data: dict) -> list:
    p_input = data['protein_list']
    pL = []
    for p in p_input:
        p_pA = p['primaryAccession']
        p_org = p['organism']
        p_name = p['proteinName']
        p_seq = p['sequence']
        p_gene = p['geneName']
        p_func = p['function']
        new_p = ProteinEntry(primaryAccession = p_pA, organism = p_org, 
                             proteinName = p_name, sequence = p_seq, 
                             geneName = p_gene, function = p_func)
        pL.append(new_p)
    return pL


# prints the total combined mass of all proteins in the dataset.
def find_total_mass(data: list) -> int:
    sum = 0
    for p in data:
        sum += p.sequence.get('mass')
    return sum

# prints a list of protein names of any proteins with a sequence length greater 
# than or equal to 1000.
def find_large_proteins(data: list) -> list:
    lp_names = []
    for p in data:
        if p.sequence.get('length') >= 1000:
            lp_names.append(p.proteinName)
        else: continue
    return lp_names

# prints a list of protein names of any non-eukaryotic proteins in the dataset
# Hint: A protein is considered non-eukaryotic if “Eukaryota” does not appear
def find_non_eukaryotes(data: list) -> list:
    non_euk_names = []
    for p in data:
        lineage = p.organism.get('lineage')
        if lineage[0] == 'Eukaryota':
            non_euk_names.append(p.proteinName)
        else: continue
    return non_euk_names


# load JSON file
fldr = Path(__file__).parent
file = fldr / 'uniprot_protein_list.json'
f = open(file, 'r')
d = json.load(f)

p_list = make_proteinList(d)
print(find_total_mass(p_list))
print(find_large_proteins(p_list))
print(find_non_eukaryotes(p_list))

    