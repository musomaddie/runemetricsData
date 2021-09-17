from bokeh.io import show
from bokeh.plotting import figure

import pandas as pd


def make_chart(data):
    date = data["Date"]
    data = data.drop("Date").drop("Invention").sort_values(ascending=True)

    skills = [axe for axe in data.axes[0]]
    values = data.values.tolist()

    fig = figure(y_range=skills,
                 title=date,
                 toolbar_location=None,
                 tools="")
    fig.hbar(y=skills, right=values, height=0.9)
    fig.x_range.start = 0

    show(fig)


if __name__ == "__main__":
    df = pd.read_csv("skills.csv")
    make_chart(df.iloc[0])
