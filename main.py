import requests
import json
from bs4 import BeautifulSoup
from notification import sendNotification

url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/README.md"

response = requests.get(url)
data = response.text

soup = BeautifulSoup(data, "html.parser")
rows = soup.find_all("tr")

wantedTerms = [
    "software",
    "developer",
    "computer vision",
    "machine learning",
    "artificial intelligence",
    "ai intern",
    "front end",
    "frontend",
    "back end",
    "backend",
    "full stack",
    "fullstack"
]

excludedTerms = [
    "phd",
    "ph.d",
    "ms/phd",
    "masters",
    "master's",
    "mba",
    "graduate"
]

usStates = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
]

with open("jobList.json", "r") as file:
    seenJobs = json.load(file)

jobs = []
previousCompany = ""

for row in rows:
    cells = row.find_all("td")

    if len(cells) >= 5:
        company = cells[0].text.strip()
        role = cells[1].text.strip()
        location = cells[2].text.strip()

        application = cells[3].find("a")
        applicationURL = application["href"].strip() if application else ""

        age = cells[4].text.strip()

        if company == "↳":
            company = previousCompany
        else:
            previousCompany = company

        job = {
            "company": company,
            "role": role,
            "location": location,
            "applicationURL": applicationURL,
            "age": age
        }

        jobs.append(job)

filteredJobs = []

for job in jobs:
    role = job["role"].lower()
    location = job["location"]

    wanted = any(term in role for term in wantedTerms)
    excluded = any(term in role for term in excludedTerms)

    usBased = (
        "United States" in location
        or "USA" in location
        or "Remote" in location
        or any(f", {state}" in location for state in usStates)
    )

    if wanted and not excluded and usBased:
        filteredJobs.append(job)

newJobs = []

for job in filteredJobs:
    if job["applicationURL"] not in seenJobs:
        newJobs.append(job)

currentURLs = []

for job in filteredJobs:
    currentURLs.append(job["applicationURL"])

with open("jobList.json", "w") as file:
    json.dump(currentURLs, file, indent=4)

print("Jobs parsed:", len(jobs))
print("Filtered jobs:", len(filteredJobs))
print("New jobs:", len(newJobs))
print("URLs saved:", len(currentURLs))

for job in newJobs:
    print("\nNEW INTERNSHIP")
    print("Company:", job["company"])
    print("Role:", job["role"])
    print("Location:", job["location"])
    print("Age:", job["age"])
    print("Apply:", job["applicationURL"])


for job in newJobs:
    sendNotification(job)