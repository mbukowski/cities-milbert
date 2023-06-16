import csv
import common.etl as etl

from common.globals import Units, UnitsData


'''
Fill out the gaps for the missing data for specific files.
After cleanup is done copy data back to the main data / dict folder.
'''

'''
Reads a units csv file and add missing values for 'kind' parameter
'''
def complete_units():
    with open(UnitsData.DATA, mode='r') as input_csv:
        csv_reader = csv.DictReader(input_csv, delimiter=',')

        header = False
        with open(Units.DATA, mode='w') as output_csv:
            for row in csv_reader:
                if not header:
                    csv_writer = csv.DictWriter(output_csv, fieldnames=row)
                    csv_writer.writeheader()
                    header = True

                if not row['kind']:
                    row['kind'] = 0
                csv_writer.writerow(row)

'''
Simple check if we can read units.csv file back again
'''
def check_units():
    df = etl.extract(UnitsData.DATA, UnitsData.HEADER, UnitsData.TYPES)
    df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)

  
def main():
    # complete_units()
    check_units()
