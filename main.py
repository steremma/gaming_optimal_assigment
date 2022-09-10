import copy

MAXIMUM_N_PREFERENCES = 3

class Node():
    """A node in our tree representing a (potentially partial) assignment of people to roles.
    
    If the assignment is complete, then this is a leaf node. Else it is an intermediate one.
    """
    def __init__(self, requirement, assignment, score=0):
        self.requirement = requirement
        self.assignment = assignment
        self.score = score
        self.available_roles = {}
        
        tmp_reqs = copy.deepcopy(requirement)
        for _, role in assignment.items():
            tmp_reqs[role] -= 1
            
        self.available_roles = {k for k, v in tmp_reqs.items() if v > 0}
            
            
    def is_valid(self, assignment):
        check = {k: v for k, v in self.requirement.items()}
        for name, role in assignment.items():
            if role not in check:
                raise ValueError('Unknown role {}'.format(role))
            check[role] -= 1
            if check[role] < 0:
                return False
        
        return True
    
    @classmethod
    def _score(cls, role, preference):
        if role in preference.positives:
            return 1
        if role in preference.negatives:
            return -1
        return 0
    
    
    def get_children(self, preferences):
        for name, preference in preferences.items():
            if name not in self.assignment:
                break
        
        assignments = [{**self.assignment, name: role} for role in self.available_roles]
        scores = [self.score + Node._score(assignment[name], preference) for assignment in assignments]
        return [
            Node(self.requirement, assignment=assignment, score=score)
            for assignment, score in zip(assignments, scores)
        ]

    def __repr__(self):
        return "STATE: {} || SCORE: {}".format(self.assignment, self.score)
    
    def is_leaf(self):
        counts = {role: 0 for role in self.requirement.keys()}
        for name, role in self.assignment.items():
            counts[role] += 1
            
        return counts == self.requirement

def find_possible_complete_assignments(requirement, preferences):
    n = Node(requirement, assignment={})
    neighbours = [n]
    complete_assignments = []
    while len(neighbours) > 0:
        current = neighbours.pop()
        if current.is_leaf():
            complete_assignments.append(current)
        neighbours += current.get_children(preferences)
    
    return complete_assignments
        

requirement = {
    'nuker': 3,
    'bd': 1,
    'sws': 1,
    'bp': 1,
    'ol': 1,
    'ee': 1,
    'se': 1
}
preferences = {
    'mysticism': Preference(positives=['nuker', 'bd'], negatives=['sws']),
    'ttl': Preference(positives=['nuker'], negatives=[]),
    'vella': Preference(positives=['ee']),
    'fortuna': Preference(positives=['sws']),
    'noveria': Preference(positives=['sws'], negatives=['bp']),
    'maria': Preference(positives=['nuker', 'bd']),
    'melz': Preference(negatives=['ee']),
    'emperior': Preference(positives=['ol']),
    'jet': Preference(positives=['nuker'])
}

complete_assignments = find_possible_complete_assignments(requirement, preferences)        
