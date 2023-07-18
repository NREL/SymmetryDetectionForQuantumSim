
import copy

''' bstr
    given an integer, transform it to a bitstring rightmostsignificant
'''
def bstr(state, n):
    return ('{0:0'+str(n)+'b}').format(state)

def binary_matrix(matrix):
    ''' a very inefficient way to use binary matrices
    '''
    return [[1 if j!=0 else 0 for j in i] for i in matrix]

def matrix_mul(X, Y):
    ''' multiply X*Y 
        NOTE: numpy is faster than this, we implement our own to avoid importing any packages
    '''
    return [[sum(i*j for i,j in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]





class StringEditMap:
    ''' StringEditMap class
        We want to transitively close local operators, and use them to describe a full quantum system
        
        The state-to-state transitions are stored as the measurement basis bitstrings, with their qubit ids
        listed in order
    '''
    def __init__(self, unitary_operator, qubits):
        self.matrix = unitary_operator

        self.qubits = qubits
        self.local_range = len(qubits)

        self.edit_map = {}  # map a bitstring -> the local set of states accessible through this operator

        # define local symmetry protected subspaces
        self.__define_local_groups()

    def __define_local_groups(self):
        ''' helper
            create the cluster graph of a k-local operator, which the string edit map uses
            from Alg. III.I
        '''
        transition_table = binary_matrix(self.matrix) + binary_matrix(list(zip(*self.matrix))) # binary matrix plus its transpose
        transition_table_2 = binary_matrix(matrix_mul(transition_table,transition_table))
        while transition_table != transition_table_2:
            transition_table = transition_table_2
            transition_table_2 = binary_matrix(matrix_mul(transition_table_2,transition_table_2))
        
        for source in range(2**self.local_range):
            self.edit_map[bstr(source, self.local_range)] = set()
            for sink in range(2**self.local_range):
                if transition_table[sink][source] == 1:
                    self.edit_map[bstr(source, self.local_range)].add(bstr(sink, self.local_range))

    def __str__(self):
        subspaces = set([tuple(target) for target in self.edit_map.values()])
        s = 'StringEditOperator: qubits={}, subspaces={}'.format(self.qubits, subspaces)
        return s

    def map(self, mbasis_string):
        ''' map L(|b>) = {|b'>}
            given a measurement basis bitstring, return the set of states which we could see after one application of this operator
            NOTE: there are more efficient ways to do this
        '''
        next_states = set([mbasis_string]) # this implicity includes the identity operator
        n = len(mbasis_string)
        local_bitstring = ''
        # get the k-local substring
        for qubit in self.qubits:
            value = mbasis_string[qubit] 
            local_bitstring += value

        # make a local edit with the subspace
        for next_substring in self.edit_map[local_bitstring]:
            if next_substring != local_bitstring: # skip identity
                next_state = list(mbasis_string) # we need to do some list-string hacking
                # replace 
                for i,val in enumerate(next_substring):
                    next_state[self.qubits[i]] = val
                next_states.add(''.join(next_state))
        return next_states





class QuantumSystem:
    ''' QuantumSystem class
        We want to store a system of unitary operators as a set of StringEditOperator objects; this will 
        encode all possible state-to-state interactions in the measurement basis
    '''
    def __init__(self, maps):
        self.system_maps = maps   # a list of string edit maps

    def __str__(self):
        s = 'Quantum System has substring edit maps:\n'
        for op in self.system_maps:
            s += op.__str__() + '\n'
        return s
    
    def __repr__(self):
        return str(self)

    def map_all_maps(self, mbasis_string):
        ''' get the space of states which are available in a single application of each local string edit map '''
        nearest_subspace_neighbors = set([mbasis_string])
        for local_map in self.system_maps:
            map_to = local_map.map(mbasis_string)
            for next_state in map_to:
                nearest_subspace_neighbors.add(next_state)
        return nearest_subspace_neighbors

    def transitive_closure(self, initial_condition, edge_limit=None):
        ''' Complete a transitive closure of the quantum system
            edge_limit is the number of times we apply the system of operators before halting
                edge_limit==1 <==> map_all_maps
        '''
        queue = []
        G = set([initial_condition])
        queue.append(initial_condition)
        while len(queue)!= 0:
            b = queue.pop(0)
            for b_prime in self.map_all_maps(b):
                if b_prime not in G:
                    G.add(b_prime)
                    queue.append(b_prime)
        return G

    def hilbert_space_closure(self, system_size):
        ''' calculate the symmetry protected subspaces of each state in a Hilbert space 
            Given a number of spins, get the symmetry protected subspace information for each measurement basis vector for those spins
        '''
        seen_states = set([])
        subspaces_list = []
        for state_int in range(2**system_size):
            state = bstr(state_int, system_size)
            if state in seen_states:
                continue
            seen_states.add(state)
            state_sps = self.transitive_closure(state)
            for s in state_sps:
                seen_states.add(s)
            subspaces_list.append(state_sps)
        return subspaces_list





class MeasurementVerifier:
    ''' A class to do post-selection
        this is seperate from the computation class to specialize more, store intermediate states, etc
    '''
    def __init__(self, quantum_computation, initial_condition):
        self.quantum_computation = quantum_computation
        self.initial_condition = initial_condition

    def greedy_min_sets_search(self, state, max_depth=1):
        ''' Use a greedy algorithm to do our pathfinding
                piggyback on the transitive closure process
        '''
        self.search_depth = 0
        b_next = state
        b_curr = None

        while b_curr is None or b_next != b_curr:
            T_b_curr = set([b_curr, b_next])
            b_curr = b_next
            self.search_depth += 1

            queue = [(b_curr, 0)]
            local_min = b_curr
            while len(queue) != 0:
                b_prime, b_prime_depth = queue.pop(0)

                if b_prime_depth == max_depth: 
                    break

                for b_prime_prime in self.quantum_computation.map_all_maps(b_prime):
                    if b_prime_prime not in T_b_curr:
                        queue.append((b_prime_prime, b_prime_depth+1))
                        T_b_curr.add(b_prime_prime)
                        if int(b_prime_prime,2) < int(local_min,2):
                            local_min = b_prime_prime
            b_next = local_min

        return b_curr
                        