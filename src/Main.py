import Simulation

if __name__ == '__init__':

    simulation = Simulation()

    not_done = True

    # run simulation in a loop
    while (not_done):

        simulation.time_step()

        # check if done