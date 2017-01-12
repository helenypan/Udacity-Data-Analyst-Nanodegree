"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "../data/colchester.osm"

postcode_pattern = re.compile(r'^[A-Z]{2}[1-9][0-9]?\s[0-9]{1,2}[A-Z]{2}$')


def audit_postcode(postcodes, cur_postcode):
    m = postcode_pattern.search(cur_postcode)
    if not m:
        postcodes.add(cur_postcode)


def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode") or \
        (elem.attrib['k'] == "postal_code") or \
        (elem.attrib['k'] == "postcode")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    postcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    audit_postcode(postcodes, tag.attrib['v'])
    osm_file.close()
    return postcodes


def update_postcode(name):
    m = postcode_pattern.search(name)
    if not m:
        if name.startswith('C0'):
            return name.replace('C0',"CO")
        elif "!" in name:
            return name.replace("!","")
        elif name.startswith('CO11  '):
            return name.replace('CO11  ',"CO11 ")
        elif name.endswith(' '):
            return name.strip()
        elif name=="co7 0pp":
            return name.upper()
        else:
            return None
    else:
        return name



def test():
    postcodes = audit(OSMFILE)
    pprint.pprint(postcodes)

    for postcode in postcodes:
        better_name = update_postcode(postcode)
        print postcode, "=>", better_name


if __name__ == '__main__':
    test()