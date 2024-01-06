import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def main():
    score()
    # density()
    # compactness()
    # correlation()
    # regression()

# boxplots for scores and city types
def score():
    # font = {'family': 'normal',
    #         'fontname': 'Calibri',
    #         'size': 22}

    # plt.rc('font', **font)

    header_types = {
        'unit_id': str,
        'teryt_id': str
    }

    df = pd.read_csv('./data/processed/stats/summary.csv', sep=',', decimal='.', dtype=header_types)
    df = df.loc[(df['type'].isin(['S', 'M', 'L']))]
    df = df.loc[(df['period_start'].isin([2006, 2011, 2016]))]
    df = df.groupby(['period_start', 'type', 'score', 'status']).size().reset_index(name='counts')

    df.loc[df["type"] == "L", "type"] = 'large'
    df.loc[df["type"] == "M", "type"] = 'medium'
    df.loc[df["type"] == "S", "type"] = 'small'


    types_colors={"large": "#f6b26b", "medium": "#6d9eeb", "small":"#c27ba0",  "R":"#c11be4"}

    # # Iterate over periods
    # for i, period in enumerate(df['period_start'].unique()):
    #     subset = df[df['period_start'] == period]
    #     sns.boxplot(data=subset[['type','score']].sort_values(by='type'), x='type', y='score', palette=types_colors)
    
    #     axes[i].set_title(f'{period}-{period + 5}', fontsize=20)
    #     axes[i].set_xlabel('City Size', fontsize=20)
    #     axes[i].set_ylabel('Score', fontsize=20)
    #     axes[i].tick_params(axis='both', which='major', labelsize=16)

    # # if save:
    # #     plt.savefig(path+str(period_start)+"-"+str(period_start+5)+'.png')

    # plt.show()



    # print(df.to_string())

    # Plotting
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Iterate over periods
    for i, period in enumerate(df['period_start'].unique()):
        subset = df[df['period_start'] == period]
        # sns.boxplot(data=subset, x='type', y='score', ax=axes[i], showfliers=True, flierprops=dict(markerfacecolor='r', marker='D'), palette=types_colors)
        sns.boxplot(data=subset, x='type', y='score', ax=axes[i], palette=types_colors)
        
        axes[i].set_title(f'{period}-{period + 5}', fontsize=18, fontname='Calibri')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('')

        # Set score ticks every 5 units
        axes[i].set_yticks(range(0, 25, 5))
    

        # Remove horizontal lines
        axes[i].xaxis.grid(False)
        axes[i].yaxis.grid(False)

        axes[i].tick_params(axis='both', which='major', labelsize=14)

        # Remove legend
        # axes[i].legend().set_visible(False)

        # plt.xlabel("X Label")
        # plt.ylabel("Y Label")


    # Set common labels and show the plot
    # fig.text(0.5, 0.01, 'City Size', ha='center', fontsize=24, fontname='Calibri')
    fig.text(0.06, 0.5, 'Score', va='center', rotation='vertical', fontsize=24, fontname='Calibri')

    # plt.tick_params(axis='both', which='major', labelsize=16)

    # plt.show()
    plt.savefig('C:\\Users\\mbukowski\Desktop\\fig_6_box_plots_scores_300.png', dpi=300)

    # # Convert period_start to categorical for correct ordering
    # df['period_start'] = pd.Categorical(df['period_start'], categories=[2006, 2011, 2016], ordered=True)

    # # Create subplots for each period
    # periods = df['period_start'].cat.categories
    # num_periods = len(periods)

    # fig, axes = plt.subplots(1, num_periods, figsize=(15, 5), sharey=True)
    # sns.set_theme(style="whitegrid")

    # for i, period in enumerate(periods):
    #     data_subset = df[df['period_start'] == period]
    #     agg_df = data_subset.groupby(['type', 'score'], as_index=False)['counts'].sum()

    #     # Create the box plot for the current period
    #     sns.boxplot(x='type', y='counts', hue='type', data=agg_df, width=0.8, showfliers=False, ax=axes[i])
    #     axes[i].set_title(f'Period {period}')
    #     axes[i].set_xlabel('Type')
    #     axes[i].set_ylabel('Counts')
    #     axes[i].legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    #     axes[i].get_legend().remove()

    #     # Add labels at the bottom
    #     axes[i].text(0.5, -0.2, 'large', ha='center', va='center', transform=axes[i].transAxes, fontdict={'fontname': 'Calibri'})
    #     axes[i].text(1.5, -0.2, 'medium', ha='center', va='center', transform=axes[i].transAxes, fontdict={'fontname': 'Calibri'})
    #     axes[i].text(2.5, -0.2, 'small', ha='center', va='center', transform=axes[i].transAxes, fontdict={'fontname': 'Calibri'})


    # plt.suptitle('Box Plots for Each Type in Each Period')
    # plt.tight_layout(rect=[0, 0, 1, 0.95])
    # plt.show()    

    # # Aggregate counts for each score within each type and period
    # agg_df = df.groupby(['period_start', 'type', 'score'], as_index=False)['counts'].sum()

    # # Create the side-by-side box plots
    # plt.figure(figsize=(15, 5))
    # sns.set_theme(style="whitegrid")

    # sns.boxplot(x='period_start', y='counts', hue='type', data=agg_df, width=0.8, showfliers=False)
    # plt.title('Box Plot for Each Type in Each Period')
    # plt.xlabel('Period Start')
    # plt.ylabel('Counts')
    # plt.legend(title='Type', bbox_to_anchor=(1.05, 1), loc='upper left')

    # plt.tight_layout()
    # plt.show()

    # # Create the side-by-side box plots
    # plt.figure(figsize=(15, 5))
    # sns.set_theme(style="whitegrid")

    # for i, period in enumerate(df['period_start'].unique()):
    #     plt.subplot(1, 3, i+1)
    #     subset = df[df['period_start'] == period]
    #     sns.boxplot(x='type', y='counts', hue='score', data=subset, width=0.8, showfliers=False)
    #     plt.title(f'Period {period}')
    #     plt.xlabel('Type')
    #     plt.ylabel('Counts')
    #     plt.legend(title='Score', bbox_to_anchor=(1.05, 1), loc='upper left')

    # plt.tight_layout()
    # plt.show()


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
        # print(model_fit.summary())


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