
import matplotlib.pyplot as plt

DEFAULT_PLOT_WIDTH_INCHES = 6.5
DEFAULT_PLOT_HEIGHT_INCHES = 9.0

def _plot_df(df,
    plot_title='pandas.DataFrame',
    filename=None,
    width=DEFAULT_PLOT_WIDTH_INCHES,
    height=DEFAULT_PLOT_HEIGHT_INCHES,
    ):

    if filename is None:
        plt.switch_backend('TKAgg')
    else:
        plt.switch_backend('Agg')

    labels = list(df.columns.values)
    num_plots = df.shape[1] - 1   

    plt.figure(figsize=(width, height), clear=True)
 
    for i in range(num_plots):

        plt.subplot(num_plots, 1, i + 1)
        plt.plot(df.iloc[:, 0].values, df.iloc[:, i + 1].values,
            linestyle='solid', linewidth=1, color=(0.0, 0.0, 0.0))
        plt.grid(linestyle=':', linewidth=1, color=(0.75, 0.75, 0.75))
        plt.ylabel(labels[i + 1])

        if i == 0:
            plt.title(plot_title)
        if i == num_plots - 1:
            plt.xlabel(labels[0])
    
    plt.tight_layout()

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)

def _plot_df_dual(df, series,
    plot_title='pandas.DataFrame',
    filename=None,
    width=DEFAULT_PLOT_WIDTH_INCHES,
    height=DEFAULT_PLOT_HEIGHT_INCHES,
    ):

    if filename is None:
        plt.switch_backend('TKAgg')
    else:
        plt.switch_backend('Agg')

    labels = list(df.columns.values)
    num_plots = df.shape[1] - 1   

    plt.figure(figsize=(width, height), clear=True)
 
    for i in range(num_plots):

        plt.subplot(num_plots, 1, i + 1)
        plt.plot(df.iloc[:, 0].values, df.iloc[:, i + 1].values,
            linestyle='solid', linewidth=1, color=(0.0, 0.0, 0.0))
        if i == 0:
            plt.plot(df.iloc[:, 0].values, series.values,
                linestyle='--', linewidth=1, color=(1.0, 0.0, 0.0))
        plt.grid(linestyle=':', linewidth=1, color=(0.75, 0.75, 0.75))
        plt.ylabel(labels[i + 1])

        if i == 0:
            plt.title(plot_title)
        if i == num_plots - 1:
            plt.xlabel(labels[0])
    
    plt.tight_layout()

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
