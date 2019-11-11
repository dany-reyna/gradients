import os
import random


def random_filename(dirname, suffixes, prefix=""):
    if not isinstance(suffixes, list):
        suffixes = [suffixes]

    suffixes = [p if p[0] == "." else "." + p for p in suffixes]

    while True:
        bname = "%09d" % random.randint(0, 999999999)
        fnames = []
        for suffix in suffixes:
            fname = os.path.join(dirname, prefix + bname + suffix)
            if not os.path.isfile(fname):
                fnames.append(fname)

        if len(fnames) == len(suffixes):
            break

    if len(fnames) == 1:
        return fnames[0]
    else:
        return fnames
