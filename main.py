# file: main.py

import requests
import json

def list(arg):
    pass

def search(arg):

    # The requests object contains HTTP headers plus payload.
    # print r.headers
    # The remote service sets cookies. For now, we do not pass the cookie.
    # print headers['set-cookie']

    # The output may be ordered differently than the input.
    # In particular, the "sequence" tuple may be buried in the list.

    # For now, hard code an example URL.
    url = 'http://mpss.udel.edu/web/php/pages/abundances.php?SITE=at_sRNA&chrnum=1&beg=9000&end=9400&format=json'
    rqst = requests.get(url)

    if rqst.ok:
        content_type = rqst.headers['content-type']
        if "application/json" in content_type:
            payload = rqst.json()
            # The payload includes this metadata.
            # payload['SITE'] = "at_sRNA"
            # payload['annotation'] = "TAIR10"
            # payload ['species'] = "Arabidopsis thaliana"
            # For now, we will filter out the metadata.
            lib_abundances = payload['lib_abundances']
            for one_seq in lib_abundances:                
                # Each one_seq includes the key tuple "sequence": "AAAGGGAAAGAACCC",
                # and a few descriptive tuples (hits, position, strand, length).
                # Some are inferrable from the data: hits, length.
                # Separate out the others.
                seq_sequence = one_seq['sequence']
                seq_position = one_seq['position']
                seq_strand   = one_seq['strand']
                del one_seq['sequence']
                del one_seq['position']
                del one_seq['strand']
                del one_seq['hits']
                del one_seq['length']
                # What is left is many tuples of <line>:<abundance> like "Col0":0.
                one_rec = {
                        'sequence':seq_sequence,
                        'position':seq_position,
                        'strand':seq_strand,
                        'abundance_table':one_seq}
                decoded = json.dumps(one_rec)
                print decoded
                print '---'
            
        
        else:
            return
    

        
    


