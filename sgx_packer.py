#!/bin/python3
import shutil
import sys
import os

destdir = sys.argv[1]
boms = sys.argv[2:]

print("Grabbing BOMs from %s and copying results to %s" % (boms, destdir))

def get_bom_inputs(boms):
    files = []

    for bom in boms:
        with open(bom, 'r') as bomf:
            for line in bomf.readlines():
                if line.startswith("DeliveryName"):
                    continue
                inname, outname, _ = line.split(maxsplit=2)
                inname = inname.replace("<deliverydir>/", "")
                outname = outname.replace("<installdir>/", "")

                files.append((inname, outname))

    return files


for inname, outname in get_bom_inputs(boms):
    outdir = os.path.join(destdir, os.path.dirname(outname))
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    shutil.copyfile(inname, os.path.join(destdir, outname))
