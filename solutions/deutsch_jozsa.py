from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import BitFlipOracleGate
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

N = 4

F_CONSTANT = False

expression = "~(x1 | x2 | x3 | x4) | (x1 & x3) | (x2 & x4)" # balanced
balanced_query_gate = BitFlipOracleGate(
    expression,
    var_order=[f"x{n+1}" for n in range(N)],
    label="U_f"
)
constant_query_gate = QuantumCircuit(N+1, name="f(x) = 0").to_gate()

qc = QuantumCircuit(N+1, N)
qc.x(N) # set last qubit to 1
qc.barrier()
qc.h(range(N+1))
qc.append(constant_query_gate if F_CONSTANT else balanced_query_gate, range(N+1))
qc.h(range(N))
qc.measure(range(N), range(N))

qc.draw("mpl", idle_wires=False)

plt.savefig('deutsch_jozsa_circuit.png')

sampler = StatevectorSampler()
result = sampler.run([qc], shots=2**16).result()
counts = result[0].data.c.get_counts()

plt.show()

plot_histogram(counts)

plt.show()

