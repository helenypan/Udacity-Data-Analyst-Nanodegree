#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should check the "k"
value for each "<tag>" and see if they can be valid keys in MongoDB, as well as
see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys,other_chars,problem_chars):
    if element.tag == "tag":
        k_value = element.attrib['k']
        if lower.search(k_value) is not None:
            keys['lower'] += 1
        elif lower_colon.search(k_value) is not None:
            keys['lower_colon'] += 1
        elif problemchars.search(k_value) is not None:
            keys["problemchars"] += 1
            problem_chars[k_value] += 1
        else:
            keys['other'] += 1
            other_chars[k_value] += 1
    return keys,other_chars,problem_chars

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    other_chars = defaultdict(int)
    problem_chars = defaultdict(int)
    for _, element in ET.iterparse(filename):
        keys,other_chars,problem_chars = key_type(element, keys,other_chars,problem_chars)
    return keys,other_chars,problem_chars



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys,other_chars,problem_chars = process_map('../data/colchester.osm')
    print "Count of different types of k values:"
    pprint.pprint(keys)
    print "Count of other k values:"
    pprint.pprint(other_chars)
    print "Count of problem k values:"
    pprint.pprint(problem_chars)

if __name__ == "__main__":
    test()