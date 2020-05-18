from __future__ import print_function
import random
from typing import Dict, Tuple

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

        return self.energy() + initial_energy

    def energy(self):
        """Calculates objective function."""
        e = 0
        for job in self.jobs:
            for skill_required in (demand for demand in job if demand==1):
                for i in range(len(self.state)):
                    e += (self.skills[self.state[i]][skill_required])*self.beta + (self.preferences[self.state[i]][job])*self.alfa
        for job, skills_required in self.jobs.items():
            for index_skills_required in range(len(skills_required)):
                if skills_required[index_skills_required] == 1:
                    for i in range(len(self.state)):
                        e += (self.skills[self.state[i]][index_skills_required]) * self.beta + (
                            self.preferences[self.state[i]][(list(self.jobs.keys()).index(job))]) * self.alfa
        return e


if __name__ == '__main__':

    alfa = 10
    beta = 10
    team = 5
    Tmax = 25000.0  # Max (starting) temperature
    Tmin = 2.5  # Min (ending) temperature
    steps = 50000  # Number of iterations
    updates = 100  # Number of updates (by default an update prints to stdout)

    jobs: Dict[str, Tuple[int, int, int, int, int]] = {
        'A1': (1, 1, 0, 1, 0),
        'A2': (0, 1, 1, 1, 0),
        'A3': (1, 1, 0, 0, 1),
        'A4': (0, 1, 0, 1, 1),
        'A5': (0, 1, 0, 0, 1),
    }

    skills = {
        'P1': (5, 9, 3, 2, 6),
        'P2': (7, 0, 8, 4, 8),
        'P3': (8, 0, 0, 8, 7),
        'P4': (9, 1, 2, 0, 2),
        'P5': (2, 9, 7, 7, 0),
        'P6': (1, 2, 6, 1, 9),
        'P7': (2, 2, 1, 9, 6),
        'P8': (4, 6, 3, 6, 8),
        'P9': (2, 1, 7, 4, 7),
        'P10': (7, 3, 3, 5, 7),
    }

    preferences = {
        'P1': (0, 0, 4, 3, 2),
        'P2': (0, 0, 6, 0, 7),
        'P3': (4, 8, 9, 3, 5),
        'P4': (8, 0, 8, 0, 6),
        'P5': (3, 3, 8, 0, 6),
        'P6': (3, 3, 8, 0, 4),
        'P7': (9, 1, 0, 5, 0),
        'P8': (6, 7, 0, 0, 6),
        'P9': (3, 0, 0, 7, 2),
        'P10': (2, 0, 2, 4, 8),
    }

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
    print("Fuction:", e)
