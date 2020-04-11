import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation
from sklearn.preprocessing import MinMaxScaler
from utilitaires.fonctions import *
from utilitaires.constantes import *
import json
import matplotlib

matplotlib.use('TkAgg')
plt.style.use('ggplot')

matplotlib.rc('font', family='sans-serif')
matplotlib.rc('font', serif='Helvetica Neue')
matplotlib.rc('text', usetex='false')


def animation_plot(country, min_cases, max_days_ahead, min_points, rolling_mean_window, to_plot, output_folder, plt_title, plt_xlabel, plt_ylabel):
    """
    Create the animation plot in a GIF output for the given country and the given data.
    :param country: name of the country to process
    :type country: str
    :param min_cases: number minimum of cases or deaths to put in the plot
    :type min_cases: float
    :param max_days_ahead: number of days of prediction
    :type max_days_ahead: int
    :param min_points: minimum of points in the plot
    :type min_points: int
    :param rolling_mean_window: size of the window for the rolling average
    :type rolling_mean_window: int
    :param to_plot: name of the column of data to process
    :type to_plot: str
    :param output_folder: name of the outpu_folder
    :type output_folder: str
    :param plt_title: title of the plot
    :type plt_title: str
    :param plt_xlabel: title of the x ax
    :type plt_xlabel: str
    :param plt_ylabel: title of the y ax
    :type plt_ylabel: str
    :return: nothing
    :rtype: None
    """
    print("Begin to process animated plot...")

    data_to_json()

    print("Loading data...")
    # récupération des données
    url = 'utilitaires/data/data_json.json'
    data = get_json_from_url(url)
    df = pd.DataFrame(data[country])

    # sélection des données qui ont une valeur supérieure à min_cases
    df = df[df[to_plot] > float(min_cases)]
    df = df.reset_index(drop=True)

    print("Initialize plot...")
    # Plot limits
    y_max = df[to_plot].max() * 2
    x_max = max_days_ahead + len(df)

    # X axis for future dates which are not in the data
    x_future = [float(x) for x in list(np.linspace(0, x_max, num=x_max))]

    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(xlim=(0, len(x_future)), ylim=(0-(y_max*0.05), y_max))
    scatter = ax.scatter([], [], s=15, color="black", marker="D")
    line, = ax.plot([], [], lw=2, color="red")
    date = ax.text(x_max - x_max*0.15, y_max + y_max*0.01, '')
    count = ax.text(x_max - x_max*0.23, y_max - y_max*0.05, '')
    plt.title(plt_title)
    plt.xlabel(plt_xlabel)
    plt.ylabel(plt_ylabel)

    print("Fit the logistic curve...")
    def plot_animation():
        def init():
            """Initialize the plot for the animation."""
            line.set_data([], [])
            scatter.set_offsets(np.empty(shape=(0, 2)))
            date.set_text('')
            count.set_text('')
            return [scatter, line, date, count],

        def fit_until_index(i):
            """Fit the logistic curve using data up until the current time <i>."""
            x = np.array([float(x) for x in range(len(df))])[:i+min_points]
            cases = df[to_plot].iloc[:i+min_points]

            # Apply smoothing via rolling average
            cases = cases.rolling(rolling_mean_window, min_periods=1, center=False).mean()

            # Scale data for fitting
            m = MinMaxScaler()
            y = m.fit_transform(cases.values.reshape(-1, 1))
            y = y.reshape(1, -1)[0]

            # Fit the logistic, then apply the inverse scaling to get actual values
            # Reshaping is needed for scipy fitting
            y_pred = fit_predict(x, y, logistic, x_pred=x_future).reshape(-1, 1)

            return m.inverse_transform(y_pred).reshape(1, -1)[0]

        def get_date(i):
            """Get the current date."""
            return df['date'].values[i+min_points-1]

        def get_count(i):
            """Get the current case counts."""
            return df[to_plot].values[i+min_points-1]

        def get_scatter_values(i):
            """Get actual values to plot as scatter points."""
            x = np.array([float(x) for x in range(len(df))])[:i+min_points]
            y = df[to_plot].iloc[:i + min_points]
            return x, y

        def animate(i):
            """Update the animation."""
            # Update scatter of actual values
            x_s, y_s = get_scatter_values(i)
            scatter_values = np.column_stack((x_s, y_s))
            scatter.set_offsets(scatter_values)

            # Update best fit line
            y = fit_until_index(i)
            line.set_data(x_future, y)
            line.label = i

            # Update texts
            date.set_text(get_date(i))
            count.set_text(f"{to_plot}: {get_count(i)}")

            return [scatter, line, date, count],\

        fig.tight_layout()

        print("Create the GIF plot...")
        return animation.FuncAnimation(fig, animate,
                                       init_func=init,
                                       frames=len(df)+1-min_points,
                                       interval=100)
    anim = plot_animation()
    os.mkdir(output_folder)
    path = output_folder + "/gif.gif"
    anim.save(path, writer='imagemagick', fps=1.5)
    plt.close()