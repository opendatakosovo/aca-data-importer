# Anti-Corruption Agency Data Importer
A python app for processing and importing Anti-Corruption Agency Data, specifically data of asset declarations of municipality politicians for years.

## Technologies used:
 * Server-side scripting: **Python 2.7**
 * Database: **MongoDB**
 * Data Analysis Library: **Pandas**
 * Data Formats: **CSV and JSON**

### Prerequisites
 * Python 2.7
 * Pip
 * Virtualenv

1. Getting the project in our local machine:
```
git clone https://github.com/opendatakosovo/aca-data-importer.git
cd aca-data-importer
```
2. Install all modules used in app:
```
bash installer.sh
```

**Note**: Your MongoDB local server must be running in order to import the data into database. Default database name is **anticorruption** and collection name is **assetdeclarations**. However you can change these names inside *run.py* file.

3. Run the importer app
```
bash run.sh
```

After processing and formatting, the data will be saved also into JSON files inside **formatted** directory inside data. 

Developed with love by **[Arianit Hetemi](https://github.com/arianithetemi)**