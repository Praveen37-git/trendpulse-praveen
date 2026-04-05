import pandas as pd

#Load the JSON file into Pandas dataframe
filename = "data/trends_20260402.json"
df = pd.read_json(filename)

#print the number of rows loaded shape[0] returns the number of rows
print(f"Loaded {df.shape[0]} stories from {filename}")

#remove duplicates and missing values
#keeps the first occurence of unique post_id and remove other duplicates
df = df.drop_duplicates(subset=['post_id'])
#drop the rows where any of these columns contain null value
df_cleaned = df.dropna(subset=['post_id','title','score'])

#print number of rows after removing duplicates and null values len(df) gives the number of rows, we can use df.shape[0] as well
print("After removing duplicates: ",len(df))
print("After removing nulls: ",len(df_cleaned))

#to find the data types of all the fields, checking score and num_comments are integers
print(df.dtypes)

#remove stories where score < 5
df_cleaned = df_cleaned[(df_cleaned["score"] >= 5)]
print("After removing low scores: ",len(df_cleaned))

#strip extra spaces from title column by converting it to string and using inbuilt strip method
df_cleaned["title"] = df_cleaned["title"].str.strip()
print("Number of rows after cleaning: ",len(df_cleaned))

#saving to CSV file
df_cleaned.to_csv("data/trends_clean.csv",index=False)

#print summary of categories
print("Stories per category: ")
print(df_cleaned["category"].value_counts())
