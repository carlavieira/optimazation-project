from __future__ import print_function
import math
import random
from typing import Dict, Tuple

from simanneal import Annealer


def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R


class TravellingSalesmanProblem(Annealer):

    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i-1]][self.state[i]]
        return e

class MakeTeamProblem(Annealer):

    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, jobs, skills, preferences):
        self.jobs = jobs,
        self.skills = skills,
        self.preferences = preferences,
        self.alfa = 1, #preferênce
        self.beta = 10, #skill
        super(MakeTeamProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for job in self.jobs:
            for skill_required in (demand for demand in job if demand==1):
                for i in range(len(self.state)):
                    e += (self.skills[self.state[i]][skill_required])*self.beta + (self.preferences[self.state[i]][job])*self.alfa
        return e


if __name__ == '__main__':

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
    state = ['P1', 'P3', 'P5', 'P8', 'P10']


    e = 0
    for job, skills_required in jobs.items():
        print("job:", job)
        print("skills_required:", skills_required)
        for index_skills_required in range(len(skills_required)):
            if skills_required[index_skills_required] == 1:
                print("index_skills_required:", index_skills_required)
                for i in range(len(state)):
                    print(state[i])
                    e += (skills[state[i]][index_skills_required]) * 10 + (
                    preferences[state[i]][(list(jobs.keys()).index(job))]) * 10
    print(e)

    print(state)
