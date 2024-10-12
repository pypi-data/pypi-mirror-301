import numpy as np
import matplotlib.pyplot as plt
import contact

def line_plot(domain, xlim, ylim, zlim, time_step, include_initial_state=True, savefig=False, ax=None, no_show=True, label=False):
    i = time_step
    beams_id = contact.identify_entities(domain.elements)
    beams = []
    for beam_id in beams_id:
        beam = []
        for e_id in beam_id:
            beam.append(domain.elements[e_id])
        beams.append(beam)

    color_map = plt.get_cmap("tab10")

    if ax is None:
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_title('Time ' + str(domain.time[i]))
        no_ax = True
    else:
        fig = ax.figure
        no_ax = False

    n_plot_points_for_each_element = 20

    for (b, beam) in enumerate(beams):
        nodes = contact.collect_nodes(beam)

        x0 = domain.coordinates[0][nodes]
        y0 = domain.coordinates[1][nodes]
        z0 = domain.coordinates[2][nodes]
        if include_initial_state:
            ax.plot3D(x0, y0, z0, '.', color=color_map(b))

        u0 = x0 + domain.displacement[i][0][nodes]
        v0 = y0 + domain.displacement[i][1][nodes]
        w0 = z0 + domain.displacement[i][2][nodes]
        ax.plot3D(u0, v0, w0, '.', color=color_map(b))

        for ele in beam:
            N = ele.interp[0](np.linspace(-1,1,n_plot_points_for_each_element))
            x = domain.coordinates[:,ele.nodes] @ N
            if include_initial_state:
                ax.plot3D(x[0], x[1], x[2], '--', color=color_map(b), alpha=0.5)
            u = x + domain.displacement[i][:,ele.nodes] @ N
            ax.plot3D(u[0], u[1], u[2], '-', color=color_map(b), alpha=0.5)
            # ax.plot3D(u[0], u[1], u[2], '-', linewidth=6.0, color=color_map(b), alpha=0.5)

    if no_ax:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)

    if savefig:
        plt.savefig('image'+str(time_step)+'.png')
    elif not no_show:
        plt.show()

    return ax


def energy_plot(domain):
    t = np.array(domain.time)
    ek = np.array(domain.kinetic_energy)
    ep = np.array(domain.potential_energy)
    e = ek + ep
    fig = plt.figure()
    ax = plt.axes()
    ax.set_title('Energy plot')
    ax.plot(t, ek, '.-', label='Kinetic energy')
    ax.plot(t, ep, '.-', label='Potential energy')
    ax.plot(t, e, '.-', label='Total energy')
    plt.show()

