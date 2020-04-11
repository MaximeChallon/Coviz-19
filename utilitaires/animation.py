"""Create an animation of the best-fit logistic curve over time."""
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

plt.style.use('dark_background')
DOTS_COLOR = 'white'

# Uncomment this for dark style
# plt.style.use('seaborn-pastel')
# DOTS_COLOR = 'black'

matplotlib.rc('font', family='sans-serif')
matplotlib.rc('font', serif='Helvetica Neue')
matplotlib.rc('text', usetex='false')


def animation_plot(country,  to_plot='new_cases', save=True, output_folder='out', repeat=False):
    """Create the animation.

    Parameters
    ----------
    country: str
        Country to plot.
    region: str
        Region of the given contry, currently supported only for Italy ('all', NAME or mNAME for excluding NAME region)
    to_plot: str, default 'confirmed'
        'confirmed' for confirmed cases, or 'deaths' for confirmed deaths.
    save: bool, default False
        Whether to save the plot.
    output_folder: str, default 'out'
        Path where to save the plot.
    repeat: bool, default True
        Whether to loop the animation or stop at last frame
    """
    data_to_json()

    if country:
        target = country + ".json"
        url = 'utilitaires/data/data_json.json'

    data = get_json_from_url(url)

    if country:
        df = pd.DataFrame(data[country])

    min_cases = 5
    df = df[df[to_plot] > float(min_cases)]
    df = df.reset_index(drop=True)

    # Plot limits
    MAX_DAYS_AHEAD = 10
    y_max = df[to_plot].max() * 2
    x_max = MAX_DAYS_AHEAD + len(df)

    # X axis for future dates which are not in the data)
    x_future = [float(x) for x in list(np.linspace(0, x_max, num=x_max))]

    fig = plt.figure()
    ax = plt.axes(xlim=(0, len(x_future)), ylim=(0-(y_max*0.05), y_max))
    scatter = ax.scatter([], [], s=15, color=DOTS_COLOR)
    line, = ax.plot([], [], lw=2)
    date = ax.text(x_max - x_max*0.15, y_max + y_max*0.01, '')
    count = ax.text(x_max - x_max*0.23, y_max - y_max*0.05, '')
    plt.title(f"Logistic best fit over time, {to_plot} cases\nCountry: {country}")
    plt.xlabel(f"Days since {min_cases} {to_plot} cases")
    plt.ylabel(f"# {to_plot}")

    def plot_animation():
        MIN_POINTS = 5
        ROLLING_MEAN_WINDOW = 2
        def init():
            """Initialize the plot for the animation."""
            line.set_data([], [])
            scatter.set_offsets(np.empty(shape=(0, 2)))
            date.set_text('')
            count.set_text('')
            return [scatter, line, date, count],

        def fit_until_index(i):
            """Fit the logistic curve using data up until the current time <i>."""
            x = np.array([float(x) for x in range(len(df))])[:i+MIN_POINTS]
            cases = df[to_plot].iloc[:i+MIN_POINTS]

            # Apply smoothing via rolling average
            cases = cases.rolling(ROLLING_MEAN_WINDOW, min_periods=1, center=False).mean()

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
            return df['date'].values[i+MIN_POINTS-1]

        def get_count(i):
            """Get the current case counts."""
            return df[to_plot].values[i+MIN_POINTS-1]

        def get_scatter_values(i):
            """Get actual values to plot as scatter points."""
            x = np.array([float(x) for x in range(len(df))])[:i+MIN_POINTS]
            y = df[to_plot].iloc[:i + MIN_POINTS]
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
            count.set_text(f"# cases: {get_count(i)}")

            return [scatter, line, date, count],\

        fig.tight_layout()

        return animation.FuncAnimation(fig, animate,
                                       init_func=init,
                                       frames=len(df)+1-MIN_POINTS,
                                       interval=100,
                                       repeat=repeat, repeat_delay=1)
    anim = plot_animation()
    if save:
        os.mkdir(output_folder)
        path = output_folder + "/gif.gif"
        anim.save(path, writer='imagemagick', fps=1.5)
    plt.close()