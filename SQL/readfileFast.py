#import pandas

import csv
import sys

FinalScienceTaxon = open("FinalTaxons.tsv","w")
finaltaxonheader = ["TaxonId", "sciName","ScientificName","Language","Country"]
final_writer = csv.writer(FinalScienceTaxon,delimiter="\t")
final_writer.writerow(finaltaxonheader)

csv.field_size_limit(sys.maxsize)

#build dict of taxons
sciNamelookup = {}
with open("FinalTaxon.tsv") as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        taxid = line[0]
        sciNamelookup[taxid] = line

count = 0
with open("NameUsage.tsv") as f:
    finalList = csv.reader(f, delimiter="\t")
    #grab accurate scientific name
    for name in finalList:
        if name[3] == "species" and name[2] == "accepted":        
            scienceName = name[4]
            for sciname in sciNamelookup:
                if scienceName == sciNamelookup[sciname][2]:
                    namesdic = ({"taxonId": sciNamelookup[sciname][0],
                                    "sciName": sciNamelookup[sciname][1],
                                    "scientificName": scienceName,
                                    "language": sciNamelookup[sciname][3],
                                    "country":sciNamelookup[sciname][4]})
                    finalSpecies = [namesdic["taxonId"],namesdic["sciName"],namesdic["scientificName"],namesdic["language"],namesdic["country"]]
                    final_writer.writerow(finalSpecies)
                    count +=1
        if count == 10000 or count == 20000 or count == 30000 or count == 40000:
            print(count)
print(count)
FinalScienceTaxon.close()
f.close()



