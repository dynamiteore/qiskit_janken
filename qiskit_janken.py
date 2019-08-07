print("now loading...")
import numpy as np
from qiskit import *
from qiskit import BasicAer
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram

def quantum_janken():
    # qbit数
    n = 5
    
    q = QuantumRegister(n, 'q')
    circ = QuantumCircuit(q)
    
    # 全qubitを重ね合わせ状態にしてみる
    for i in range(n):
        circ.h(q[i])
    
    # えんたんぐるさせてみる 意味ない？
    circ.cx(q[3], q[4])
    circ.cx(q[2], q[3])
    circ.cx(q[1], q[2])
    circ.cx(q[0], q[1])
    
    
    # 観測する
    c = ClassicalRegister(n, 'c')
    meas = QuantumCircuit(q, c)
    meas.barrier(q)
    meas.measure(q,c)
    
    qc = circ+meas
    
    IBMQ.save_account('a1346077218bfce3358a898007a5bc93ef29a017b768e570e46437b740806e0cc25c760485f411a6b740070e6b27c2cf8290356ba177894e3253682d4e281737')
    #IBMQ.save_account('MY_TOKEN')  # 自分のとーくんをつかってね
    provider = IBMQ.load_account()
    large_enough_devices = provider.backends(filters=lambda x: x.configuration().n_qubits < 10 and
                                                                       not x.configuration().simulator)
    
    backend = BasicAer.get_backend('qasm_simulator')    # シミュレーターはこっちを使う
    #backend = least_busy(large_enough_devices)         # 実機の場合はこっちを使う。順番待ちなのでおそいよ
    
    # 1024回試行
    shots = 1024
    max_credits = 1
    job_exp = execute(qc, backend=backend, shots=shots, max_credits=max_credits)
    job_monitor(job_exp)
    result_exp = job_exp.result()
    counts_exp = result_exp.get_counts(qc)
    
    # 一番確率が高い値を採用
    rslt = int(max(counts_exp, key=counts_exp.get),2)
    
    if rslt < 10:
        return 1
    elif rslt < 20:
        return 2
    elif rslt < 30:
        return 3
    else:
        return 4

aaa = quantum_janken()

print("\nYOUじゃんけんしていきなよ、\n[1] グー\n[2] ちょき\n[3] per\n")
bbb = int(input())

