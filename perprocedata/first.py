# -*- coding: utf-8 -*-
import csv

rawfilename = 'E:\explore\scrapy\lol-getdatas\\tutorial\persongame.csv'
nextFilename = 'E:\explore\scrapy\lol-getdatas\perprocedata\\first.csv';
with open(rawfilename) as fr:
    with open(nextFilename, "w") as fn:
        reader = csv.reader(fr)
        head_row = next(reader)
        writer = csv.writer(fn)
        for row in reader:
            line = []
            if row[4] == '(Blue Team)':
                line = row[3].split(',') + row[0].split(',')+ [0]
            else:
                line = row[0].split(',') + row[3].split(',')+ [1]
            writer.writerow(line)
        fn.close()
    fr.close()
