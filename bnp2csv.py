#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pdf2txt
import sys
import subprocess
import logging
import re
import csv
import copy

# line patterns
r_op = re.compile(
    r'^\s+(?P<op_dd>\d\d)\.(?P<op_mm>\d\d)\s+(?P<label>.*?)\s+(?P<val_dd>\d\d)\.(?P<val_mm>\d\d)\s+(?P<amount>[\d\s]+?,\d\d)$')
r_op_more = re.compile(r'^\s+(?P<more_label>.+?)$')

# label patterns
r_op_cb = re.compile(
    r'.*DU\s(?P<label_dd>\d\d)\s*(?P<label_mm>\d\d)\s*(?P<label_yy>\d\d)\s(?P<second_label>.+)', re.M | re.S)
r_op_dab = re.compile(
    r'RETRAIT\sDAB\s(?P<label_dd>\d\d)/(?P<label_mm>\d\d)/(?P<label_yy>\d\d).*?\n(?P<second_label>.*?)\n', re.M | re.S)
r_op_sepa_virement = re.compile(
    r'VIR\sSEPA\sRECU\s/DE\s(?P<second_label>.*?)\s/MOTIF\s(?P<sepa_motif>.*?)\s?/REF\s(?P<sepa_ref>.*)$', re.M | re.S)
r_labels = {'cb': r_op_cb, 'dab': r_op_dab, 'sepavir': r_op_sepa_virement}


def parseline_main_op(line, current_op):
    """Parse main operation"""
    m = r_op.match(line)
    if m != None:  # main op
        current_op = m.groupdict()
        current_op['type'] = ["main"]
        return(current_op)
    return(None)


def parseline_more_op(line, current_op):
    """Parse multiline operation"""
    m = r_op_more.match(line)
    if m != None and current_op is not None:  # details (optionnal) for op
        current_op['label'] += "\n%s" % m.group('more_label')
        current_op['type'].append('more')
        return(current_op)
    return(None)


def parseop_label(op):
    for typ in r_labels:
        rop = r_labels[typ]
        m = rop.match(op['label'])
        if m != None:  # details (optionnal) for op
            op.update(m.groupdict())
            op['type'].append(typ)
            break
    return(op)


def write_csv(csvfname, dictrows):
    for dr in dictrows:
        if "label_dd" in dr:
            dr['date'] = "%s/%s" % (dr['label_dd'], dr['label_mm'])
        elif "op_dd" in dr:
            dr['date'] = "%s/%s" % (dr['op_dd'], dr['op_mm'])
        else:
            raise ValueError
        if "second_label" in dr:
            dr['description'] = dr['second_label']
        elif "label" in dr:
            dr['description'] = dr['label']
        else:
            raise ValueError
        if "amount" not in dr:
            raise ValueError

    with open(csvfname, 'w', newline='') as f:
        writer = csv.DictWriter(
            f, ['date', 'description', 'amount', 'flag', 'label', 'type'], restval="", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(dictrows)


def parse_from_txt(txtfname):
    success = 0
    ops = []
    noops = []
    with open(txtfname) as file:
        current_op = None
        for line in file:
            op = parseline_main_op(line, current_op)
            if op:
                success += 1
                ops.append(op)
                current_op = op
                continue
            if parseline_more_op(line, current_op):
                continue
            current_op = None
            noops.append(line)

        for o in ops:
            o = parseop_label(o)
            o['type'] = ",".join(o['type'])
            for k in o:
                o[k] = re.sub(" +", " ", o[k]).strip()

    return(ops, noops)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        globalops = []
        globalnoops = []
        for fname in sys.argv[1:]:
            txtfname = pdf2txt.file_to_pdf(fname)
            ops, noops = parse_from_txt(txtfname)
            globalops += ops
            globalnoops += noops
        write_csv("out.csv", globalops)
        with open("excluded.txt", 'w') as f:
            for l in globalnoops:
                f.write(l)
