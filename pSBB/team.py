import random
import numpy
from collections import Counter
from program import Program
from environments.classification_environment import ClassificationEnvironment
from utils.helpers import round_value_to_decimals, round_array_to_decimals
from config import CONFIG, RESTRICTIONS

def reset_teams_ids():
    global next_team_id
    next_team_id = 0

def get_team_id():
    global next_team_id
    next_team_id += 1
    return next_team_id

class Team:
    def __init__(self, generation, environment, programs, initialization=True):
        self.team_id = get_team_id()
        self.generation = generation
        self.environment = environment
        self.fitness = -1
        self.score_trainingset = 0
        self.score_testset = 0
        self.extra_metrics = {}
        self.programs = []
        self.active_programs = []
        if initialization:
            # randomly gets one program per action
            programs_per_class = self.__get_programs_per_class(programs)
            for action in programs_per_class: # programs is an array of programs per action
                program = random.choice(action)
                self.programs.append(program)
                program.add_team(self)
        else:
            # add all programs to itself
            for program in programs: # programs is an array of programs
                self.programs.append(program)
                program.add_team(self)

    def __get_programs_per_class(self, programs):
        programs_per_class = []
        for class_index in range(self.environment.total_actions):
            values = [p for p in programs if p.action == class_index]
            if len(values) == 0:
                print "WARNING! No programs for class "+str(class_index)
                raise Exception # to improve
            programs_per_class.append(values)
        return programs_per_class

    def execute(self, data, testset=False): # modificar para ser compativel com reinforcement learning
        # execute code for each input
        outputs = []
        X = ClassificationEnvironment.get_X(data)
        Y = ClassificationEnvironment.get_Y(data)
        for x in X:
            partial_outputs = []
            for program in self.programs:
                partial_outputs.append(program.execute(x, testset=False))
            selected_program = self.programs[partial_outputs.index(max(partial_outputs))]
            output_class = selected_program.action
            outputs.append(output_class)
            if selected_program.program_id not in self.active_programs:
                self.active_programs.append(selected_program.program_id)
        # calculate fitness and accuracy
        score, extra_metrics = self.environment.evaluate(outputs, Y, testset)
        if testset:
            self.score_testset = score
            self.extra_metrics = extra_metrics
        else:
            self.fitness = score
            self.score_trainingset = score

    def remove_programs_link(self):
        for p in self.programs:
            p.remove_team(self)

    def mutate(self, new_programs):
        """ Generates mutation chances and mutate the team if it is a valid mutation """
        mutation_chance = random.random()
        if mutation_chance <= CONFIG['training_parameters']['mutation']['team']['remove_program']:
            self.remove_program()
        if len(self.programs) < CONFIG['training_parameters']['team_size']['max']:
            mutation_chance = random.random()
            if mutation_chance <= CONFIG['training_parameters']['mutation']['team']['add_program']:
                self.add_program(new_programs)          

    def remove_program(self):
        """ Remove a program from the team. A program is removible only if there is at least two programs for its action. """
        # Get list of actions with more than one program
        actions = [p.action for p in self.programs]
        actions_count = Counter(actions)
        valid_actions_to_remove = []
        for key, value in actions_count.iteritems():
            if value > 1:
                valid_actions_to_remove.append(key)
        if len(valid_actions_to_remove) == 0:
            return
        # Get list of programs for the removible actions
        valid_programs_to_remove = [p for p in self.programs if p.action in valid_actions_to_remove]
        # Randomly select a program to remove from the list
        removed_program = random.choice(valid_programs_to_remove)
        removed_program.remove_team(self)
        self.programs.remove(removed_program)

    def add_program(self, new_programs):
        if len(new_programs) == 0:
            print "WARNING! NO NEW PROGRAMS!"
            return
        test = False
        while not test:
            new_program = random.choice(new_programs)
            if new_program not in self.programs:
                new_program.add_team(self)
                self.programs.append(new_program)
                test = True

    def print_metrics(self):
        r = round_value_to_decimals
        teams_members_ids = [p.__repr__() for p in self.programs]
        m = str(self.team_id)+":"+str(self.generation)+", team members ("+str(len(self.programs))+"): "+str(teams_members_ids)
        # m += "\nTRAIN: acc: "+str(r(self.accuracy_trainingset)) +", mrecall: "+str(r(self.score_trainingset))
        # m += "\nTEST: acc: "+str(r(self.accuracy_testset))+", mrecall: "+str(r(self.score_testset))+", recall: "+str(round_array_to_decimals(self.recall))
        m += "\nfitness (train): "+str(r(self.fitness))+", score (train): "+str(r(self.score_trainingset))+", score (test): "+str(r(self.score_testset))
        #  print extra_metrics (versao sem verbose ser sem extra_metrics e sem action_counter?)
        return m

    def __repr__(self): 
        return "("+str(self.team_id)+":"+str(self.generation)+")"

    def __str__(self):
        text = "\nTeam "+self.__repr__()+", team size: "+str(len(self.programs))
        text += "\n################"
        for p in self.programs:
            text += "\n"+str(p)
        text += "\n################"
        return text


