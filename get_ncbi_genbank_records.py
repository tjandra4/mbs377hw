#!/usr/bin/env python3
from Bio import Entrez
from Bio import SeqIO
import socket
import logging
import argparse

# -------------------------
# Logging setup
# -------------------------
# Create a parser object responsible for reading/understanding command-line arguments
a_parser = argparse.ArgumentParser()

a_parser.add_argument('output_file', type = str, help = "Path to output TXT file")
a_parser.add_argument('search_term', 
                      type = str, 
                      required = False,
                      default = 'Arabidopsis thaliana AND AT5G10140',
                      help = 'Specific search term'),
a_parser.add_argument('-l', '--loglevel',
                    type=str,
                    required=False,
                    default='WARNING',
                    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')

# Create object that will store command-line arguments provided by the user
args = a_parser.parse_args()

# Use user-defined log level
format_str = (
    f'[%(asctime)s {socket.gethostname()}] '
    '%(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s')
logging.basicConfig(level=args.loglevel, format=format_str)

def fetch_gbrecs(GI_nums: list) -> list:
    ids = ",".join(GI_nums)
    with Entrez.efetch(db="protein", id=ids, rettype="gb", retmode="text") as h:
        record = SeqIO.parse(h, "gb")
        rec_list = list(record)
        return rec_list

def search_ncbi(key_term: str, retmax: int) -> list:
    try:
        with Entrez.esearch(db = "protein", term = key_term) as h:
            results = Entrez.read(h)
            records = fetch_gbrecs(results.get('IdList'))
            logging.info(f"Records in {args.output_file}")
            return records
    except FileNotFoundError:
        logging.error(f"{args.search_term} not found. Exiting")
        sys.exit(1) 

def store_redis(records: list) -> None:
    try:
        rdata = redis.Redis(host = "localhost", port = 6379, decode_responses = True)

        for r in records:
            rd = {"id": r.id, "name": r.name, "description": r.description,
                  "sequence": str(r.seq)}
            rdata.set(r.id, json,dumps(rd))
        logging.info(f"Stored record data in Redis")
    except:
        logging.info(f"Could not be stored in Redis")
        sys.exit(1)

def extract_redis(output: str) -> None:
    rdata = redis.Redis(host = "localhost", port = 6379, decode_responses = True)
    with open(output, "w") as o:
        for r in rdata:
            rinfo = rdata.get(r)
            f.write(f"ID: {rinfo.get('id')}\n")
            f.write(f"Name: {rinfo.get('name')}\n")
            f.write(f"Description: {rinfo.get('description')}\n")
            f.write(f"Sequence: {rinfo.get('sequence')}\n\n")



def main() -> None:
    logging.info(f"Starting search of {args.search_term}")
    records = search_ncbi(args.search_term, 30)
    store_redis(records)
    extract_redis(args.output_file)


if __name__ == "__main__":
    main()