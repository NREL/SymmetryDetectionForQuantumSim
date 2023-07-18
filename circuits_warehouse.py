
import cirq
import numpy as np
import os
#import Q


########
# T6 QCA
########
def unitary_T6QCA(q0, q1, q2):
    # q0 o--
    #    | 
    # q1 H-H
    #      |
    # q2 --o
    return cirq.Circuit(cirq.H(q1).controlled_by(q0), 
                        cirq.H(q1).controlled_by(q2)
                       )

def circuit_T6QCA(qubits):
    circuit = cirq.Circuit()
    for i in range(1,len(qubits)-1,2):
        circuit += unitary_T6QCA(qubits[i-1],qubits[i],qubits[i+1])
    for i in range(2,len(qubits)-1,2):
        circuit += unitary_T6QCA(qubits[i-1],qubits[i],qubits[i+1])
    return circuit

def circuit_T6QCA_noise(qubits, error_rate):
    circuit = circuit_T6QCA(qubits)
    ## TODO: make more accurate/better
    #circuit.append([cirq.X(q).with_probability(error_rate) for q in qubits])
    #circuit.append([cirq.Y(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.X(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.Y(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.Z(q).with_probability(error_rate) for q in qubits])
    return circuit

#def computation_T6QCA(n_qubits, exponent=.2):
#    ## Qubit information for our simulation
#    q = cirq.LineQubit.range(n)
#    q_ids = list(range(n))
#
#    ## A full T6QCA simulation
#    t6qca_cycle = [] # list( (circuit, q_ids) )
#
#    # even
#    for i in range(2, n-1, 2):
#        t6qca_cycle.append((cw.unitary_T6QCA(q[i-1], q[i], q[i+1]),[i-1, i,i+1]))
#    # odd
#    for i in range(1, n-1, 2):
#        t6qca_cycle.append((cw.unitary_T6QCA(q[i-1], q[i], q[i+1]),[i-1, i,i+1]))
#            
#    ## Make a simulation
#    computation = prx2.QuantumSystem(
#                        [prx2.LocalEditOperator(cirq.unitary(op[0]), op[1]) for _, op in enumerate(t6qca_cycle)]
#                  )


########
# HeisXXX
########
def unitary_HeisenbergXXX(q0, q1, exponent):
    return cirq.Circuit(cirq.ZZ(q0, q1)**exponent, cirq.ISWAP(q0, q1)**exponent)

#def unitary_list_HeisenbergXXX(qubits, dt, time_steps):#T, dt):
#    in_order_ops = []
#    for 

def circuit_Heisenberg1D(qubits, exponent=.2):
    circuit = cirq.Circuit()
    # even
    for i in range(0, len(qubits)-1, 2):
        circuit += unitary_HeisenbergXXX(qubits[i],qubits[i+1],exponent)
    # odd
    for i in range(1, len(qubits)-1, 2):
        circuit += unitary_HeisenbergXXX(qubits[i],qubits[i+1],exponent)
    return circuit

def circuit_Heisenberg_noise(qubits, error_rate, exponent=.2,):
    circuit = circuit_Heisenberg1D(qubits, exponent)
    # TODO: make more accurate/better
    circuit.append([cirq.X(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.Y(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.Z(q).with_probability(error_rate) for q in qubits])
    #circuit.append([cirq.depolarize(error_rate, 1).on(q) for q in qubits])
    return circuit

#def computation_HeisenbergXXX(n_qubits, exponent=.2):
#    q = cirq.LineQubit.range(n)
#    q_ids = list(range(n))
#
#    ## A full Heisenberg simulation
#    heisenberg_cycle = [] # list( (circuit, q_ids) )
#
#    # even
#    for i in range(0, n-1, 2):
#        heisenberg_cycle.append((cw.unitary_HeisenbergXXX(q[i], q[i+1], exponent),[i,i+1]))
#    # odd
#    for i in range(1, n-1, 2):
#        heisenberg_cycle.append((cw.unitary_HeisenbergXXX(q[i], q[i+1], exponent),[i,i+1]))
#            
#    ## Make a simulation
#    computation = prx2.QuantumSystem(
#                        [prx2.LocalEditOperator(cirq.unitary(op[0]), op[1]) for _, op in enumerate(heisenberg_cycle)]
#                  )
#    #return cirq.Circuit(heisenberg_cycle), computation
#    return computation


########
# F4QCA
########
control_qubits = [cirq.LineQubit(0), cirq.LineQubit(1), cirq.LineQubit(3), cirq.LineQubit(4)]
target_qubit = cirq.LineQubit(2)
F4QCAGATE = cirq.MatrixGate(cirq.unitary(cirq.Circuit([
                cirq.Moment(cirq.X.on_each(control_qubits)),
                cirq.H(target_qubit).controlled_by(control_qubits[0]).controlled_by(control_qubits[1]).controlled_by(control_qubits[2]).controlled_by(control_qubits[3]),
                cirq.X.on_each(control_qubits),
                cirq.H(target_qubit).controlled_by(control_qubits[0]).controlled_by(control_qubits[1]).controlled_by(control_qubits[2]).controlled_by(control_qubits[3]),
                cirq.H(target_qubit),
                [cirq.H(target_qubit).controlled_by(c) for c in control_qubits]
            ])))
def unitary_F4QCA(target_qubit, control_qubits):
    return F4QCAGATE.on(control_qubits[0], control_qubits[1], target_qubit, control_qubits[2], control_qubits[3])
    #return cirq.MatrixGate(cirq.unitary(cirq.Circuit([
    #            cirq.Moment(cirq.X.on_each(control_qubits)),
    #            cirq.H(target_qubit).controlled_by(control_qubits[0]).controlled_by(control_qubits[1]).controlled_by(control_qubits[2]).controlled_by(control_qubits[3]),
    #            cirq.X.on_each(control_qubits),
    #            cirq.H(target_qubit).controlled_by(control_qubits[0]).controlled_by(control_qubits[1]).controlled_by(control_qubits[2]).controlled_by(control_qubits[3]),
    #            cirq.H(target_qubit),
    #            [cirq.H(target_qubit).controlled_by(c) for c in control_qubits]
    #        ]))).on(control_qubits[0], control_qubits[1], target_qubit, control_qubits[2], control_qubits[3])

def circuit_F4QCA(qubits, even=True):
    circuit = cirq.Circuit()
        
    for i in range(4,len(qubits)-2,3):
        target_qubit = qubits[i]
        control_qubits = qubits[i-2:i] + qubits[i+1:i+3]
        circuit += unitary_F4QCA(target_qubit,control_qubits)
    if even:
        for i in range(3,len(qubits)-2,3):
            target_qubit = qubits[i]
            control_qubits = qubits[i-2:i] + qubits[i+1:i+3]
            circuit += unitary_F4QCA(target_qubit,control_qubits)
        for i in range(2,len(qubits)-2,3):
            target_qubit = qubits[i]
            control_qubits = qubits[i-2:i] + qubits[i+1:i+3]
            circuit += unitary_F4QCA(target_qubit,control_qubits)

    if not even:
        for i in range(2,len(qubits)-2,3):
            target_qubit = qubits[i]
            control_qubits = qubits[i-2:i] + qubits[i+1:i+3]
            circuit += unitary_F4QCA(target_qubit,control_qubits)
        for i in range(3,len(qubits)-2,3):
            target_qubit = qubits[i]
            control_qubits = qubits[i-2:i] + qubits[i+1:i+3]
            circuit += unitary_F4QCA(target_qubit,control_qubits)
    return circuit

def circuit_F4QCA_noise(qubits, error_rate, even):
    circuit = cirq.align_left(circuit_F4QCA(qubits, even))
    ## TODO: fix errors
    #circuit.append([cirq.X(q).with_probability(error_rate) for q in qubits])
    #circuit.append([cirq.Y(q).with_probability(error_rate) for q in qubits])
    #circuit.append([cirq.depolarize(error_rate, 1).on(q) for q in qubits])
    circuit.append([cirq.X(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.Y(q).with_probability(error_rate) for q in qubits])
    circuit.append([cirq.Z(q).with_probability(error_rate) for q in qubits])
    return circuit


class QuantumCircuitDriver:
    ''' QuantumCircuitDriver class
        Manage a quantum circuit, if it is noisy, how many qubits, mixing layers, measurement preparation, etc
    '''
    def __init__(self, quantum_system_circuit, qubits):
        self.qubits = qubits
        self.quantum_system_circuit = quantum_system_circuit

    def simulate(self, circuit_initial_condition, time_steps, nmeas=1_000, parameters=None, noisy=False, measurement_circuit=None, simulator=cirq.Simulator()):
        ''' simulate the simulation for a few time steps
            int             :time_steps:            the numer of discrete time steps in the simulation
            list(int)       :parameters:            an additional exponent over the simulation at each time step, len(parameter) == time_steps
            bool            :noisy:                 should we add random pauli errors?
            cirq.Circuit    :measurement_circuit:   basis transformation gates
        '''
        circuit = circuit_initial_condition
        # if no basis transformation
        if measurement_circuit is None:
            measurement_circuit = cirq.I.on_each(self.qubits)
        # construct, leave option for variational parameters
        if parameters is None:
            circuit += cirq.Circuit([self.quantum_system_circuit for _ in range(time_steps)])
        else:
            assert(len(parameters) == time_steps)
            for t in range(time_steps):
                circuit += cirq.Circuit([op**parameters[t] for op in self.quantum_system_circuit])

        circuit += measurement_circuit
        circuit += cirq.measure(*self.qubits)#, key='z')

        # run and measure
        results = simulator.run(circuit, repetitions=nmeas)
        return results
