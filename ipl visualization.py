# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 01:01:19 2023

@author: Puneet
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import plotly.graph_objects as go
import matplotlib.cm as cm
import seaborn as sns
import textwrap


# importing the dataset
df = pd.read_csv("matches.csv")
print(df.dtypes)

# data cleansing
df.loc[df['team1'] == "Rising Pune Supergiants", 'team1'] = "Rising Pune Supergiant"
df.loc[df['team2'] == "Rising Pune Supergiants", 'team2'] = "Rising Pune Supergiant"
df.loc[df['team1'] == "Pune Warriors", 'team1'] = "Rising Pune Supergiant"
df.loc[df['team2'] == "Pune Warriors", 'team2'] = "Rising Pune Supergiant"
df.loc[df['team1'] == "Deccan Chargers", 'team1'] = "Sunrisers Hyderabad"
df.loc[df['team2'] == "Deccan Chargers", 'team2'] = "Sunrisers Hyderabad"
df.loc[df['team1'] == "Delhi Daredevils", 'team1'] = "Delhi Capitals"
df.loc[df['team2'] == "Delhi Daredevils", 'team2'] = "Delhi Capitals"
df.loc[df['winner'] == "Rising Pune Supergiants", 'winner'] = "Rising Pune Supergiant"
df.loc[df['winner'] == "Pune Warriors", 'winner'] = "Rising Pune Supergiant"
df.loc[df['winner'] == "Deccan Chargers", 'winner'] = "Sunrisers Hyderabad"
df.loc[df['winner'] == "Delhi Daredevils", 'winner'] = "Delhi Capitals"



# Define the team colors
team_colors = {"Mumbai Indians": "#004ba0",
               "Royal Challengers Bangalore": "#fcb913",
               "Kings XI Punjab": "#e03a3e",
               "Sunrisers Hyderabad": "#ff822a",
               "Kolkata Knight Riders": "#522886",
               "Chennai Super Kings": "#fdb913",
               "Delhi Daredevils": "#e91d1d",
               "Rajasthan Royals": "#ef68a3",
               "Pune Warriors": "#87ceeb",
               "Kochi Tuskers Kerala": "#3d3d3d"}

# removing the rows == no result
df1 = df[df.result != "no result"]



# Create the figure and GridSpec layout
fig = plt.figure(figsize=(35, 15), dpi=300)
gs = fig.add_gridspec(nrows=4, ncols=3)


# Select matches with margin > 50 runs
ch = df1[df1['win_by_runs'] > 50]
wbr = ch['winner'].value_counts().sort_values(ascending=False).head(8)

# Select matches with margin > 5 wickets
ch1 = df1[df1['win_by_wickets'] > 5]
wbw = ch1['winner'].value_counts().sort_values(ascending=False).head(8)

# Plot the matches won with margin > 50 runs
ax1 = fig.add_subplot(gs[2, 1])
for team in wbr.index:
    ax1.bar(team, wbr[team], color=team_colors.get(team), alpha=0.8,)
ax1.set_title("Matches Won with Margin > 50 Runs", fontsize=16, fontweight="bold")
ax1.set_xlabel("Teams", fontsize=12)
ax1.set_ylabel("No of Matches", fontsize=12)
ax1.tick_params(axis='x', rotation=0, labelsize=10)
ax1.set_xticklabels([textwrap.fill(label, 10) for label in wbr.index], rotation=0, ha='right',fontweight='bold')
plt.yticks(fontweight='bold')
for i, v in enumerate(wbr.values):
    ax1.text(i, v+0.5, str(v), ha="center", fontsize=10)

gs.update(hspace=0.5)

# Plot the matches won with margin > 5 wickets
ax2 = fig.add_subplot(gs[3, 1])
for team in wbw.index:
    ax2.bar(team, wbw[team], color=team_colors.get(team), alpha=0.8,)
ax2.set_title("Matches Won with Margin > 5 Wickets", fontsize=16, fontweight="bold")
ax2.set_xlabel("Teams", fontsize=12)
ax2.set_ylabel("No of Matches", fontsize=12)
ax2.tick_params(axis='x', rotation=0, labelsize=10)
ax2.set_xticklabels([textwrap.fill(label, 10) for label in wbw.index], rotation=0, ha='right',fontweight='bold')
plt.yticks(fontweight='bold')
for i, v in enumerate(wbw.values):
    ax2.text(i, v+0.5, str(v), ha="center", fontsize=10)



# Calculate the number of matches played by each team
matches_played = df["team1"].value_counts() + df["team2"].value_counts()
matches_played = matches_played.sort_values(ascending=False)

# Calculate the number of matches won by each team
matches_won = df["winner"].value_counts()
matches_won = matches_won.reindex(matches_played.index)  # Sort by team name
ax3 = fig.add_subplot(gs[2, 0])
# Plot the number of matches played by each team
ax3.bar(matches_played.index, matches_played.values, color='green', alpha=0.5, label='Matches Played')

# Plot the number of matches won by each team
for team in matches_won.index:
    ax3.bar(team, matches_won[team], color=team_colors.get(team), alpha=0.8,)

# Set the axis labels and title
ax3.set_xlabel("Team")
ax3.set_ylabel("Number of Matches")
ax3.set_title("IPL Matches Played and Won by Teams")

# Add the legend
ax3.legend()

# Rotate the x-axis labels
ax3.set_xticklabels([textwrap.fill(label, 10) for label in matches_played.index], rotation=0, ha='right',fontweight='bold')
plt.yticks(fontweight='bold')



matches_won = df1.groupby(['Season', 'winner'])['winner'].count().reset_index(name='matches')

# Create the dot plot
ax4 = fig.add_subplot(gs[0, 1:])
for i, team in enumerate(matches_won['winner'].unique()):
    team_data = matches_won[matches_won['winner'] == team]
    ax4.scatter(team_data['Season'], team_data['matches'], s=100, alpha=0.5, label=team)
# Add labels and legend
ax4.set_xlabel('Year')
ax4.set_ylabel('Number of Matches Won')

plt.xticks(rotation=0, fontweight='bold')
plt.yticks(fontweight='bold')
ax4.set_title("No of maches own based on every IPL")
ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=9)

#top 10 player of the match
tpl = dict(df1['player_of_match'].value_counts().sort_values(ascending=True)[217:227])
ax5 = fig.add_subplot(gs[2, 2])
ax5.barh(list(tpl.keys()), list(tpl.values()), color=['#6b3d92', '#9e9ac8', '#bcbddc', '#dadaeb', '#efedf5', '#fbb4b9', '#f768a1', '#c51b8a', '#7a0177', '#49006a'])
ax5.set_xlabel("No of Times")
ax5.set_ylabel("Players")
plt.yticks(fontweight='bold')
plt.xticks(fontweight='bold')
ax5.set_title("TOP 10 PLAYER OF THE MATCH WINNERS")

for i, v in enumerate(tpl.values()):
    ax5.text(v + 0.5, i - 0.15, str(v), color='black', fontweight='bold')

#plt.show()

# Group data by season and count the number of matches
matches_per_season = df1.groupby('Season')['id'].count().reset_index(name='matches')

# Create a line plot of matches per season
sns.set_style('darkgrid')
sns.set_palette('muted')

ax6 = fig.add_subplot(gs[0, 0])
sns.lineplot(x='Season', y='matches', data=matches_per_season, marker='o', markersize=7, ax=ax6)
ax6.set_xlabel('Season')
ax6.set_ylabel('Number of Matches')
ax6.set_title('Matches Played in Each Year')
plt.yticks(fontweight='bold')
plt.xticks(fontweight='bold')

for index, row in matches_per_season.iterrows():
    ax6.text(row['Season'], row['matches']-1, row['matches'], ha='center', fontsize=10)

sub='The Indian Premier League (IPL) is a professional Twenty20 cricket league in India contested by ten teams based in ten Indian cities. The league was founded by the Board of Control for Cricket in India (BCCI) in 2008. The IPL is the most-popular cricket league in the world, and is ranked sixth by average attendance among all sports leagues. The IPL is played over a period of two months in April and May each year. Each team plays a total of 14 matches in the league stage, with the top four teams qualifying for the playoffs. The playoffs consist of two semifinals and a final.'
fig.suptitle('Indian Premier League(IPL)\n Puneet Ananth Hegde-21062529', fontweight='bold', fontsize=20, color='Black')
wrapped_text_sub = textwrap.fill(sub, width=300)
fig.text(0.45, 0.91, wrapped_text_sub , ha='center', fontsize=15)

plot1 = "The line chart presented above illustrates the correlation between the number of teams participating in the annual IPL cricket tournament and the corresponding number of matches played each year. The trend line on the chart displays a mix of upward and downward slopes, indicating that as the number of participating teams increases, the number of matches played tends to rise as well. For instance, in 2008, when there were nine teams, a total of 58 matches were played. However, during the period of 2011 to 2013, when the number of teams increased to 10-11, the number of matches played also rose to 72-76. Subsequently, from 2014 onwards, the number of teams decreased again to nine, leading to a reduction in the number of matches played to nearly 60."
wrapped_text = textwrap.fill(plot1, width=100)
fig.text(0.07, 0.54, wrapped_text, ha='left', fontsize=15)


plot2 = "The plots below showcase the performance of various teams in the Indian Premier League (IPL) based on their ability to win matches by a large margin and to chase down targets with a comfortable margin of wickets. The blowing performance of the teams is reflected in the charts, with Chennai Superkings leading the way, followed by Mumbai Indians and Royal Challengers Bangalore at the second and third spots, respectively. On the other hand, Kolkata Knight Riders, Kings XI Punjab, and Delhi Capitals have displayed remarkable batting performances, occupying the first, second, and third places, respectively.\n The analysis indicates that Chennai Super Kings, Mumbai Indians, and Royal Challengers Bangalore are the top-performing teams in terms of defending their scores, while Kolkata Knight Riders, Kings XI Punjab, and Delhi Capitals have excelled at chasing targets with a comfortable margin of wickets in hand. These findings suggest that these teams possess the necessary skills and abilities to succeed in the IPL and emerge as strong contenders for the title."
wrapped_text = textwrap.fill(plot2, width=100)
fig.text(0.37, 0.5, wrapped_text, ha='left', fontsize=15)


plot3 = "The graph presented above depicts the number of matches won by each team in the Indian Premier League (IPL) from 2008 to 2019. Mumbai Indians have emerged as the most successful team, having won the highest number of matches in five IPL seasons. Chennai Super Kings occupy the second spot, while Royal Challengers Bangalore claim the third position. \n These findings suggest that Mumbai Indians have consistently performed well in the IPL and have been the most dominant team across the years. Chennai Super Kings have also displayed a commendable performance, with a substantial number of match wins to their credit. Royal Challengers Bangalore, while not as successful as the other two teams, have still managed to secure a significant number of victories, highlighting their competitive spirit and potential to perform well in the tournament."
wrapped_text = textwrap.fill(plot3, width=100)
fig.text(0.67, 0.54, wrapped_text, ha='left', fontsize=15)


plot4 = "The above graph displays the number of matches played by each team in the Indian Premier League (IPL) from 2008 to 2019 and the corresponding number of matches won. The graph shows that most teams have played a similar number of matches, but there are some notable variations in the number of matches won. According to the graph, Mumbai Indians have the highest winning ratio, followed by Chennai Super Kings and Kolkata Knight Riders. These findings suggest that these three teams are the most successful in the IPL, and are more likely to win most of the IPL trophies. The data presented in the graph can help cricket enthusiasts to identify the most successful teams in the IPL and predict their future performance. It can also provide valuable insights for team management to develop strategies to improve their team's performance and increase their chances of winning the tournament."
wrapped_text = textwrap.fill(plot4, width=100)
fig.text(0.07, 0.12, wrapped_text, ha='left', fontsize=15)


plot5 ='The Man of the Match award in IPL is a prestigious recognition given to the player who has performed exceptionally well in a match, as assessed by a panel of experts. The award is conferred on players who have made noteworthy contributions in terms of scoring runs, taking wickets, or displaying outstanding fielding efforts. The objective of the award is to acknowledge and appreciate exceptional individual performances and motivate players to strive for excellence. The above graph provides valuable insights into the top-performing players in the IPL. As per the graph, the top three players who have received the Man of the Match award most frequently are Chris Gayle, AB de Villiers, and Rohit Sharma. These players have consistently demonstrated their exceptional skills and abilities on the field and have made significant contributions to their respective teams in the IPL. This information can be beneficial for IPL teams to identify and recruit the best players and build a competitive team. It can also inspire players to strive for excellence and aim to be recognized as the best performers in the tournament.'
wrapped_text = textwrap.fill(plot5, width=100)
fig.text(0.67, 0.12, wrapped_text, ha='left', fontsize=15)


plt.savefig('IPL.jpg')
plt.show()


'''
# Group data by team and count the number of wins
team_wins = df1.groupby(['winner']).size().reset_index(name='wins')

# Create a histogram for each team
fig = go.Figure()
for i, team in enumerate(team_wins['winner']):
    hist_data = df1[df1['winner'] == team]['Season'].sort_values()
    fig.add_trace(go.Histogram(x=hist_data, name=team, visible=False))
    fig.data[i].visible = True


# Create the dropdown menu for team selection
buttons = []
for i, team in enumerate(team_wins['winner']):
    visibility = [False] * len(team_wins['winner'])
    visibility[i] = True
    button = dict(label=team,
                  method='update',
                  args=[{'visible': visibility},
                        {'title': 'Histogram of ' + team + ' Wins of Every Year'}])
    buttons.append(button)

# Add dropdown menu to the figure layout
fig.update_layout(showlegend=False, updatemenus=[{'type': 'dropdown', 'active': 0, 'buttons': buttons}])

# Set the axis labels and title
fig.update_layout(xaxis_title='Season', yaxis_title='Number of Wins', title='Histogram of All Teams Wins of Every Year', template='none')

# Display the interactive histogram
fig.show(renderer='browser')
'''
















