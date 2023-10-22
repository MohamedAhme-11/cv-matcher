import requests
import json

def get_json_safe(response):
    """Attempt to decode JSON response and return None on failure."""
    try:
        return response.json()
    except:
        print(f"Error decoding JSON. Status Code: {response.status_code}\n{response.text}")
        return None

def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

job = "Data Analyst"
wuzzuf_search_api = 'https://wuzzuf.net/api/search/job'
headers = {'content-type': 'application/json;charset=UTF-8'}
data = {
    "startIndex":0,
    "pageSize":10000,
    "longitude":"0",
    "latitude":"0",
    "query":job,
    "searchFilters":{}
}
data = json.dumps(data)

job_search_json = get_json_safe(requests.post(wuzzuf_search_api, headers=headers, data=data))
if not job_search_json:
    exit("Error fetching job search results.")

# Extract job ids and split them into smaller chunks
job_ids = [job['id'] for job in job_search_json['data']]
job_details_all = []

for job_id_chunk in chunk_list(job_ids, 50):  # Adjust chunk size as necessary
    wuzzuf_job_api = 'https://wuzzuf.net/api/job?filter[other][ids]=' + ','.join(job_id_chunk)
    job_details_json_chunk = get_json_safe(requests.get(wuzzuf_job_api))

    if job_details_json_chunk:
        job_details_all.extend(job_details_json_chunk['data'])

# Extract company ids, remove duplicates, and split them into chunks
company_ids = list({company['relationships']['company']['data']['id'] for company in job_details_all if company['relationships']['company']['data']})
company_details_all = []

for company_id_chunk in chunk_list(company_ids, 50):  # Adjust chunk size as necessary
    wuzzuf_company_api = 'https://wuzzuf.net/api/company?filter[id]=' + ','.join(company_id_chunk)
    company_details_json_chunk = get_json_safe(requests.get(wuzzuf_company_api))

    if company_details_json_chunk:
        company_details_all.extend(company_details_json_chunk['data'])

# Consolidating and Structuring Data

company_dict = {company['id']: company for company in company_details_all}

structured_jobs = []

for job in job_details_all:
    company_relation = job['relationships'].get('company')
    
    if not company_relation or not company_relation.get('data'):
        # Skip the current iteration if company relationship or its data is missing
        continue
    
    company_id = company_relation['data']['id']
    current_company = company_dict.get(company_id)
    
    # If the company is not in our company_dict, skip this iteration
    if not current_company:
        continue

    job_data = {
        "job_id": job['id'],
        "title": job['attributes']['title'],
        "description": job['attributes']['description'],
        "experience_needed": job['attributes'].get('experienceNeeded', ""), 
        "location": job['attributes']['location'],
        "company": {
            "company_id": company_id,
            "name": current_company['attributes']['name'],
            "industry": current_company['attributes'].get('industry', "Unknown"),
            "description": current_company['attributes'].get('description', "Unknown"),
            "location": current_company['attributes'].get('location', "Unknown")
        }
    }
    structured_jobs.append(job_data)


# Save the structured data
with open('consolidated_jobs.json', 'w', encoding='utf-8') as f:
    json.dump({'jobs': structured_jobs}, f, ensure_ascii=False, indent=4)
