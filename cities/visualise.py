import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def main():
    # density()
    # compactness()
    # correlation()
    regression()

def density():
    header_types = {
        'unit_id': str,
        'teryt_id': str
    }

    df = pd.read_csv('./data/processed/analyse/analyse.csv', sep=',', decimal='.', dtype=header_types)
    df = df.loc[(df['type'] == 'M')]
    df = df.loc[(df['period_start'].isin([2006, 2011, 2016]))]
    df = df.loc[(df['group'] == 'artificial_surfaces')]    

    fig, axs = plt.subplots(figsize=(8, 6))
    # axs[0, 0].boxplot(df)


    boxprops = dict(linestyle='-', linewidth=1, color='#0d88e6')
    medianprops = dict(linestyle='-', linewidth=2, color='#6ab187')
    whiskerprops = dict(linestyle='-', linewidth=1, color='#fd7f6f')
    capprops = dict(linestyle='-', linewidth=2, color='#fd7f6f')
    
    ax, bplot = df.boxplot(column=['density'], by='year', ax=axs, 
                        boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops,
                        showfliers=False, showmeans=False, return_type='both')['density']
    
    # for k in bplot:
    #     print(f'{k} -> {bplot[k]}')
    
    print('medians')
    medians = [median.get_ydata()[0] for median in bplot['medians']]
    print(medians)

    print('means')
    means = [median.get_ydata()[0] for median in bplot["means"]]
    print(means)

    print('caps')
    caps = [median.get_ydata()[0] for median in bplot['caps']]
    print(caps)

    print('whiskers')
    whiskers = [median.get_ydata()[0] for median in bplot['whiskers']]
    print(whiskers)    

    # plt.boxplot(df)
    plt.suptitle('Density by Year', fontsize=14)
    plt.title('people / km2', fontsize=10)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Density', fontsize=12)

    ax = plt.gca()
    ax.grid(which='major', axis='both', linestyle='--', color = 'grey', linewidth = 0.5)

    plt.gca().xaxis.grid(False)
    # plt.gca().yaxis.grid(False)

    plt.show()


def compactness():
    header_types = {
        'unit_id': str,
        'teryt_id': str
    }

    df = pd.read_csv('./data/processed/analyse/analyse.csv', sep=',', decimal='.', dtype=header_types)
    df = df.loc[(df['type'] == 'M')]
    df = df.loc[(df['period_start'].isin([2006, 2011, 2016]))]
    df = df.loc[(df['group'] == 'artificial_surfaces')]

    fig, axs = plt.subplots(figsize=(8, 6))

    boxprops = dict(linestyle='-', linewidth=1, color='#445055')
    medianprops = dict(linestyle='-', linewidth=2, color='#6ab187')
    whiskerprops = dict(linestyle='-', linewidth=1, color='#fd7f6f')
    capprops = dict(linestyle='-', linewidth=2, color='#fd7f6f')
    
    ax, bplot = df.boxplot(column=['convex_hull'], by='year', ax=axs, 
                        boxprops=boxprops, medianprops=medianprops, whiskerprops=whiskerprops, capprops=capprops,
                        showfliers=True, showmeans=True, return_type='both')['convex_hull']
    
    # schwartzberg,polsby_popper,reock,box,rectangle,convex_hull
    
    print('medians')
    medians = [median.get_ydata()[0] for median in bplot['medians']]
    print(medians)

    print('means')
    means = [median.get_ydata()[0] for median in bplot["means"]]
    print(means)

    print('caps')
    caps = [median.get_ydata()[0] for median in bplot['caps']]
    print(caps)

    print('whiskers')
    whiskers = [median.get_ydata()[0] for median in bplot['whiskers']]
    print(whiskers)    

    # plt.boxplot(df)
    plt.suptitle('Compactness by Year', fontsize=14)
    plt.title('Convex Hull', fontsize=10)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Compactness', fontsize=12)

    ax = plt.gca()
    ax.grid(which='major', axis='both', linestyle='--', color = 'grey', linewidth = 0.5)

    plt.gca().xaxis.grid(False)
    # plt.gca().yaxis.grid(False)

    plt.show()

# not visualise but still here 
def correlation():
    header_types = {
        'unit_id': str,
        'teryt_id': str
    }

    df = pd.read_csv('./data/processed/analyse/analyse.csv', sep=',', decimal='.', dtype=header_types)
    df = df.loc[(df['type'] == 'M')]
    df = df.loc[(df['period_start'].isin([2006, 2011, 2016]))]
    df = df.loc[(df['group'] == 'artificial_surfaces')]

    for year in [2006, 2012, 2018]:
        df1 = df.loc[(df['year'] == year)]

        print(year)
        corr=df1['score'].corr(df1['density'])
        print(f'score-density: {corr}')

        corr=df1['score'].corr(df1['schwartzberg'])
        print(f'score-schwartzberg: {corr}')

        corr=df1['score'].corr(df1['polsby_popper'])
        print(f'score-polsby_popper: {corr}')

        corr=df1['score'].corr(df1['reock'])
        print(f'score-reock: {corr}')

        corr=df1['score'].corr(df1['box'])
        print(f'score-box: {corr}')

        corr=df1['score'].corr(df1['rectangle'])
        print(f'score-rectangle: {corr}')

        corr=df1['score'].corr(df1['convex_hull'])
        print(f'score-convex_hull: {corr}')

        print()



def regression():
    header_types = {
        'unit_id': str,
        'teryt_id': str
    }

    df = pd.read_csv('./data/processed/analyse/analyse.csv', sep=',', decimal='.', dtype=header_types)
    df = df.loc[(df['type'] == 'M')]
    df = df.loc[(df['period_start'].isin([2006, 2011, 2016]))]
    df = df.loc[(df['group'] == 'artificial_surfaces')]

    for year in [2006, 2012, 2018]:
        df1 = df.loc[(df['year'] == year)]

        # print(df1.describe())

        # Data distribution
        # plt.title('Density Distribution Plot')
        # sns.distplot(df1['density'])

        # Relationship between Density and Score
        # plt.scatter(df1['density'], df1['score'], color = 'lightcoral')
        # plt.title('Density vs Score')
        # plt.xlabel('Density')
        # plt.ylabel('Score')
        # plt.box(False)
        # plt.show()

        # Splitting variables
        # X = df1.loc[df1['density']]  # independent
        # y = df1.loc[df1['score']]  # dependent

        # Splitting variables
        # X = df1.iloc[:, 14]  # independent / 
        # y = df1.iloc[:, 7]  # dependent / score

        selected_features = ['convex_hull']
        X = df1[selected_features] # independent
        y = df1['score'] # dependent / score

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a linear regression model
        model = LinearRegression()

        # Train the model on the training set
        model.fit(X_train, y_train)

        # Make predictions on the testing set
        y_pred_test = model.predict(X_test) # predicted value of y_test
        y_pred_train = model.predict(X_train) # predicted value of y_train

        # Evaluate the model
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_test))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_test))
        print('Root Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_test, squared=False))


        # # Visualize the results (optional)
        # plt.scatter(X_test['density'], y_test, color='black', label='Actual')
        # plt.scatter(X_test['density'], y_pred, color='blue', label='Predicted')
        # plt.xlabel('Density')
        # plt.ylabel('Score')
        # plt.legend()
        # plt.show()

        # # Prediction on training set
        # plt.scatter(X_train, y_train, color = 'lightcoral')
        # plt.plot(X_train, y_pred_train, color = 'firebrick')
        # plt.title('Salary vs Experience (Training Set)')
        # plt.xlabel('Years of Experience')
        # plt.ylabel('Salary')
        # plt.legend(['X_train/Pred(y_test)', 'X_train/y_train'], title = 'Sal/Exp', loc='best', facecolor='white')
        # plt.box(False)
        # plt.show()


        # Prediction on test set
        plt.scatter(X_test, y_test, color = 'lightcoral')
        plt.plot(X_train, y_pred_train, color = 'firebrick')
        plt.suptitle('Compactness vs Score', fontsize=14)
        plt.title(year, fontsize=10)
        plt.xlabel('Compactness', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        # plt.legend(['X_train/Pred(y_test)', 'X_train/y_train'], title = 'Sal/Exp', loc='best', facecolor='white')
        # plt.box(False)
        plt.show()

        # Regressor coefficients and intercept
        print(f'Coefficient: {model.coef_}')
        print(f'Intercept: {model.intercept_}')

        # plt.show()

if __name__ == '__main__':
    main()