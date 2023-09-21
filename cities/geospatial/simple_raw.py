import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


def main():

    # # Create a Pandas.Series object with random data
    # data = pd.Series(np.random.randn(1000))

    # # Create a histogram plot of the data
    # data.hist()

    # # Save the plot to a file
    # plt.savefig('./data/qgis/histogram.png')


    df = pd.read_csv('./data/qgis/areas.csv', sep=',', header=0, dtype={'fid': int, 'teryt_id': str, 'area': float})

    total_df = df.groupby('teryt_id')['area'].sum()

    df['total'] = df['area'].groupby(df['teryt_id']).transform('sum')
    df['perc'] = df['area'] / df['total']

    # Define the bins and labels
    bins = [i/100 for i in range(0, 101)]  # Bins from 0.00 to 1.00 with a step of 0.01
    labels = [f'{i:.2f}-{i+0.01:.2f}' for i in bins[:-1]]  # Labels for each bin

    # Cut the 'perc' column into bins and count the items in each bin
    bin_counts = pd.cut(df['perc'], bins=bins, labels=labels, include_lowest=True).value_counts().sort_index()

    print(type(bin_counts))
    print(bin_counts)
    bin_counts.to_csv('./data/qgis/bin_counts.csv', float_format='%.4f', index=False)

    bin_counts.plot.bar()
    plt.axis('off')
    plt.show()
    plt.close()

    # df.hist(by='count', bins=100)
    # plt.savefig('./data/qgis/histogram.png')
    # plt.show()

    # # df.hist(column='perc', bins=50)
    # df.hist(by='perc', bins=100)
    # plt.savefig('./data/qgis/histogram.png')
    # plt.show()
    


    # df.plot.hist()
    # plt.show()

    # df.to_csv('./data/qgis/areas_val.csv', float_format='%.4f', index=False)

    # N_points = 100000
    # n_bins = 50

    # # Generate two normal distributions
    # dist1 = rng.standard_normal(N_points)
    # dist2 = 0.4 * rng.standard_normal(N_points) + 5

    # fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    # # We can set the number of bins with the *bins* keyword argument.
    # axs[0].hist(dist1, bins=n_bins)
    # axs[1].hist(dist2, bins=n_bins)

    # df = pd.DataFrame({
    #     'Maths': [80.4, 50.6, 70.4, 50.2, 80.9],
    #     'Physics': [70.4, 50.4, 60.4, 90.1, 90.1],
    #     'Chemistry': [40, 60.5, 70.8, 90.88, 40],
    #     'Students': ['Student1', 'Student1', 'Student1', 'Student2', 'Student2']
    # })
    # df.hist()



if __name__ == '__main__':
    main()