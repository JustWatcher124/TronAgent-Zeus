class CutOffDetector:
    def __init__(self):
        self.agents = []

    def set_agent(self, agent):
        self.agents.append(agent)

    def did_cutoff(self, name):
        agent_one = self.agents[0]
        agent_two = self.agents[1]

        name_of_cutter_offer = ""
        if agent_one.head in agent_two.snake[1:]:
            name_of_cutter_offer = agent_two.name
        if agent_two.head in agent_one.snake[1:]:
            name_of_cutter_offer = agent_one.name

        if name == name_of_cutter_offer:
            return True
        else:
            return False
            

