import numpy as np
from typing import Callable
import interpolation as intp
from errors import ConvergenceError

import contact
import matplotlib.pyplot as plt
import postprocessing as postproc

class StaticAnalysis:
    def __init__(self, coordinates, elements):
        ndf = 6
        self.coordinates = coordinates
        self.elements = elements
        for ele in self.elements:
            ele.construct_assembly_matrix(self.coordinates.shape[1])
        self.degrees_of_freedom = [np.ones((ndf,coordinates.shape[1]), dtype=np.bool)]

        # Constructing a vector of unknowns for the solver A.x = b
        self.unknowns = np.zeros_like(self.degrees_of_freedom[0], dtype=np.float)

        # Constructing matrices of physical fields
        n_nodes = self.coordinates.shape[1]
        self.displacement = [np.zeros((3,n_nodes))]

        # Initiating time
        self.time_step = 1.0
        self.time = [0.0]
        self.current_time = self.time[0]
        self.final_time = 1.0
        self.time_splitting = False

        # Invariants
        self.potential_energy = [self.compute_potential_energy()]

        # Select solver parameters
        self.max_number_of_time_steps = 100
        self.max_number_of_newton_iterations = 60
        self.tolerance = 1e-8
        self.beta = 0.25
        self.gamma = 0.5

        # Other parameters
        self.verbose = True

    def get_number_of_nodes(self):
        return self.coordinates.shape[1]
    def get_number_of_elements(self):
        return len(self.elements)
    def get_number_of_degrees_of_freedom_per_node(self):
        return self.degrees_of_freedom[-1].shape[0]
    def get_number_of_all_degrees_of_freedom(self):
        return len(self.degrees_of_freedom[-1].flatten(order='F'))

    def force_load(self):
        n_nodes = self.get_number_of_nodes()
        return np.zeros((6, n_nodes))

    def distributed_force_load(self):
        q = [np.zeros((6, ele.gauss[1].n_pts)) for ele in self.elements]
        return q

    def follower_force_load(self):
        n_nodes = self.get_number_of_nodes()
        return np.zeros((6, n_nodes))

    def displacement_load(self):
        n_nodes = self.get_number_of_nodes()
        return np.zeros((6, n_nodes))

    def equilibriate(self):
        c = np.array([1.0, 0.0, 0.0])
        n_dof = self.get_number_of_all_degrees_of_freedom()
        n_ndof = self.get_number_of_degrees_of_freedom_per_node()
        n_nodes = self.get_number_of_nodes()
        n_ele = self.get_number_of_elements()

        du = self.unknowns
        R = np.zeros(du.shape)
        # Apply displacement load
        du[:6] = self.displacement_load()
        tangent = np.zeros((n_dof, n_dof))

        # Perform Newton-Raphson iteration method to find new balance
        for i in range(self.max_number_of_newton_iterations):
            # Initiate new iteration
            self.__displacement[1] = self.__displacement[2]

            #R[:] = 0.0

            # External forces
            R[:6] = self.force_load()

            # Update nodal values
            self.__displacement[2] += du[:3]

        
            # Resisting forces
            Q0 = self.distributed_force_load()
            for e, ele in enumerate(self.elements):
                ele.commit(2, 1, "q")

                # Update integration point beam values
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                ele.update(X, du[3:6,ele.nodes], self.time_step, iter0=(i == 0))

                ele.gauss[1].q[2] = Q0[e]
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                r = ele.stiffness_residual(X)
                A = ele.assemb
                R -= (A @ r).reshape((n_ndof, n_nodes), order='F')


            res_norm = np.linalg.norm(R[:6][self.__degrees_of_freedom[2][:6]])
            if self.verbose: print("\tResidual", res_norm)
            if res_norm <= self.tolerance:
                break

            # Assembly of tangent matrix from all elements.
            tangent[:] = 0.0
            for ele in self.elements:
                A = ele.assemb
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                S = ele.stiffness_matrix(X)
                tangent += A @ S @ A.T

            # Solve system of equations by condensing inactive dofs
            mask = self.__degrees_of_freedom[2].flatten(order='F')
            R_flat = R.flatten(order='F')
            du_flat = du.flatten(order='F')
            du_flat[mask] = np.linalg.solve(tangent[mask][:,mask], R_flat[mask])
            du_flat[~mask] = 0.0
            du[:] = du_flat.reshape((n_ndof,n_nodes), order='F')


        else:
            raise ConvergenceError('Newton-Raphson: Maximum number of iterations reached without convergence.')

    def __newton_loop(self):
        c = np.array([1.0, 0.0, 0.0])
        n_dof = self.get_number_of_all_degrees_of_freedom()
        n_ndof = self.get_number_of_degrees_of_freedom_per_node()
        n_nodes = self.get_number_of_nodes()
        n_ele = self.get_number_of_elements()

        # Apply displacement load
        x = self.unknowns
        x[:] = 0.0
        x[:6] = self.displacement_load()

        # Perform Newton-Raphson iteration method to find new balance
        for i in range(self.max_number_of_newton_iterations):
            # Initiate new iteration
            self.__displacement[1] = self.__displacement[2]
            for ele in self.elements:
                ele.gauss[1].q[1] = ele.gauss[1].q[2]

            # In iteration 0 discover the current state of the system,
            #  therefore skip the computation of displacements.
            if i > 0:
                # Assembly of tangent matrix from all elements.
                tangent = np.zeros((n_dof, n_dof))
                for ele in self.elements:
                    A = ele.assemb

                    # Static contribution
                    X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                    S = c[0] * ele.stiffness_matrix(X)

                    # Dynamic contribution
#                   if c[2] != 0:
#                       S += c[2] * ele.mass_matrix(self.time_step, self.beta, self.gamma)

                    # Follower load contributions
                    # ---
                    tangent += A @ S @ A.T

                # Solve system of equations by condensing inactive dofs
                mask = self.__degrees_of_freedom[2].flatten(order='F')
                x_flat = x.flatten(order='F')
                x_flat[mask] = np.linalg.solve(tangent[mask][:,mask], x_flat[mask])
                x_flat[~mask] = 0.0
                x = x_flat.reshape((n_ndof,n_nodes), order='F')

            # Update nodal beam values
            self.__displacement[2] += x[:3]

            # Update integration point beam values
            for ele in self.elements:
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                ele.update(X, x[3:6,ele.nodes], self.time_step, iter0=(i == 0))


            # Displacement convergence
            if self.convergence_test_type == "DSP" and i > 0:
                if self.verbose: print("Displacement", np.linalg.norm(x[:3]))
                if np.linalg.norm(x[:3]) <= self.tolerance:
                    if self.verbose: print("Time step converged in", i+1, "iterations.")
                    break

            # Reset x
            x[:] = 0.0

            # External forces
            x[:6] = self.force_load()
            Q0 = self.distributed_force_load()
            for (e, ele) in enumerate(self.elements):
                ele.gauss[1].q[2] = Q0[e] 

            for ele in self.elements:
                # Internal forces
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                R = ele.stiffness_residual(X)
#               if c[2] != 0:
#                   R += ele.mass_residual(self.__acceleration[2][:,ele.nodes])
                A = ele.assemb
                x -= (A @ R).reshape((n_ndof, n_nodes), order='F')


            # Residual convergence
            if i == 0:
                res_norm = np.linalg.norm(x[self.__degrees_of_freedom[2]])
            else:
                res_norm = np.linalg.norm(x[:6][self.__degrees_of_freedom[2][:6]])
            if self.convergence_test_type == "RES":
                if self.verbose: print("Residual", res_norm)
                if res_norm <= self.tolerance:
                    if self.verbose: print("\tTime step converged within", i+1, "iterations.\n")
                    break

        else:
            raise ConvergenceError('Newton-Raphson: Maximum number of iterations reached without convergence.')

    def __time_loop(self):
        # Start of time loop
        for n in range(self.max_number_of_time_steps):
            if self.verbose: print("Time step: ", n+1, " (time ", self.current_time, " -> ", self.current_time + self.time_step, ")", sep='')

            self.current_time += self.time_step
            self.__displacement[0] = self.__displacement[2]
            self.__degrees_of_freedom[0] = self.__degrees_of_freedom[2]
            for elem in self.elements:
                elem.commit(2, 0)
#               ele.gauss[0].w[0] = ele.gauss[0].w[2]
#               ele.gauss[0].a[0] = ele.gauss[0].a[2]
                # ele.gauss[0].rot[0] = ele.gauss[0].rot[2]
                # ele.gauss[1].rot[0] = ele.gauss[1].rot[2]
                # ele.gauss[1].om[0] = ele.gauss[1].om[2]
                # ele.gauss[1].q[0] = ele.gauss[1].q[2]
                # ele.gauss[1].f[0] = ele.gauss[1].f[2]

            if self.time_splitting:
                split_time_step_size_counter = 0
                original_time_step = self.time_step
                while True:
                    try:
                        #self.__newton_loop()
                        self.equilibriate()
                        break
                    except ConvergenceError:
                        if self.verbose: print('\n\tNo convergence, automatic time step split.')
                        self.current_time -= self.time_step
                        self.time_step = self.time_step / 2
                        self.__displacement[2] = self.__displacement[0]
                        self.__degrees_of_freedom[2] = self.__degrees_of_freedom[0]
                        for elem in self.elements:
                            elem.commit(0, 2)
                            # ele.gauss[0].rot[2] = ele.gauss[0].rot[0]
                            # ele.gauss[1].om[2] = ele.gauss[1].om[0]
                            # ele.gauss[1].q[2] = ele.gauss[1].q[0]
                            # ele.gauss[1].f[2] = ele.gauss[1].f[0]
                            # ele.gauss[1].rot[2] = ele.gauss[1].rot[0]

                    split_time_step_size_counter += 1
                    if split_time_step_size_counter > 5:
                        raise ConvergenceError('Splitting time step did not help')

                self.time_step = original_time_step
            else:
                #self.__newton_loop()
                self.equilibriate()

            self.displacement.append(self.__displacement[2].copy())
            self.time.append(self.current_time)
            self.potential_energy.append(self.compute_potential_energy())

            if self.current_time >= self.final_time:
                if self.verbose: print("Computation is finished, reached the end of time.")
                break

    def compute_potential_energy(self):
        ep = 0.0
        for ele in self.elements:
            ep += ele.compute_potential_energy(X=self.coordinates[:, ele.nodes] + self.displacement[-1][:,ele.nodes])
        return ep

    def solve(self):
        if self.verbose:
            print("Beginning static solve.")
        self.__degrees_of_freedom = np.array([self.degrees_of_freedom[-1]]*3)
        self.__displacement = np.array([self.displacement[-1]]*3)
        self.__time_loop()

class System(StaticAnalysis):
    def __init__(self, coordinates, elements):
        # Mesh
        assert coordinates.shape[0] == 3, 'Only three-dimensional systems are currently supported.'
        self.coordinates = coordinates
        self.elements = elements
        for ele in self.elements:
            ele.construct_assembly_matrix(self.coordinates.shape[1])
        self.degrees_of_freedom = [np.ones((7,coordinates.shape[1]), dtype=np.bool)]
        self.degrees_of_freedom[0][6,:] = False  # defualt - no contact at the beginning

        # Constructing a vector of unknowns for the solver A.x = b
        self.unknowns = np.zeros_like(self.degrees_of_freedom[0], dtype=np.float)

        # Constructing matrices of physical fields
        n_nodes = self.coordinates.shape[1]
        self.displacement = [np.zeros((3,n_nodes))]
        self.velocity = [np.zeros((3,n_nodes))]
        self.acceleration = [np.zeros((3,n_nodes))]
        self.lagrange = [np.zeros(n_nodes)]

        # Initiating time
        self.time_step = 1.0
        self.time = [0.0]
        self.current_time = self.time[0]
        self.final_time = 1.0
        self.time_splitting = False

        # Invariants
        self.momentum = [self.compute_momentum()]
        self.kinetic_energy = [self.compute_kinetic_energy()]
        self.potential_energy = [self.compute_potential_energy()]

        # Select solver parameters
        self.max_number_of_time_steps = 100
        self.max_number_of_newton_iterations = 60
        self.max_number_of_contact_iterations = 10
        self.tolerance = 1e-8
        self.convergence_test_type = "RES"  # options: "RES" - force residual, "DSP" - displacement, "ENE" - energy
        self.solver_type = "dynamic"  # options: "dynamic", "static"
        self.dynamic_solver_type = "Newmark-beta method"  # options: "Newmark-beta method", "Generalized-alpha method"
        self.beta = 0.25
        self.gamma = 0.5
        self.contact_detection = True

        # Other parameters
        self.verbose = True
        self.print_residual = False

    def get_number_of_nodes(self):
        return self.coordinates.shape[1]
    def get_number_of_elements(self):
        return len(self.elements)
    def get_number_of_degrees_of_freedom_per_node(self):
        return self.degrees_of_freedom[-1].shape[0]
    def get_number_of_all_degrees_of_freedom(self):
        return len(self.degrees_of_freedom[-1].flatten(order='F'))
    def get_matrix_multipliers(self):
        if self.solver_type == 'static':
            return np.array([1.0, 0.0, 0.0])
        elif self.solver_type == 'dynamic':
            return np.array([1.0, self.gamma/(self.time_step*self.beta), 1/(self.time_step**2*self.beta)])
        else:
            raise Exception('Solver parameter error - only "static" or "dynamic" types are supported for solver_type.')

    def force_load(self):
        n_nodes = self.get_number_of_nodes()
        return np.zeros((6, n_nodes))

    def distributed_force_load(self):
        q = [np.zeros((6, ele.gauss[1].n_pts)) for ele in self.elements]
        return q

    def follower_force_load(self):
        n_nodes = self.get_number_of_nodes()
        return np.zeros((6, n_nodes))

    def displacement_load(self):
        n_nodes = self.get_number_of_nodes()
        return np.zeros((6, n_nodes))

    def __newton_loop(self):
        c = self.get_matrix_multipliers()
        n_dof = self.get_number_of_all_degrees_of_freedom()
        n_ndof = self.get_number_of_degrees_of_freedom_per_node()
        n_nodes = self.get_number_of_nodes()
        n_ele = self.get_number_of_elements()

        # Apply displacement load
        x = self.unknowns
        x[:] = 0.0
        x[:6] = self.displacement_load()

        # Perform Newton-Raphson iteration method to find new balance
        for i in range(self.max_number_of_newton_iterations):
            # Initiate new iteration
            self.__displacement[1] = self.__displacement[2]
            self.__velocity[1] = self.__velocity[2]
            self.__acceleration[1] = self.__acceleration[2]
            self.__lagrange[1] = self.__lagrange[2]
            for ele in self.elements:
                ele.gauss[1].q[1] = ele.gauss[1].q[2]

            # In iteration 0 discover the current state of the system,
            #  therefore skip the computation of displacements.
            if i > 0:
                # Assembly of tangent matrix from all elements.
                tangent = np.zeros((n_dof, n_dof))
                for ele in self.elements:
                    A = ele.assemb

                    # Static contribution
                    X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                    S = c[0] * ele.stiffness_matrix(X)

                    # Dynamic contribution
                    if c[2] != 0:
                        S += c[2] * ele.mass_matrix(self.time_step, self.beta, self.gamma)

                    # Follower load contributions
                    # ---

                    tangent += A @ S @ A.T
                    # Contact contribution
                    try:
                        contact_element = ele.child
                        tangent += c[0] * contact_element.contact_tangent(self.coordinates+self.__displacement[2], self.__lagrange[2], n_nodes)
                        mask = self.__degrees_of_freedom[2].flatten(order='F')
                    except AttributeError:
                        pass

                # Solve system of equations by condensing inactive dofs
                mask = self.__degrees_of_freedom[2].flatten(order='F')
                x_flat = x.flatten(order='F')
                x_flat[mask] = np.linalg.solve(tangent[mask][:,mask], x_flat[mask])
                x_flat[~mask] = 0.0
                x = x_flat.reshape((n_ndof,n_nodes), order='F')

            # Update nodal beam values
            self.__displacement[2] += x[:3]
            if i == 0:
                a_new = (
                    (1 - 0.5/self.beta) * self.__acceleration[2] -
                    1/(self.time_step*self.beta) * self.__velocity[2]
                )
                self.__velocity[2] += self.time_step * (
                    (1 - self.gamma) * self.__acceleration[2] +
                    self.gamma * a_new
                )
                self.__acceleration[2] = a_new
            else:

                iterative_displacement_change = x[:3]
                self.__velocity[2] += self.gamma / (self.time_step * self.beta) * iterative_displacement_change
                self.__acceleration[2] += 1 / (self.time_step**2 * self.beta) * iterative_displacement_change

            # Update integration point beam values
            for ele in self.elements:
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                ele.update(X, x[3:6,ele.nodes], self.time_step, self.beta, self.gamma, iter0=(i == 0))

            # Update nodal contact values
            self.__lagrange[2] += x[6]

            # Update integration point contact values
            for ele in self.elements:
                try:
                    contact_element = ele.child
                    contact_element.find_gap(self.coordinates+self.__displacement[2])
                except AttributeError:
                    pass

            # Displacement convergence
            if self.convergence_test_type == "DSP" and i > 0:
                if self.verbose and self.print_residual: print("Displacement", np.linalg.norm(x[:3]))
                if np.linalg.norm(x[:3]) <= self.tolerance:
                    if self.verbose: print("Time step converged within", i+1, "iterations.")
                    break

            # Reset x
            x[:] = 0.0

            # External forces
            x[:6] = self.force_load()
            Q0 = self.distributed_force_load()
            for (e, ele) in enumerate(self.elements):
                ele.gauss[1].q[2] = Q0[e]

            for ele in self.elements:
                # Internal forces
                X = self.coordinates[:,ele.nodes] + self.__displacement[2][:,ele.nodes]
                R = ele.stiffness_residual(X)
                if c[2] != 0:
                    R += ele.mass_residual(self.__acceleration[2][:,ele.nodes])
                A = ele.assemb
                x -= (A @ R).reshape((n_ndof, n_nodes), order='F')

                # Contact forces
                try:
                    contact_element = ele.child
                    contact_forces = contact_element.contact_residual(
                        self.coordinates+self.__displacement[2], self.__lagrange[2], n_nodes
                    ).reshape((n_ndof, n_nodes), order='F')
                    x -= contact_forces
                except AttributeError:
                    pass

            # Residual convergence
            if i == 0:
                res_norm = np.linalg.norm(x[self.__degrees_of_freedom[2]])
            else:
                res_norm = np.linalg.norm(x[:6][self.__degrees_of_freedom[2][:6]])
            if self.convergence_test_type == "RES":
                if self.verbose and self.print_residual: print("Residual", res_norm)
                if res_norm <= self.tolerance:
                    # Newton-Raphson algorithm converged to a new solution
                    if self.verbose: print("\tTime step converged within", i+1, "iterations.\n")
                    break

        else:
            raise ConvergenceError('Newton-Raphson: Maximum number of iterations reached without convergence.')


    def __time_loop(self):
        # Start of time loop
        for n in range(self.max_number_of_time_steps):
            if self.verbose: print("Time step: ", n+1, " (time ", self.current_time, " --> ", self.current_time + self.time_step, ")", sep='')

            self.current_time += self.time_step
            self.__displacement[0] = self.__displacement[2]
            self.__velocity[0] = self.__velocity[2]
            self.__acceleration[0] = self.__acceleration[2]
            self.__lagrange[0] = self.__lagrange[2]
            self.__degrees_of_freedom[0] = self.__degrees_of_freedom[2]
            for ele in self.elements:
                ele.gauss[0].rot[0] = ele.gauss[0].rot[2]
                ele.gauss[1].rot[0] = ele.gauss[1].rot[2]
                ele.gauss[1].om[0] = ele.gauss[1].om[2]
                ele.gauss[1].q[0] = ele.gauss[1].q[2]
                ele.gauss[1].f[0] = ele.gauss[1].f[2]

            if self.time_splitting:
                split_time_step_size_counter = 0
                original_time_step = self.time_step
                while True:
                    try:
                        if self.contact_detection:
                            self.__contact_loop()
                        else:
                            self.__newton_loop()
                        break
                    except ConvergenceError:
                        if self.verbose: print('\n\tNo convergence, automatic time step split.')
                        self.current_time -= self.time_step
                        self.time_step = self.time_step / 2
                        self.__displacement[2] = self.__displacement[0]
#                       self.__velocity[2] = self.__velocity[0]
#                       self.__acceleration[2] = self.__acceleration[0]
                        self.__lagrange[2] = self.__lagrange[0]
                        self.__degrees_of_freedom[2] = self.__degrees_of_freedom[0]
                        for ele in self.elements:
                            ele.gauss[0].rot[2] = ele.gauss[0].rot[0]
                            ele.gauss[1].om[2] = ele.gauss[1].om[0]
                            ele.gauss[1].q[2] = ele.gauss[1].q[0]
                            ele.gauss[1].f[2] = ele.gauss[1].f[0]
                            ele.gauss[1].rot[2] = ele.gauss[1].rot[0]

                    split_time_step_size_counter += 1
                    if split_time_step_size_counter > 5:
                        raise ConvergenceError('Splitting time step did not help')

                self.time_step = original_time_step
            else:
                if self.contact_detection:
                    self.__contact_loop()
                else:
                    self.__newton_loop()

            self.displacement.append(self.__displacement[2].copy())
            self.lagrange.append(self.__lagrange[2].copy())
            self.time.append(self.current_time)
            self.kinetic_energy.append(self.compute_kinetic_energy())
            self.potential_energy.append(self.compute_potential_energy())

            if self.current_time >= self.final_time:
                if self.verbose: print("Computation is finished, reached the end of time.")
                break

    def gap_function(self, axis=0):
        """
        Return gap function values along one of the main axes.
        """
        gaps = []
        X = self.coordinates + self.displacement[-1]
        for ele in self.elements:
            try:
                contact_element = ele.child
                for g in range(len(contact_element.gauss)):
                    x = X[axis,ele.nodes] @ contact_element.N_displacement[:,g]
                    y = contact_element.gauss[g].gap
                    gaps.append([x,y])
            except AttributeError:
                continue
        gaps = np.array(gaps)
        return gaps

    def compute_momentum(self):
        p = np.zeros(6)
        for ele in self.elements:
            p += ele.compute_momentum(
                X=self.coordinates[:, ele.nodes] + self.displacement[-1][:,ele.nodes],
                V=self.velocity[-1][:,ele.nodes])
        return p

    def compute_kinetic_energy(self):
        ek = 0.0
        for ele in self.elements:
            ek += ele.compute_kinetic_energy(V=self.velocity[-1][:,ele.nodes])
        return ek

    def compute_potential_energy(self):
        ep = 0.0
        for ele in self.elements:
            ep += ele.compute_potential_energy(X=self.coordinates[:, ele.nodes] + self.displacement[-1][:,ele.nodes])
        return ep

    def solve(self):
        if self.verbose:
            print("Hello, world!\nThis is a FEM program for beam analysis.")
            print("This will be a", self.solver_type, "analysis.")
            if self.solver_type == 'dynamic':
                print("We use", self.dynamic_solver_type + ".")

        self.__degrees_of_freedom = np.array([self.degrees_of_freedom[-1]]*3)
        self.__displacement = np.array([self.displacement[-1]]*3)
        self.__velocity = np.array([self.velocity[-1]]*3)
        self.__acceleration = np.array([self.acceleration[-1]]*3)
        self.__lagrange = np.array([self.lagrange[-1]]*3)
        self.__time_loop()

