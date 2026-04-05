import pandas as pd
import os
import matplotlib.pyplot as plt
import textwrap

#Load CSV into dataframe
filename = "data/trends_analysed.csv"
df = pd.read_csv(filename)

#create a outputs directory if it doesn't exist
os.makedirs("outputs", exist_ok= True)

#Chart 1 - Top 10 Stories by Score 
#Sorting the dataframe to show the top 10 stories in descending order by score
sorted_df = df.sort_values(by = 'score', ascending= False)
#head(10) gives the first 10 stories from the sorted dataframe
data = sorted_df.head(10)
title_list = []
titles = data["title"]
score = data["score"]
#Iterate over sortened dataframe to shorten the title if it has more then 50 characters and append it to the list using textwrap
for index, row in data.iterrows():
    shortened_title = textwrap.shorten(str(row["title"]),width=47,placeholder="...")
    title_list.append(shortened_title)
#create horizontal bar chart y - titles, x - score
plt.barh(title_list, score, color = "steelblue")
plt.title("Chart 1 - Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Title")
#save the chart as PNG file in outputs folder
plt.savefig("outputs/chart1_top_stories.png")
plt.show()
#close the chart figure
plt.close()

#Chart 2: Stories per Category
category_counts = df["category"].value_counts()
#list of colors for the chart
colors = ['steelblue', 'coral', 'mediumseagreen', 'goldenrod']
#Get the category names and count of categories, index to get the category names and values for count of stories in the category
categories = category_counts.index
count = category_counts.values
#create a bar chart, x - categories, y - count of stories 
plt.bar(categories, count, color=colors)
plt.title("Chart 2: Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
#save the chart as PNG file in outputs folder
plt.savefig("outputs/chart2_categories.png")
plt.show()
plt.close()

#Chart 3: Score vs Comments
scores = df["score"]
comments = df["num_comments"]
is_popular = df["is_popular"]
#Split rows into popular and non-popular
popular = df["is_popular"] == True
not_popular = df["is_popular"] == False
#Plot using scatter plot by locating popular and non-popular stories using boolean masks that is defined in previous lines
plt.scatter(df.loc[popular,"score"],df.loc[popular,"num_comments"],color = "green",label = "Popular",alpha=0.7)
plt.scatter(df.loc[not_popular,"score"],df.loc[not_popular,"num_comments"],color = "green",label = "Not Popular",alpha=0.7)
#create scatter plot x - Score of popular posts, y - no. of comments in popular post
plt.title("Chart 3: Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
#save the chart as PNG file in outputs folder
plt.savefig("outputs/chart3_scatter.png")
plt.show()
plt.close()

#Dashboard
#create 1x3 (1 row, 3 columns) subplot layout
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
#Draw chart 1 on first axes
ax1 = ax[0]
ax1.barh(title_list, score, color = "steelblue")
ax1.set_title("Chart 1 - Top 10 Stories by Score")
ax1.set_xlabel("Score")
ax1.set_ylabel("Title")
#Draw chart 2 on second axes
ax2 = ax[1]
ax2.bar(categories, count, color=colors)
ax2.set_title("Chart 2: Stories per Category")
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")
#Draw chart 3 on third axes
ax3 = ax[2]
ax3.scatter(df.loc[popular,"score"],df.loc[popular,"num_comments"],color = "green",label = "Popular",alpha=0.7)
ax3.scatter(df.loc[not_popular,"score"],df.loc[not_popular,"num_comments"],color = "green",label = "Not Popular",alpha=0.7)
ax3.set_title("Chart 3: Score vs Comments")
ax3.set_xlabel("Score")
ax3.set_ylabel("Number of Comments")
#Set Dashboard title and save it as PNG file
fig.suptitle("TrendPulse Dashboard", fontsize=16)
plt.savefig("outputs/dashboard.png")
plt.show()
plt.close()
