#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import subprocess
import logging  # FIXME : Debug mode


def file_to_pdf(pdffname, txtfname=None):
    """Convert to txt using pdftotext"""
    if txtfname is None:
        txtfname = pdffname[:-3]+"txt"
    logging.info("[pdf->txt] Convert : %s", pdffname)
    subprocess.call(['pdftotext', '-layout', pdffname, txtfname])
    return txtfname


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        file_to_pdf(sys.argv[1])
