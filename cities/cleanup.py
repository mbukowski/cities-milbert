import cleanup.units_unify as unify
import cleanup.units_classify as classify
import cleanup.missing_data as missing_data


'''
Executes cleanup and data preparation scripts
- first unify units, find out which units have to be merged or replaced
- second we do some name modifications and we put them in separate folders divided by specific kind and level
'''

'''
TODO filter data from whole bdl based on variables and check in to github
'''

def main():
    # missing_data.main()
    # unify.main()
    classify.main()
    

if __name__ == '__main__':
    main()