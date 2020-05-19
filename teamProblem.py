from __future__ import print_function
import random
import json

from simanneal import Annealer


class AssembleTeamProblem(Annealer):

    """Test annealer with a assemble a team problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, jobs, skills, preferences, people, alfa, beta):
        self.jobs = jobs
        self.skills = skills
        self.preferences = preferences
        self.people = people
        self.alfa = alfa
        self.beta = beta
        super(AssembleTeamProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps a member."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.people) - 1)
        b = random.randint(0, len(self.state) - 1)
        while self.people[a] in self.state:
            a = random.randint(0, len(self.people) - 1)
        self.state[b] = self.people[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates objective function."""
        e = 0
        for job, skills_required in self.jobs.items():
            for index_skills_required in range(len(skills_required)):
                if skills_required[index_skills_required] == 1:
                    for i in range(len(self.state)):
                        e -= (self.skills[self.state[i]][index_skills_required]) * self.beta + (
                            self.preferences[self.state[i]][(list(self.jobs.keys()).index(job))]) * self.alfa
        return e

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


if __name__ == '__main__':

    alfa = 10
    beta = 1
    team = 5
    Tmax = 25000.0  # Max (starting) temperature
    Tmin = 2.5  # Min (ending) temperature
    steps = 50000  # Number of iterations
    updates = 100  # Number of updates (by default an update prints to stdout)

    # Static test data;
    # jobs: Dict[str, Tuple[int, int, int, int, int]] = {
    #     'A1': (1, 1, 0, 1, 0),
    #     'A2': (0, 1, 1, 1, 0),
    #     'A3': (1, 1, 0, 0, 1),
    #     'A4': (0, 1, 0, 1, 1),
    #     'A5': (0, 1, 0, 0, 1),
    # }
    #
    # skills = {
    #     'P1': (5, 9, 3, 2, 6),
    #     'P2': (7, 0, 8, 4, 8),
    #     'P3': (8, 0, 0, 8, 7),
    #     'P4': (9, 1, 2, 0, 2),
    #     'P5': (2, 9, 7, 7, 0),
    #     'P6': (1, 2, 6, 1, 9),
    #     'P7': (2, 2, 1, 9, 6),
    #     'P8': (4, 6, 3, 6, 8),
    #     'P9': (2, 1, 7, 4, 7),
    #     'P10': (7, 3, 3, 5, 7),
    # }
    #
    # preferences = {
    #     'P1': (0, 0, 4, 3, 2),
    #     'P2': (0, 0, 6, 0, 7),
    #     'P3': (4, 8, 9, 3, 5),
    #     'P4': (8, 0, 8, 0, 6),
    #     'P5': (3, 3, 8, 0, 6),
    #     'P6': (3, 3, 8, 0, 4),
    #     'P7': (9, 1, 0, 5, 0),
    #     'P8': (6, 7, 0, 0, 6),
    #     'P9': (3, 0, 0, 7, 2),
    #     'P10': (2, 0, 2, 4, 8),
    # }

    with open('jobsSkills.txt') as json_file:
        jobs = json.load(json_file)

    with open('peopleSkills.txt') as json_file:
        skills = json.load(json_file)
    with open('peoplePreference.txt') as json_file:
        preferences = json.load(json_file)

    # initial state, a randomly-ordered itinerary
    people = list(skills.keys())
    random.shuffle(people)
    init_state = people[0:team]

    tsp = AssembleTeamProblem(init_state, jobs, skills, preferences, people, alfa, beta)
    tsp.set_schedule(tsp.auto(minutes=0.2))
    tsp.Tmax = Tmax  # Max (starting) temperature
    tsp.Tmin = Tmin  # Min (ending) temperature
    tsp.steps = steps  # Number of iterations
    tsp.updates = updates  # Number of updates (by default an update prints to stdout)
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()

    print("Team:", sorted(state))
    print("Fuction:", (-1)*e)
