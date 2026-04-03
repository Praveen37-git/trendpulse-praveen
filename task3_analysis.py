import pandas as pd
import numpy as np

#Load the CSV files into Panda dataframe
filename = "data/trends_clean.csv"
df = pd.read_csv(filename)

#print shape of dataframe (rows and columns)
print("Loaded data: ",df.shape)

#print first 5 rows
print("First 5 rows: \n",df.head())

#print average score and average num_comments
print("Average Score: ",df["score"].mean())
print("Average comments: ",df["num_comments"].mean())

#Calculating mean, median and standard deviation
scores = df["score"].values
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
#Calulating highest and lowest score
max_score = np.max(scores)
min_score = np.min(scores)
#printing all the results
print("---- NumPy Stats ----")
print("Mean of Scores: ", mean_score)
print("Median of Scores: ", median_score)
print("Standard deviation of Scores: ", std_score)
print("Highest score: ",max_score)
print("Lowest score: ",min_score)

#Finding the category with most stories
category = df["category"].value_counts()
#Find the index with most stories
max_category_name_idx = category.idxmax()
max_story_category = np.max(category)
print(f"Most stories in : {max_category_name_idx} ({max_story_category})")

#Find story with most comments
#Find the index with max comments
max_comments_idx = df["num_comments"].idxmax()
#print the story title with most comments
print(f"Most commented story : {df.loc[max_comments_idx,'title']} - {df.loc[max_comments_idx,'num_comments']}")

#Add new columns
df["engagement"] = df["num_comments"]/(df["score"] + 1)
df["is_popular"] = df["score"] > mean_score

#Save the updated Dataframe
filename = "data/trends_analysed.csv"
df.to_csv(filename,index=False)
print(f"Saved to {filename}")
