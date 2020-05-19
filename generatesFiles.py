import random

import json

def genereteJobsSkillsMatrix(num_jobs, num_skills):
    jobs = {}
    for i in range(1, num_jobs+1):
        job_key = "J"+str(i)
        skills = []
        for j in range(num_skills):
            skills.append(random.randint(0, 1))
        jobs[job_key] = skills
    return jobs

def generetePeopleSkillsMatrix(num_people, num_skills):
    skills = {}
    for i in range(1, num_people+1):
        people_key = "P"+str(i)
        skillsPerPeople = []
        for j in range(num_skills):
            skillsPerPeople.append(random.randint(0, 9))
        skills[people_key] = skillsPerPeople
    return skills


def generetePeoplePreferenceMatrix(num_people, num_jobs):
    preferences = {}
    for i in range(1, num_people+1):
        people_key = "P"+str(i)
        jobs = []
        for j in range(num_jobs):
            jobs.append(random.randint(0, 9))
        preferences[people_key] = jobs
    return preferences

if __name__ == "__main__":
    num_people = 100
    num_jobs = 5
    num_skills = 10

    jobs = genereteJobsSkillsMatrix(num_jobs, num_skills)
    skills = generetePeopleSkillsMatrix(num_people, num_skills)
    preferences = generetePeoplePreferenceMatrix(num_people, num_jobs)

    print(jobs)
    print(skills)
    print(preferences)

    with open('jobsSkills.txt', 'w') as file:
        file.write(json.dumps(jobs))
    with open('peopleSkills.txt', 'w') as file:
        file.write(json.dumps(skills))
    with open('peoplePreference.txt', 'w') as file:
        file.write(json.dumps(preferences))