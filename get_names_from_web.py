#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script retrieves names from a website.
"""

# Import necessary libraries
from bs4 import BeautifulSoup
import pickle
# Define constants
# <tr class="ant-table-row ant-table-row-level-0" data-row-key="서준">
#   <td class="">
#     <a href="/name/%EC%84%9C%EC%A4%80">서준</a>
#   </td>
#   <td class="">2 </td>
#   <td class="">41,457 </td>
# </tr>

def parse_html():
    soup = BeautifulSoup(open("index.html").read(), "html.parser")
    a = soup.find_all("a")
    [print(e.text) for e in a]


def parse_first_names():
    with open("names.txt", "r") as f:
        lines = f.read().split("\n")
        lines = set(lines)
        print(len(lines))
        pickle.dump(lines, open("first_names.pkl", "wb"))

def parse_last_names():
    with open("last_name.txt", "r") as f:
        lines = f.read().replace("\n", " ").split(" ")
        lines = set(lines)
        print(len(lines))
        pickle.dump(lines, open("last_names.pkl", "wb"))

if __name__ == "__main__":
    parse_first_names()
    parse_last_names()