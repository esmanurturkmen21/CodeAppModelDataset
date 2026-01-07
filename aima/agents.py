"""
Agents and Environments (Chapters 1-2)
Simplified and cleaned version for core functionality.
"""

import random
import collections
from statistics import mean

# -------------------- Things --------------------

class Thing:
    """A physical object that can exist in an environment."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        return hasattr(self, 'alive') and self.alive


class Agent(Thing):
    """An agent that acts in an environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None or not isinstance(program, collections.abc.Callable):
            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))
        self.program = program

    def can_grab(self, thing):
        return False


# -------------------- Environments --------------------

class Environment:
    """Abstract environment."""

    def __init__(self):
        self.things = []
        self.agents = []

    def percept(self, agent):
        raise NotImplementedError

    def execute_action(self, agent, action):
        raise NotImplementedError

    def default_location(self, thing):
        return None

    def is_done(self):
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        if self.is_done():
            return
        actions = [agent.program(self.percept(agent)) if agent.alive else None
                   for agent in self.agents]
        for agent, action in zip(self.agents, actions):
            if action is not None:
                self.execute_action(agent, action)

    def run(self, steps=1000):
        for _ in range(steps):
            if self.is_done():
                break
            self.step()

    def add_thing(self, thing, location=None):
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        thing.location = location if location is not None else self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            self.agents.append(thing)

# -------------------- XY Environment --------------------

class XYEnvironment(Environment):
    """Environment on a 2D grid."""

    def __init__(self, width=10, height=10):
        super().__init__()
        self.width = width
        self.height = height

    def is_inbounds(self, location):
        x, y = location
        return 0 <= x < self.width and 0 <= y < self.height

    def default_location(self, thing):
        return (random.randint(0, self.width - 1), random.randint(0, self.height - 1))


# -------------------- Vacuum World --------------------

loc_A, loc_B = (0, 0), (1, 0)

class Dirt(Thing):
    pass

class ReflexVacuumAgent(Agent):
    def __init__(self):
        def program(percept):
            location, status = percept
            if status == 'Dirty':
                return 'Suck'
            elif location == loc_A:
                return 'Right'
            elif location == loc_B:
                return 'Left'
        super().__init__(program)


class TrivialVacuumEnvironment(Environment):
    """Two-location vacuum environment."""

    def __init__(self):
        super().__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty'])}

    def percept(self, agent):
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        if action == 'Right':
            agent.location = loc_B
            agent.performance -= 1
        elif action == 'Left':
            agent.location = loc_A
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'


# -------------------- Helper functions --------------------

def test_agent(AgentFactory, steps=100):
    env = TrivialVacuumEnvironment()
    agent = AgentFactory()
    env.add_thing(agent, loc_A)
    env.run(steps)
    return agent.performance
