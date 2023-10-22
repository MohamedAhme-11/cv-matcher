import json
from PyPDF2 import PdfReader  # Import PdfReader from PyPDF2

# Load job listings data from consolidated_jobs.json
with open('consolidated_jobs.json', 'r', encoding='utf-8') as jobs_file:
    job_listings = json.load(jobs_file)['jobs']

# Function to calculate the suitability score for a job listing based on CV keywords
def calculate_suitability_score(job, cv_keywords):
    job_description = job['description'].lower()
    score = sum(keyword in job_description for keyword in cv_keywords)
    return score

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    pdf_reader = PdfReader(pdf_file_path)  # Use PdfReader to open the PDF
    cv_text = ''
    for page in pdf_reader.pages:
        cv_text += page.extract_text()
    return cv_text.lower()

# Path to the user's CV PDF file
cv_pdf_path = r'D:\movie\MOHAMED_ABDELMONIEM_Resume_27-08-2023-06-32-18.pdf'

# Extract text from the user's CV
user_cv_text = extract_text_from_pdf(cv_pdf_path)

# Tokenize the CV text into keywords
cv_keywords = set(user_cv_text.split())

# Calculate suitability scores for each job listing
job_scores = []
for job in job_listings:
    score = calculate_suitability_score(job, cv_keywords)
    job_scores.append({'job_id': job['job_id'], 'title': job['title'], 'score': score})

# Sort job listings by suitability score in descending order
job_scores.sort(key=lambda x: x['score'], reverse=True)

# Display the top matching job listings and their scores
print("Top Matching Job Listings:")
for idx, job in enumerate(job_scores[:10], start=1):
    print(f"{idx}. Job Title: {job['title']}, Suitability Score: {job['score']}")

# Save the full list of job scores to a file
with open('job_scores.json', 'w', encoding='utf-8') as scores_file:
    json.dump({'job_scores': job_scores}, scores_file, ensure_ascii=False, indent=4)

print("Job scores saved to job_scores.json.")
