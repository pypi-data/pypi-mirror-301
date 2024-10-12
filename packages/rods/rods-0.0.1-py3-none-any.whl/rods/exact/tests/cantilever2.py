import os
import sys

cwd = os.getcwd()
folder = os.path.basename(cwd)
while folder != "beam":
    cwd = os.path.dirname(cwd)
    folder = os.path.basename(cwd)
    if len(cwd) == 0:
        print("ERROR finding root.")
        sys.exit()
# print("Root directory:", cwd)
sys.path.insert(0, cwd)

import functools
import numpy as np
from domain import StaticAnalysis
import mesh
import postprocessing as postproc


def case1(P=10.):
    mat = {
        'area':              1e2,
        'elastic_modulus':   1.0e3,
        'shear_modulus':     10,
        'inertia_primary':   20.0,
        'inertia_secondary': 20.0,
        'inertia_torsion':   1e2,
    }
    L = 10

    nodes, elements = mesh.line_mesh(
            A=(0,0,0),
            B=(L,0,0),
            n_elements=2,
            order=1,
            material=mat,
            reference_vector=(0,0,1)
    )

    # (nodes, elements) = mesh.line_mesh(A=(0,0,0), B=(0.8,0.6,0), n_elements=5, order=1, material=mat, reference_vector=(0,0,1))
    analysis = StaticAnalysis(nodes, elements)
    analysis.time_step  = 1.0
    analysis.final_time = 1.0

    def user_force_load(self):
        n_nodes = self.get_number_of_nodes()
        Q = np.zeros((6, n_nodes))
        Q[0,-1] = -200.
        Q[1,-1] = P
        Q[2,-1] = P
        return Q

    analysis.degrees_of_freedom[-1][:6,0] = False  # [current time, dof 0 through 5, node 0]
    analysis.force_load = functools.partial(user_force_load, analysis)
    return analysis

def case2():
    mat = {
        'area':             20.0,
        'elastic_modulus':   1.0,
        'shear_modulus':    10.0,
        'inertia_primary':   2.0,
        'inertia_secondary': 1.0,
        'inertia_torsion':   1.0
    }

    (nodes, elements) = mesh.line_mesh(A=(0,0,0), B=(1,0,0), n_elements=5, order=1, material=mat, reference_vector=(0,0,1))
    domain = StaticAnalysis(nodes, elements)
    domain.time_step = 1.0
    domain.final_time = 1.0

    def user_displacement_load(self):
        n_nodes = self.get_number_of_nodes()
        Q = np.zeros((6, n_nodes))
        Q[2,-1] = 0.5
        return Q

    domain.degrees_of_freedom[-1][:6,0] = False  # [current time, dof 0 through 5, node 0]
    domain.degrees_of_freedom[-1][:6,-1] = False  # [current time, dof 0 through 5 , last node]

    domain.displacement_load = functools.partial(user_displacement_load, domain)

    return domain

def case3():
    mat = {
        'area':              1.0,
        'elastic_modulus':   1.0,
        'shear_modulus':     1.0,
        'inertia_primary':   2.0,
        'inertia_secondary': 1.0,
        'inertia_torsion':   1.0,
    }

    (nodes, elements) = mesh.line_mesh(A=(0,0,0), B=(1,0,0), n_elements=5, order=2, material=mat, reference_vector=(0,0,1))
    #(nodes, elements) = mesh.line_mesh(A=(0,0,0), B=(0.8,0.6,0), n_elements=5, order=1, material=mat, reference_vector=(0,0,1))
    analysis = StaticAnalysis(nodes, elements)
    analysis.time_step = 1.0
    analysis.final_time = 1.0

    def user_force_load(self):
        n_nodes = self.get_number_of_nodes()
        Q = np.zeros((6, n_nodes))
        Q[4,-1] = 8*np.pi
        Q[1,-1] = 0.5
        # Q[4,-1] = 8*0.8*np.pi
        # Q[5,-1] =-8*0.6*np.pi
        return Q

    analysis.degrees_of_freedom[-1][:6,0] = False  # [current time, dof 0 through 5, node 0]

    analysis.force_load = functools.partial(user_force_load, analysis)

    return analysis



def main(n="3"):
    if len(sys.argv) > 1: n = sys.argv[1]
    cases = {"1": case1, "2": case2, "3": case3, "4": lambda: case1(1.)}
    domain = cases[n]()
    domain.solve()
    print(domain.displacement[-1][:,-1])

    for i in range(len(domain.time[:])):
        postproc.line_plot(domain, (0.,12.), (-0.7,0.7), (-0.7,0.7), i)

    import matplotlib.pyplot as plt
    plt.show()


if __name__ == "__main__":
    main()

