from utils.helpers import is_nearly_equal_to

class ParetoDominanceForPoints():
    """
    Pareto dominance: Given a set of objectives, a solution is said to Pareto dominate another if the 
    first is not inferior to the second in all objectives, and, additionally, there is at least one 
    objective where it is better.

    This code is based on the original SBB C++ version that used teams and points to obtains teams 
    or points focused on obtaining distinct solutions.
    """

    @staticmethod
    def run(point_population, teams_population, to_keep):
        """
        Finds the pareto front, i.e. the pareto dominant points.
        """
        results_map = ParetoDominanceForPoints._generate_results_map_for_points(point_population, teams_population)
        front, dominateds = ParetoDominanceForPoints._pareto_front(point_population, results_map)

        keep_solutions = front
        remove_solutions = dominateds
        if len(keep_solutions) < to_keep:  # must include some teams from dominateds
            ParetoDominanceForPoints._fitness_sharing_for_points(point_population, results_map)
            keep_solutions, remove_solutions = ParetoDominanceForPoints._balance_pareto_front_to_up(point_population, keep_solutions, remove_solutions, to_keep)
        if len(keep_solutions) > to_keep: # must discard some teams from front
            ParetoDominanceForPoints._fitness_sharing_for_points(front, results_map)
            keep_solutions, remove_solutions = ParetoDominanceForPoints._balance_pareto_front_to_down(front, keep_solutions, remove_solutions, to_keep)
        return keep_solutions, remove_solutions

    @staticmethod
    def _generate_results_map_for_points(point_population, teams_population):
        """
        Create a a matrix of (points) x (array version of a matrix that compares all teams outcomes against 
        each other for this point  (0: <=, 1: >)). This matrix is used by pareto to find a front of points 
        that characterize distinct teams.
        """
        results_map = []
        try:
            for point in point_population:
                distinction_vector = []
                for team1 in teams_population:
                    outcome1 = team1.results_per_points_[point.point_id]
                    for team2 in teams_population:
                        outcome2 = team2.results_per_points_[point.point_id]                 
                        if outcome1 > outcome2 and not is_nearly_equal_to(outcome1, outcome2):
                            distinction_vector.append(1)
                        else:
                            distinction_vector.append(0)
                results_map.append(distinction_vector)
        except KeyError as e:
            raise KeyError("A team hasn't processed the point "+str(e)+" before! You got a bug!")
        return results_map

    @staticmethod
    def _pareto_front(solutions, results_map):
        """
        Finds the pareto front, i.e. the pareto dominant solutions.
        """
        front = []
        dominateds = []
        i = 0
        for solution, outcomes1 in zip(solutions, results_map):
            is_dominated = False
            j = 0
            for outcomes2 in results_map:
                is_dominated, is_equal = ParetoDominanceForPoints._check_if_is_dominated(outcomes1, outcomes2)
                if j < i and is_equal: # also dominated if equal to a previous processed item, since this one would be irrelevant
                    is_dominated = True
                if is_dominated:
                    break
                j += 1
            if is_dominated:
                dominateds.append(solution)
            else:
                front.append(solution)
            i += 1
        return front, dominateds

    @staticmethod
    def _check_if_is_dominated(results1, results2):
        """
        Check if a solution is domninated or equal to another, assuming that higher results are better than lower ones.
        """  
        equal = True
        for index in range(len(results1)):
            if not is_nearly_equal_to(results1[index], results2[index]):
                equal = False
                if(results1[index] > results2[index]): # not dominated since "results1" is greater than "results2" in this dimension
                    return False, equal
        if equal:
            return False, equal
        else:
            return True, equal

    @staticmethod
    def _fitness_sharing_for_points(population, results_map):
        """
        Equal to fitness_sharing, but works specifically for points (ie. dont have previous fitness values and uses 'results_map').
        """
        # calculate denominators in each dimension
        denominators = [1.0] * len(results_map[0]) # initialized to 1 so we don't divide by zero
        for individual, results in zip(population, results_map):
            for index, value in enumerate(results):
                denominators[index] += float(value)

        # calculate fitness
        for individual, results in zip(population, results_map):
            score = 0.0
            for index, value in enumerate(results):
                score += float(value) / denominators[index]
            individual.fitness_ = score/float(len(results_map[0]))

    @staticmethod
    def _balance_pareto_front_to_up(population, keep_solutions, remove_solutions, to_keep):
        sorted_solutions = sorted(population, key=lambda solution: solution.fitness_, reverse = True) # better ones first
        for solution in sorted_solutions:
            if solution not in keep_solutions:
                keep_solutions.append(solution)
                remove_solutions.remove(solution)
            if len(keep_solutions) == to_keep:
                break
        return keep_solutions, remove_solutions

    @staticmethod
    def _balance_pareto_front_to_down(population, keep_solutions, remove_solutions, to_keep):
        sorted_solutions = sorted(population, key=lambda solution: solution.fitness_, reverse = False) # worse ones first
        for solution in sorted_solutions:
            keep_solutions.remove(solution)
            remove_solutions.append(solution)
            if len(keep_solutions) == to_keep:
                break
        return keep_solutions, remove_solutions