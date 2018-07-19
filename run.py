# -*- coding: utf-8 -*-
import os
import shutil
import json
import pandas as pd
from pymongo import MongoClient
from slugify import slugify

# Const
RAW_DATA_DIR = './data/raw/'
FORMATTED_DATA_DIR = './data/formatted/'
DB_NAME = 'anticorruption'
DB_COLLECTION = 'assetdeclarations'

# Mongo Setup
client = MongoClient()
db = client[DB_NAME]
coll = db[DB_COLLECTION]

# Removing collection data will prevent data overwriting
coll.remove({})

# First remove the formatted files if exists else create formatted dir
if os.path.exists(FORMATTED_DATA_DIR):
    shutil.rmtree(FORMATTED_DATA_DIR)
else:
    os.makedirs(FORMATTED_DATA_DIR)

def process_data(df, y, muni):
    # Year dict
    year_d = {y: []}

    print "Processing " + muni + " - " + y

    # Loop through every row and process data
    for i, row in df.iterrows():
        name = row[0]
        surname = row[1]
        url = row[2]
        full_name = name + ' ' + surname
        municipality = muni

        # Slugify Dict
        sl_d = {}
        sl_d['name'] = slugify(name)
        sl_d['surname'] = slugify(surname)
        sl_d['full_name'] = slugify(full_name)
        sl_d['municipality'] = slugify(municipality)

        # Final Dict
        fd = {}
        fd['name'] = name
        fd['surname'] = surname
        fd['url'] = url
        fd['full_name'] = full_name
        fd['municipality'] = municipality
        fd['slugify'] = sl_d

        year_d[y].append(fd)

    return year_d

def save_in_json(muni, year, data):
    muni_formatted_dir = FORMATTED_DATA_DIR + muni
    year_muni_formatted_file = muni_formatted_dir + '/' + year + '.json'

    # Saving data into JSON files
    if not os.path.exists(muni_formatted_dir):
        os.makedirs(muni_formatted_dir)

    with open(year_muni_formatted_file, 'w') as outfile:
        json.dump(data, outfile)

# Processing and importing
for muni in os.listdir(RAW_DATA_DIR):
    if not muni.startswith('.'):
        for csv_file in os.listdir(RAW_DATA_DIR + muni):

            if not csv_file.startswith('.'):

                year = csv_file.split('.')[0]
                csv_file_dir = RAW_DATA_DIR + muni + '/' + csv_file
                
                # Read csv file with Pandas
                df = pd.read_csv(csv_file_dir, sep=',')

                # Processing Data
                data = process_data(df, year, muni)

                # Saving as JSON files
                save_in_json(muni, year, data)
                print "Saved as JSON " + muni + " - " + year

                # Importing into Database
                coll.insert(data)
                print "Imported into DB " + muni + " - " + year