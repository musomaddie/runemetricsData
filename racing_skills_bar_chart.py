import pandas as pd
import bar_chart_race as bcr
from datetime import datetime

# Creating the racing bar chart for the skills
filename = "skills.csv"
df = pd.read_csv(filename)
df.at[0, "Date"] = datetime.min
for index, row in df.iterrows():
    if index == 0:
        continue
    now = datetime.now()
    date_str = f"{row['Date']} {now.year}"
    datetime_obj = datetime.strptime(date_str,
                                     "%d %B %Y")
    df.at[index, "Date"] = datetime_obj

print(df.shape)
bcr.bar_chart_race(
    df=df,
    sort='desc',
    title="Runescape XP in Skill Tracking",
    filename="skills_race.mp4")
