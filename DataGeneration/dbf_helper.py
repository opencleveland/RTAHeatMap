# The sole purpose of this method is to convert the .dbf file that we have
# received which contains all addresses in the city to a .csv file
import dbfread as dbf  #To read our .dbf file
import csv             #To write to .csv

def convert_addresses_to_csv():
  with open('addresses.csv', 'wb') as csvfile:
    headerexists = False
    for rec in dbf.DBF('LBRS_Site.dbf'):
      if headerexists == False:
        writer = csv.DictWriter(csvfile, fieldnames=rec.keys())
        writer.writeheader()
        headerexists = True
      writer.writerow(rec)