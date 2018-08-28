#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import tagout

if __name__ == "__main__":
    labels = tagout.read_json("out/labels.json", 'labels')
    counter = 0
    whos = []
    tags = []
    for label in labels :
        dat = labels[label]
        if dat['WHO'] not in whos :
            whos.append(dat['WHO'])
        mtags = dat['TAG'].split(' ')
        for tag in mtags :
            if tag not in tags :
                tags.append(tag)

    whostr = " ".join(whos)
    tagstr = " ".join(tags)
    for label in labels :
        dat = labels[label]
        print(dat)
        done = False
        if dat['WHO'] == '':
            who = input("\nWHO is %s ?\n%s\n> " % (label, whostr))
            dat['WHO'] = who.strip()
            if dat['WHO'] not in whos :
                y = input("Want to add %s in the Who's who ?\ny/n >" % dat['WHO'])
                if y == 'y':
                    whos.append(dat['WHO'])
                    whostr = " ".join(whos)
            done = True
        if dat['TAG'] == '':
            tag = input("\nTAG for %s\n%s\n> " % (label, tagstr))
            dat['TAG'] = tag.strip()
            mtags = dat['TAG'].split(' ')
            for tag in mtags :
                if tag not in tags :
                    y = input("\nWant to add %s in the tag list ?\ny/n >" % tag)
                    if y == 'y':
                        tags.append(tag)
                        tagstr = " ".join(tags)
            done = True
        if done:
            counter += 1
        if counter > 10:
            break
    tagout.save_labels(labels)
