#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pdf2txt
import sys
import subprocess
import logging
import re
import csv

r_op = re.compile(
    r'^\s+(?P<op_dd>\d\d)\.(?P<op_mm>\d\d)\s+(?P<first_label>.*?)\s+(?P<val_dd>\d\d)\.(?P<val_mm>\d\d)\s+(?P<amount>[\d\s]+?,\d\d)$')
r_op_more = re.compile(r'^\s+(?P<more_label>.+?)$')
r_op_cb = re.compile(
    r'DU\s(?P<op_dd>\d\d)(?P<op_mm>\d\d)(?P<op_yy>\d\d)\s(?P<first_label>.+)')


def parse_from_txt_to_csv(txtfname):
    csvfname = txtfname[:-3]+"csv"
    rows = []

    with open(txtfname) as file:
        success_before = False
        for line in file:
            m = r_op.match(line)
            if m != None:  # main op
                g = m.groups()
                if success_before:
                    # success just after success, don't loose the previous context !
                    rows.append(row)
                row = ["%s/%s" % (g[0], g[1]), g[2], "%s/%s" %
                       (g[3], g[4]), g[5]]
                success_before = True
                continue
            m = r_op_more.match(line)
            if m != None:  # details (optionnal) for op
                if success_before:  # main op
                    row[1] += "\n"+m.groups()[0]
                    continue
            if success_before:
                rows.append(row)
            if line.strip() != "":
                print(line)
            success_before = False

    with open(csvfname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return csvfname


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        txtfname = pdf2txt.file_to_pdf(sys.argv[1])
        csvfname = parse_from_txt_to_csv(txtfname)
