# Cities Milbert
Statistics for Milbert methodology to identify shrinking cities in Poland based on GUS data acquired from [Bank Danych Lokalnych](https://bdl.stat.gov.pl).

## Configuration
Before we start running scripts we need to provide statistic's data in data/bdl folder. Files need to have specific format as well as the name. Dictionary and configuration data are commited to the source code.

Files can be either in long or short format. For convenience we suggest to use a short version, where some columns were removed. For full reference and general view long version is recommended. Code is analysing a short version of the data. Data files should be located in data/bdl/ folder.

| file | header | 
| ---- | ------ |
| data_unit_population.csv | unitId,varId,year,val |


# TODO 
- add example file to bdl, 
- explain location folder, 
- explain files and what kind of data they carry
- some fixes from milbert docu
- rename main to milbert 
- add cires module and separate file 