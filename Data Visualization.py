import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Load the job_scores.json file
with open('job_scores.json', 'r', encoding='utf-8') as scores_file:
    job_scores_data = json.load(scores_file)

# Convert job scores data to a DataFrame
df_job_scores = pd.DataFrame(job_scores_data['job_scores'])

# a. Bar Charts Showing the Most In-Demand Job Titles:
job_title_counts = df_job_scores['title'].value_counts()
plt.figure(figsize=(10, 6))
job_title_counts.head(10).plot(kind='bar')
plt.title('Top 10 Most In-Demand Job Titles')
plt.xlabel('Job Title')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# b. Word Clouds Highlighting Frequently Mentioned Qualifications and Skills:
qualifications_and_skills = ' '.join(df_job_scores['title'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(qualifications_and_skills)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Qualifications and Skills')
plt.axis('off')
plt.show()

# c. Geographic Heat Map (Additional data and libraries needed)
# To create a geographic heat map, you'll need to use libraries like Folium or Plotly
# and have additional geographic data for job locations.

# d. Scatterplot or Bar Chart Displaying Job Suitability Scores for the User's CV:
plt.figure(figsize=(10, 6))
plt.scatter(range(len(df_job_scores)), df_job_scores['score'], alpha=0.5)
plt.title('Job Suitability Scores for User\'s CV')
plt.xlabel('Job Listing Index')
plt.ylabel('Suitability Score')
plt.tight_layout()
plt.show()
