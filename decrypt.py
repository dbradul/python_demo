import sys
from string import ascii_lowercase
from functools import reduce

#------------------------------------------------------------
# Manually supported dict. for improper recognized symbols
# Holds relation decoded -> actual symbol
exceptions = {
    'h': 'n',
    'f': 'y',
    # 'k':'v',
    # 'm':'w',
    # 'c':'m',
    # 'w':'c',
    # 'z':'q',
    # '{':'v'
}

#------------------------------------------------------------
def map_dicts_by_values(d1, d2):
    '''
    Maps 2 dicts according to their values
    :param d1:
    :param d2:
    :return: Keys of mapped dicts
    '''
    mapped_keys = {l:r for l, r in zip(sorted(d1, key=d1.get),
                                       sorted(d2, key=d2.get))}
    return mapped_keys

#------------------------------------------------------------
def get_stats(text):
    '''
    Creates frequency dict for the given text
    :param text: Text to process
    :return: Frequency dict: letter->number of occur.
    '''

    stats = {}

    _ = [stats.__setitem__(c, stats.get(c, 0)+1)
                    for c in text if c in ascii_lowercase]

    return stats

#------------------------------------------------------------
def decode(text, matches):
    '''
    Decrypts text using letters mapping
    :param text: Text to decrypt
    :param letters_map: Letters mapping
    :return: Decrypted text
    '''
    pipeline = [matches, exceptions]

    decoded = map(lambda c: reduce(lambda c, p: p.get(c, c), pipeline, c), text)

    result = "".join(list(decoded))

    return result


#----------------------------------------------------------
if __name__ == "__main__":
    # command line arguments
    filename_ref = sys.argv[1]
    filename_enc = sys.argv[2]
    filename_dec = sys.argv[3]

    # calc letter frequency for normal text
    # will be used as a reference frequency
    with open(filename_ref) as f:
        stats_ref = get_stats(f.read().lower())

    # calc letter frequency for encrypted text
    with open(filename_enc) as f:
        text    = f.read().lower()
        stats   = get_stats(text)

    # map reference<->encrypted letters according to their frequencies
    decode_map  = map_dicts_by_values(stats, stats_ref)

    # decode text
    decoded     = decode(text, decode_map)

    print(decoded)

    # save decoded text
    with open(filename_dec, "w") as f:
        f.write(decoded)

    # save ref<->enc letters mapping
    with open("key.map", "w") as f:
        for k, v in decode_map.items():
            f.write("{0}:{1}\n".format(k, exceptions.get(v, v)))