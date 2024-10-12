import numpy as np
import section as sect
import mathematics as math
import interpolation as intp
import conversions as conv

from pandas import DataFrame as df

class Element:
    def __init__(self, nodes, local_dof):
        self.nodes = np.array(nodes)
        self.n_nodes = len(self.nodes)
        self.dof = np.array(local_dof)

    def construct_assembly_matrix(self, n_nodes_in_mesh):
        n_all = len(self.dof)
        n_loc = np.sum(self.dof)
        N = n_all * n_nodes_in_mesh
        self.assemb = np.zeros(shape=(N,n_loc*self.n_nodes))
        for i in range(self.n_nodes):
            self.assemb[:,n_loc*i:n_loc*(i+1)] += assembly_matrix(
                node=self.nodes[i],
                local_dof=self.dof,
                n_nodes_in_mesh=n_nodes_in_mesh
            )


class SimoBeam(Element):
    def __init__(
        self,
        nodes, ndf: int,
        yornt: np.ndarray,
        coordinates: np.ndarray,
        distributed_load: np.ndarray = np.zeros(6),
        **section
    ):
        # --------------------------------------------------------------
        # nodes
        ndf = 6
        dof = np.zeros(ndf, dtype=np.bool)
        dof[:6] = True
        super().__init__(nodes, dof)

        # --------------------------------------------------------------
        # displacement interpolation
        Ndis = self.interp = [
            lambda x: intp.lagrange_polynomial(self.n_nodes-1, x),
            lambda x: intp.lagrange_polynomial_derivative(self.n_nodes-1, x),
            lambda x: intp.lagrange_polynomial_2_derivative(self.n_nodes-1, x),
            lambda x: intp.lagrange_polynomial_3_derivative(self.n_nodes-1, x)
        ]

        # rotation interpolation
        Nrot = [
            lambda x: intp.lagrange_polynomial(self.n_nodes-1, x),
            lambda x: intp.lagrange_polynomial_derivative(self.n_nodes-1, x),
            lambda x: intp.lagrange_polynomial_2_derivative(self.n_nodes-1, x),
            lambda x: intp.lagrange_polynomial_3_derivative(self.n_nodes-1, x)
        ]

        # integration points
        lgf = np.polynomial.legendre.leggauss(self.n_nodes)
        lgr = np.polynomial.legendre.leggauss(self.n_nodes - 1)

        self.gauss = [
            sect.SectionKinematics(
                displacement_interpolation=Ndis,
                rotation_interpolation=Nrot,
                points_location=lgf[0],
                weights=lgf[1]
            ),
            sect.SectionKinematics(
                displacement_interpolation=Ndis,
                rotation_interpolation=Nrot,
                points_location=lgr[0],
                weights=lgr[1]
            )
        ]

        # Interpolation derivatives need to be corrected for
        #  isoparametric formulation (inverse of jacobian). This is
        #  done, when the element length is computed.

        # --------------------------------------------------------------
        # initial element length
        dxds = coordinates @ self.gauss[1].dN_displacement
        intg = np.zeros(3)
        for i in range(len(intg)):
            intg[i] = np.dot(dxds[i], self.gauss[1].wgt)
        L = np.linalg.norm(intg)
        self.jacobian = L / 2

        # --------------------------------------------------------------
        # initial rotation
        for i in range(len(self.gauss)):
            self.gauss[i].rot = np.zeros((3,4,self.gauss[i].n_pts))
            dx = 1/self.jacobian * coordinates @ self.gauss[i].dN_displacement
            for g in range(self.gauss[i].n_pts):
                rotmat = np.zeros(shape=(3,3))
                rotmat[:,0] = math.normalized(dx[:,g])
                rotmat[:,1] = math.normalized(np.cross(yornt, rotmat[:,0]))
                rotmat[:,2] = np.cross(rotmat[:,0], rotmat[:,1])
                self.gauss[i].rot[:,:,g] = math.rotmat_to_quat(rotmat)

        # --------------------------------------------------------------
        # interpolate load
        self.gauss[1].om[2] = np.zeros(shape=(3,self.gauss[1].n_pts))
        self.gauss[1].q[2] = np.tile(distributed_load,reps=(self.gauss[1].n_pts,1)).T

        # --------------------------------------------------------------
        # element properties
        self.prop = sect.ElasticCrossSection(length=L, **section)

    def disp_shape_fun(int_points_locations):
        return intp.lagrange_polynomial(self.n_nodes-1, int_points_locations)

    def commit(self, frm, dst, var="qrof"):
        if "q" in var:
            self.gauss[1].q[dst] = self.gauss[1].q[frm]
        if "r" in var:
            for i in range(len(self.gauss)):
                self.gauss[i].rot[dst] = self.gauss[i].rot[frm]
        if "o" in var:
            self.gauss[1].om[dst] = self.gauss[1].om[frm]
        if "f" in var:
            self.gauss[1].f[dst] = self.gauss[1].f[frm]


    def update(self, x, du, dt, iter0 = False):
        if iter0:
            self.commit(2, 1)
        else:
            self.commit(2, 1, "r")

        state = self.gauss[1]

        E1  = np.array([1, 0, 0])
        dx  = 1 / self.jacobian * x @ state.dN_displacement
        th  = du @ state.N_rotation
        dth = 1 / self.jacobian * du @ state.dN_rotation

        for g in range(state.n_pts):
            dq = math.rotvec_to_quat(th[:,g])
            #dq = conv.ax2qu(th[:,g])
            state.rot[2,:,g] = math.hamp(dq, state.rot[2,:,g])

            state.om[2,:,g]  = curvature_update(state.om[2,:,g], th[:,g], dth[:,g])

            #
            # Strain
            #
            Gamma = math.rotate(
                math.conjugate_quat(state.rot[2,:,g]),
                dx[:,g]
            ) - E1
            kappa = math.rotate(
                math.conjugate_quat(state.rot[2,:,g]),
                state.om[2,:,g]
            )

            #
            # Stress
            #
            fnm = self.prop.getTrialResponse([*Gamma, *kappa])
            fn,fm = fnm[:3], fnm[3:]

            #
            # Push-forward resultants
            #
            state.f[2,:3,g] = math.rotate(state.rot[2,:,g], fn)
            state.f[2,3:,g] = math.rotate(state.rot[2,:,g], fm)

    def residual(self, x: np.ndarray) -> np.ndarray:
        dx = 1 / self.jacobian * x @ self.gauss[1].dN_displacement
        r = np.zeros(shape=(6*self.n_nodes))
        for g in range(self.gauss[1].n_pts):
            # internal distributed forces
            for i in range(self.n_nodes):
                Xi_i = Xi_mat(
                    dx[:,g],
                    1 / self.jacobian * self.gauss[1].dN_displacement[i,g],
                    self.gauss[1].N_rotation[i,g],
                    1 / self.jacobian * self.gauss[1].dN_rotation[i,g]
                )
                r[6*i:6*(i+1)] += Xi_i @ self.gauss[1].f[2,:,g] * self.gauss[1].wgt[g]

                # external distributed forces
                r[6*i:6*i+3] -= self.gauss[1].N_displacement[i,g] * self.gauss[1].q[2,:3,g]
                r[6*i+3:6*(i+1)] -= self.gauss[1].N_rotation[i,g] * self.gauss[1].q[2,3:,g]

        return self.jacobian * r

    def stiffness_matrix(self, x: np.ndarray) -> np.ndarray:
        dx = 1 / self.jacobian * x @ self.gauss[1].dN_displacement
        K = np.zeros(shape=(6*self.n_nodes, 6*self.n_nodes))

        # Material part
        # --------------------------------------------------------------
        for g in range(self.gauss[1].n_pts):
            c = np.zeros((6,6))
            q = self.gauss[1].rot[2,:,g]
            c[:3,:3] = math.rotate2(q, math.rotate2(q, self.prop.C[:3,:3]).T)
            c[3:,3:] = math.rotate2(q, math.rotate2(q, self.prop.C[3:,3:]).T)

            for i in range(self.n_nodes):
                Xi_i = Xi_mat(
                    dx[:,g],
                    1 / self.jacobian * self.gauss[1].dN_displacement[i,g],
                    self.gauss[1].N_rotation[i,g],
                    1 / self.jacobian * self.gauss[1].dN_rotation[i,g]
                )
                for j in range(self.n_nodes):
                    Xi_j = Xi_mat(
                        dx[:,g],
                        1 / self.jacobian * self.gauss[1].dN_displacement[j,g],
                        self.gauss[1].N_rotation[j,g],
                        1 / self.jacobian * self.gauss[1].dN_rotation[j,g]
                    )
                    K[6*i:6*(i+1), 6*j:6*(j+1)] += self.gauss[1].wgt[g] * Xi_i @ c @ Xi_j.T


        # Geometric part
        # --------------------------------------------------------------
        for g in range(self.gauss[1].n_pts):
            for i in range(self.n_nodes):
                for j in range(self.n_nodes):
                    G = np.zeros((6,6))
                    G[:3,3:] = (
                        -math.skew(self.gauss[1].f[2,:3,g]) *
                        1 / self.jacobian * self.gauss[1].dN_displacement[i,g] *
                        self.gauss[1].N_rotation[j,g]
                    )
                    G[3:,:3] = (
                        math.skew(self.gauss[1].f[2,:3,g]) *
                        1 / self.jacobian * self.gauss[1].dN_displacement[j,g] *
                        self.gauss[1].N_rotation[i,g]
                    )
                    G[3:,3:] = (
                        -math.skew(self.gauss[1].f[2,3:,g]) *
                        1 / self.jacobian * self.gauss[1].dN_rotation[i,g] *
                        self.gauss[1].N_rotation[j,g] +
                        math.skew(dx[:,g]) @ math.skew(self.gauss[1].f[2,:3,g]) *
                        self.gauss[1].N_rotation[i,g] * self.gauss[1].N_rotation[j,g]
                    )
                    K[6*i:6*(i+1), 6*j:6*(j+1)] += self.gauss[1].wgt[g] * G


        return self.jacobian * K

    def follower_matrix(self) -> np.ndarray:
        K = np.zeros(shape=(6*self.n_nodes,6*self.n_nodes))
        return K

    def follower_residual(self) -> np.ndarray:
        R = np.zeros(shape=(6*self.n_nodes))
        return R

    def compute_momentum(self, X, V):
        p = np.zeros(6)
        x = X @ self.gauss[0].N_displacement
        v = V @ self.gauss[0].N_displacement
        p_linear = self.jacobian * self.prop.Arho * v @ self.gauss[0].wgt

        p_angular = np.zeros(3)
        for g in range(self.gauss[0].n_pts):
            p_angular += self.jacobian * self.gauss[0].wgt[g] * (
                np.cross(x[:,g], self.prop.Arho * v[:,g]) #+
#               math.rotate(self.gauss[0].rot[2,:,g], self.prop.Irho @ self.gauss[0].w[2,:,g])
            )

        p[:3]  = p_linear
        p[3:6] = p_angular
        return p

    def compute_kinetic_energy(self, V):
        ek = 0.0
        v = V @ self.gauss[0].N_displacement
        for g in range(self.gauss[0].n_pts):
            ek += 1/2 * self.jacobian * self.gauss[0].wgt[g] * (
                self.prop.Arho * v[:,g] @ v[:,g] #+ 
#               self.gauss[0].w[2,:,g] @ self.prop.Irho @ self.gauss[0].w[2,:,g]
            )
        return ek

    def compute_potential_energy(self, X):
        ep = 0.0
        dx = 1 / self.jacobian * X @ self.gauss[1].dN_displacement
        E1 = np.array([1.0, 0.0, 0.0])
        Cn = self.prop.C[:3,:3]
        Cm = self.prop.C[3:,3:]
        for g in range(self.gauss[1].n_pts):
            Gamma = math.rotate(math.conjugate_quat(self.gauss[1].rot[2,:,g]), dx[:,g]) - E1
            kappa = math.rotate(math.conjugate_quat(self.gauss[1].rot[2,:,g]), self.gauss[1].om[2,:,g])
            ep += 1/2 * self.jacobian * self.gauss[1].wgt[g] * (
                Gamma @ Cn @ Gamma + kappa @ Cm @ kappa
            )
        return ep



def Xi_mat(
    dx: np.ndarray,
    dN_displacement: float,
    N_rotation: float,
    dN_rotation: float
) -> np.ndarray:
    Xi = np.identity(6)
    Xi[:3] *= dN_displacement
    Xi[3:] *= dN_rotation
    Xi[3:,:3] = - N_rotation * math.skew(dx)
    return Xi

def assembly_matrix(
    node: int,
    local_dof: np.ndarray,
    n_nodes_in_mesh: int
) -> np.ndarray:

    n_loc = np.sum(local_dof)
    n_all = len(local_dof)
    N = n_all * n_nodes_in_mesh
    A = np.zeros((N,n_loc))
    for j in range(n_loc): A[node*n_all+j,j] = 1

    return A

def curvature_update(curv, th, dth):

    ang = np.linalg.norm(th)

    if ang == 0.0:
        return curv + dth

    else:
        return (
            np.sin(ang)/ang * dth +
            (1 - np.sin(ang)/ang) * np.dot(th, dth)/ang**2 * th +
            (1 - np.cos(ang))/ang**2 * np.cross(th, dth) + np.cos(ang)*curv +
            (1 - np.cos(ang))/ang**2 * np.dot(th, curv)*th + np.sin(ang)/ang * np.cross(th,curv)
        )

