from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import PhaseOracleGate
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

N_QUBITS = 6
N = 1 << N_QUBITS

F_CONSTANT = False

keys = [
    "111000",
    "111100",
    "111110",
]
keys = [key[::-1] for key in keys] # reverse the keys because qiskit expects Little Endian
NUM_SOLUTIONS = len(keys)

def expression_for_key(key):
    literals = [f'{'~' if int(val) == 0 else ''}x{i}' for i, val in enumerate(key, 1)]
    return '(' + ' & '.join(literals) + ')'

keys_expression = ' | '.join([expression_for_key(key) for key in keys])
Z_f = PhaseOracleGate(
    keys_expression,
    var_order=[f"x{n+1}" for n in range(N_QUBITS)],
    label="Z_f"
)

grover_iteration_circuit = QuantumCircuit(N_QUBITS)
grover_iteration_circuit.append(Z_f, range(N_QUBITS))
grover_iteration_circuit.h(range(N_QUBITS))
grover_iteration_circuit.append(PhaseOracleGate(
    ' | '.join([f'x{n+1}' for n in range(N_QUBITS)]),
    label='Z_OR'
), range(N_QUBITS))
grover_iteration_circuit.h(range(N_QUBITS))
G = grover_iteration_circuit.to_gate(label="G")

num_iterations = int(np.floor(np.pi / 4 * np.sqrt(N / NUM_SOLUTIONS)))

qc = QuantumCircuit(N_QUBITS)
qc.h(range(N_QUBITS))
for i in range(num_iterations):
    qc.append(G, range(N_QUBITS))
qc.measure_all()

print(qc.draw("text"))

sampler = StatevectorSampler()
result = sampler.run([qc], shots=2**16).result()
counts = result[0].data.meas.get_counts()

plot_histogram(counts)
plt.show()
