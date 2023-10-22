import json
from collections import Counter

# Load the consolidated job listings data
with open('consolidated_jobs.json', 'r', encoding='utf-8') as f:
    job_data = json.load(f)

# Extract job titles, industries, qualifications/skills, and locations
job_titles = [job['title'] for job in job_data['jobs']]
industries = [job['company']['industry'] for job in job_data['jobs']]
locations = [f"{job['location']['city']['name']}, {job['location']['country']['name']}" for job in job_data['jobs']]

# Data Analysis
# a. Most common job titles
common_job_titles = Counter(job_titles).most_common(10)
most_common_job_titles = [{'title': title, 'count': count} for title, count in common_job_titles]

# b. Industries or sectors with the highest demand
common_industries = Counter(industries).most_common(10)
most_common_industries = [{'industry': industry, 'count': count} for industry, count in common_industries]

# d. Geographic Distribution of Job Opportunities
common_locations = Counter(locations).most_common(10)
geographic_distribution = [{'location': location, 'count': count} for location, count in common_locations]

# Save results to separate JSON files
with open('most_common_job_titles.json', 'w', encoding='utf-8') as f:
    json.dump({'most_common_job_titles': most_common_job_titles}, f, ensure_ascii=False, indent=4)

with open('most_common_industries.json', 'w', encoding='utf-8') as f:
    json.dump({'most_common_industries': most_common_industries}, f, ensure_ascii=False, indent=4)

with open('geographic_distribution.json', 'w', encoding='utf-8') as f:
    json.dump({'geographic_distribution': geographic_distribution}, f, ensure_ascii=False, indent=4)
