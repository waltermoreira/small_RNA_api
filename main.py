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

    # Expect JSON argument like this python command.
    input_chr = arg['chr']
    input_beg = arg['beg']
    input_end = arg['end']
    # Example:
    # main.search({'chr':1,'beg':9000,'end':9400})
    # That equates to this URL.
    # 'http://mpss.udel.edu/web/php/pages/abundances.php?SITE=at_sRNA&chrnum=1&beg=9000&end=9400&format=json'

    # The remote site tolerates beg>end, so 200 to 100 is treated as 100 to 200.
    # The remote site tolerates non-integers, so 2000.1 is treated as 2000.
    # The remote site tolerates negative coordinates, so 0 to 1000 is same as -1000 to 1000.
    # The remote site admin says to use chrnum=6 for chloroplast and chrnum=7 for mitochondria.
    # We will allow {6, 'C', 'c'} as equivlanets. Same for {7, 'M', 'm'}.
    if str(input_chr).lower() == 'c':
        input_chr = 6
    if str(input_chr).lower() == 'm':
        input_chr=7

    # The remote service takes additional parameters that we will hard code.
    #   format=json
    #   SITE=at_sRNA  (indicates small RNA for Arabidopsis thaliana)
    # We will expose all of SITE=at_sRNA as one endpoint called at_sRNA.
    url = ('http://mpss.udel.edu/web/php/pages/abundances.php?SITE=at_sRNA'
           '&chrnum={chr}&beg={beg}&end={end}&format=json'
           .format(chr=input_chr, beg=input_beg, end=input_end))

    rqst = requests.get(url)

    # If the response status is not 2xx, raise an exception with the
    # proper error message
    rqst.raise_for_status()

    # if we are here, it means the request was successful
    try:
        # try to decode the JSON response (it will succeed even if the
        # content type is not properly set, but the response is really
        # a JSON object)
        payload = rqst.json()
    except ValueError:
        raise Exception('could not decode JSON object')

    abundance_data = payload['abundance_data']
    for one_seq in abundance_data:
        # Each one_seq includes the key tuple "sequence": "AAAGGGAAAGAACCC",
        # and a few descriptive tuples (hits, position, strand)
        # and an array (abundance_table) of objects, where each object is "lib":value. 
        # Note "hits" value counts hits genome wide, not just this chromosome.

        # Here, add optional code to reformat the JSON object.
        # None required.

        decoded = json.dumps(one_seq)
        print decoded
        print '---'
