import cleanup.units_unify as unify
import cleanup.units_classify as classify


'''
Executes cleanup and data preparation scripts
- first unify units, find out which units have to be merged or replaced
- second we do some name modifications and we put them in separate folders divided by specific kind and level
'''


def main():
    unify.main()
    classify.main()

    pass

if __name__ == '__main__':
    main()