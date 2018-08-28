#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import formatter
import predictor
import json

if __name__ == "__main__":
    level = 0.1
    datafield = "description"
    while(True) :
        print("--Level : %f" % level)
        rows = formatter.read_json("out/out.json", 'rows')
        print("--Rows : %d" % len(rows))
        whos = set(["ME", "US", "?"])
        step = 5
        train = []
        test = []
        pipe = predictor.get_pipe()
        for row in rows:
            if 'trained' in row:
                row['trained'] = row['trained'].upper()
                train.append((row[datafield], row['trained']))
                whos.add(row['trained'])
            else :
                test.append(row)
        print("--TRAIN : %d" % len(train))
        print("--TEST : %d" % len(test))
        #print(train)
        found = 0
        if len(train) >= step:
            print("--Tags : %s" % (whos))
            pipe.fit([x[0] for x in train], [x[1] for x in train])
            counter = 0

            for row in test :
                pred_data = pipe.predict([row[datafield]])
                row['prediction'] = pred_data[0]
                decision_function = pipe.decision_function([row[datafield]])[0]
                #print("%s / %s / %s" % (row[datafield], row['prediction'], decision_function))
                try:
                    row['confidence'] = max(decision_function)
                except:
                    row['confidence'] = decision_function
                if row['confidence'] > level:
                    found += 1
                    continue
                counter += 1
                if counter >= step :
                    break
                #print("%f" % row['confidence'])
        counter = 0
        
        prevset = []
        for row in test:
            #print(row)
            if row[datafield] in prevset :
                continue
            prevset.append(row[datafield])
            prediction = ""
            confidence = -1.
            if 'confidence' in row and row['confidence'] > level:
                #print('!!! %s (%.1f%%)\n%s' % (row['prediction'], 100.*row['confidence'], row[datafield]))
                continue
            elif 'confidence' in row :
                #print("%f : %s" % (row['confidence'], row['prediction']))
                prediction = row['prediction']
                confidence = row['confidence']

            who = ""
            while who not in whos:
                who = input("%s - %s\n%.1f%% - %s>" % (row['amount'], row[datafield], 100.*confidence, prediction))
                who = who.upper()
                if who == "":
                    who = prediction
            row['trained'] = who
            counter += 1
            if counter >= step :
                break
        if counter < step :
            level += (1.-level)*0.5
        print("\n--%d found, %d set, %d total" % (found, len(train)+counter, len(rows)))
        with open("out/out.json", 'w') as fp:
            json.dump({'rows': rows}, fp, indent=2)