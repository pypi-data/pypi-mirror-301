import numpy as np
import cmp_elements as elmt


def _node_id(ele_id, n_nodes_per_ele):
    return np.array([
        n_nodes_per_ele*ele_id+j for j in range(n_nodes_per_ele+1)
    ], dtype=int)

def line_mesh(A, B, n_elements, order, material, reference_vector, starting_node_index=0,
#              consider_contact_jacobian=False, dual_basis_functions=True, n_contact_integration_points=None
):
    """
    Create line mesh from coordinate A to B.
    """
    n_ele = n_elements
    n_nod = order * n_ele + 1

    coordinates = np.zeros((3,n_nod))
    for i in range(3):
        coordinates[i,:] = np.linspace(A[i], B[i], n_nod)

    beam = []
    for i in range(n_ele):
        element = elmt.SimoBeam(
            nodes=starting_node_index+_node_id(i, order),
            ndf=7,
            yornt=reference_vector,
            coordinates=coordinates[:,_node_id(i, order)],
            **material
        )
        beam.append(element)
    return (coordinates, beam)

def n_point_mesh(points, n_elements, order, material,
        reference_vector, starting_node_index=0
#       consider_contact_jacobian=False,
#       dual_basis_functions=True
        ):
    """
    Create a mesh from a list of points by connecting them in a sequence
    (P1 -- P2 -- P3 -- ... -- PN).

    # Parameters:
    points ...................... points in 3D
    n_elements .................. a list containing the number of elements for each segment
    order ....................... element order (polynomial interpolation order)
    material .................... dictionary with material properties
    reference_vector ............ a vector to define the orientation of the cross-section
    dual_basis_functions ........ a boolean saying if the Lagrange multiplier field should be interpolated with dual shape functions or with Lagrange polynomials
    """

    assert points.shape[1] == len(n_elements) + 1, 'Number of points should be one greater then the length of n_elements list.'
    n_ele = np.array(n_elements)
    n_nod = order * np.sum(n_ele) + 1
    coordinates = np.zeros((3,n_nod))
    for i in range(len(n_ele)):
        n1 = order*np.sum(n_ele[:i])
        n2 = order*np.sum(n_ele[:i])+order*n_ele[i]
        for j in range(n1, n2):
            for k in range(3):
                coordinates[k,j] = points[k,i] + (points[k,i+1] - points[k,i]) * (j - n1) / (n2 - n1)
    coordinates[:,-1] = points[:,-1]

    beam = []
    for i in range(np.sum(n_ele)):
        element = elmt.SimoBeam(
            nodes=starting_node_index+_node_id(i, order),
            ndf=7,
            yornt=reference_vector,
            coordinates=coordinates[:,_node_id(i, order)],
            **material
        )
        beam.append(element)
    return (coordinates, beam)
