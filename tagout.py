#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import urllib3


def read_json(fname, rootkey=None):
    try:
        with open(fname, 'r') as fp:
            datas = json.load(fp)
            if rootkey is not None:
                if rootkey in datas:
                    return datas[rootkey]
                else:
                    return {}
            return datas
    except:
        return({})


def complete_labels_with_rows(labels, rows):
    for r in rows:
        if r['description'] not in labels:
            labels[r['description']] = {'WHO': "", 'TAG': ""}
        if "dab" in r['type'] and 'dab' not in labels[r['description']]['TAG']:
            labels[r['description']]['TAG'] = "dab"


def save_labels(labels):
    with open("out/labels.json", 'w') as fp:
        json.dump({'labels': labels}, fp, indent=2)


def link_to_google(search):
    # FIXME : Url encode
    url = "https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8".format(
        search)
    return(url)


def labels_to_html(labels):
    html = "<ul>"
    for l in labels:
        state = labels[l]['WHO']
        if state == "":
            html += "<li>{} : <a href=\"{}\" target=_blank>{}</a></li>\n".format(
                l, link_to_google(l), "Unknown")
        else:
            html += "<li>{} : {}</li>\n".format(l, state)
    html += "</ul>\n"
    return(html)


def clean_labels(labels):
    for l in labels:
        if labels[l] == "Unknown":
            labels[l] = {"WHO": "", "TAG": ""}
        elif type(labels[l]) == type(""):
            labels[l] = {"WHO": labels[l], "TAG": ""}


if __name__ == "__main__":
    rows = read_json("out/out.json", 'rows')
    labels = read_json("out/labels.json", 'labels')
    complete_labels_with_rows(labels, rows)
    clean_labels(labels)
    save_labels(labels)
    with open('out/labels.html', 'w') as fp:
        fp.write(labels_to_html(labels))
