"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
========================================================================================================================
COMPSCI 2120A/9642A/ DIGIHUM 2220A - Assignment 2
Student Name: Michael.......
Student Number: No
========================================================================================================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import numpy as np
import networkx as nt
import matplotlib.pyplot as plt


def create_adjacency_matrix(population_size):
    """
    This function creates and returns a randomized population_size x population_size matrix.
    It is an "adjacency" matrix, meaning that it indicates which people are adjacent (in proximity)

    Why use this? The idea: if two people are in proximity, one person can transmit to the other

    How to read it...

    matrix[row 0][column 8] = 1 --> Person 0 is adjacent to Person 8.
    matrix[row 5][column 3] = 0 --> Person 5 is not adjacent to Person 3.

    :param population_size: the given number of people featured in your matrix (and in your system)
    :return: a randomized adjacency matrix of size population_size x population_size
    """

    # create random adjacency matrix with 0's and 1's of size population_size x population_size
    adjacency = np.random.randint(0, 2, (population_size, population_size))

    # cut out entries below diagonal to reduce the number of connections
    adjacency = np.triu(adjacency)

    # create a network from the adjacency matrix
    adjacency_network = nt.from_numpy_matrix(adjacency)

    # if the network is not connected, keep creating random ones until you get one that is connected
    if not (nt.is_connected(adjacency_network)):
        while not (nt.is_connected(adjacency_network)):
            adjacency = np.random.randint(0, 2,
                                          (population_size, population_size))
            adjacency = np.triu(adjacency)
            adjacency_network = nt.from_numpy_matrix(adjacency)

    # fill all person-person connections with value 1 (for each person with themselves)
    np.fill_diagonal(adjacency, 1)

    return adjacency


def create_population_list(population_size):
    """
    This function creates and returns a list of lists; specifically, it creates and returns
    a list containing "people". Each "person" is a 3-element list.. i.e ['Person #', Positive_Flag, List of Others in Proximity]

    Let's break down each "person" list: It contains...
     1) A person # such as 'Person 0'
     2) A positive flag --> True if that person is positive for the virus, False otherwise
     3) A list of others in proximity --> a list, such as [0, 3, 4] which would mean that this person is in proximity to persons
     0, 3, and 4

     The list which we return contains these "person" lists.
     i.e. [['Person 0', False, [0, 1]], ['Person 1', False, [1, 2]], ['Person 2', False, [1, 2]]]

    :param population_size: the number of people who will be in your population
    :return: a list which contains all people and their information (#, positive_flag, list_of_others_in_proximity)
    """

    # create a randomized adjacency matrix for this population
    adjacency = create_adjacency_matrix(population_size)

    population_list = []

    # for each person in your population, create list which contains a 'Person #', a positive flag, and a list of others
    # in proximity
    for i in range(population_size):
        person_name = "Person " + str(i)
        positive_flag = False
        others_in_proximity = adjacency[
            i]  # get row of adjacency matrix for that person to get all others in proximity
        # "np.where(condition)[0]" returns an array of all indexes where the condition is met
        others_in_proximity2 = np.where(others_in_proximity == 1)[0]
        others_in_proximity_list = list(
            others_in_proximity2)  # convert it to a list
        population_list.append([person_name, positive_flag,
                                others_in_proximity_list])  # add person to population list

    return population_list


def draw_network(population_list):
    """
    This function creates and draws a "network" of nodes and edges corresponding to the data from population_list.

    For example, person 0 will be represented by node "0"; the node will be red if they are positive for the virus and
    blue otherwise; the node will be connected to other nodes based on its list of others in proximity

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :return: nothing, but displays the resulting graph in a new window using matplotlib.pyplot
    """

    # these lists store all of the people who have their positive_flag set to True or False, respectively
    positive_case_list = []
    negative_case_list = []

    # initialize our network
    network = nt.Graph()

    # fill positive and negative case lists with people
    for i in range(len(population_list)):
        # if person i's positive_flag is True, add them to the positive_case list; also add their node to the
        # graph in red
        if population_list[i][1]:
            positive_case_list.append(i)
            network.add_node(i, node_color='r')
        # else, if person i's positive_flag is False, add them to the negative_case list; also add their node to the
        # graph in blue
        else:
            negative_case_list.append(i)
            network.add_node(i, node_color='b')

        # add all of the edges between nodes... i.e. for each element j in the list of others in proximity, add a new
        # edge (a line) between person i and person in proximity (j)
        for j in population_list[i][2]:
            network.add_edge(i, j)

    # You can uncomment the lines below to print the running lists of positive and negative cases as a check
    # print("Positive_Cases: ", positive_case_list)
    # print("Negative Cases:", negative_case_list)

    # this creates a randomized layout for the network
    node_layout = nt.random_layout(network)

    # these commands draw our nodes, edges, and labels
    nt.draw_networkx_nodes(network, node_layout, nodelist=positive_case_list,
                           node_color='r')
    nt.draw_networkx_nodes(network, node_layout, nodelist=negative_case_list,
                           node_color='b')
    nt.draw_networkx_edges(network, node_layout)
    nt.draw_networkx_labels(network, node_layout)

    plt.show()
    plt.draw()


def new_positive_case(population_list, person_number):
    # set person to positive
    population_list[person_number][1] = True

    return None


def transmit(population_list, person_number, p_transmission):
    person = population_list[person_number]
    if person[1]:
        # for everyone in proximity of positive person, chance to transmit to them if they're negative
        for person_nearby in person[2]:
            if not population_list[person_nearby][1] and np.random.rand() < p_transmission:
                population_list[person_nearby][1] = True

    return None


def recover(population_list, person_number):
    # set person to negative
    population_list[person_number][1] = False

    return None


def simulate_step(population_list, p_transmission, p_recovery):
    if np.random.rand() < p_transmission:
        # randomly generate integer corresponding to person in population
        unlucky_fellow = np.random.randint(0, len(population_list))
        # make that person positive
        new_positive_case(population_list, unlucky_fellow)

    for person_number, person in enumerate(population_list):
        # if a person is positive, chance to transmit to others
        if person[1]:
            transmit(population_list, person_number, p_transmission)

        # if person is positive, chance for them to recover
        if person[1] and np.random.rand() < p_recovery:
            recover(population_list, person_number)

    return None


def all_cases_positive(population_list):
    for person in population_list:
        if not person[1]:
            # if any single person tests negative, returns false
            return False
    # otherwise, return true
    return True


def simulate_run(population_list, p_transmission, p_recovery, first_positive_person):
    new_positive_case(population_list, first_positive_person)
    draw_network(population_list)

    while not all_cases_positive(population_list):
        simulate_step(population_list, p_transmission, p_recovery)
        draw_network(population_list)

    return None


def simulate_run_no_draw(population_list, p_transmission, p_recovery, first_positive_person):
    new_positive_case(population_list, first_positive_person)

    count = 0
    while not all_cases_positive(population_list):
        simulate_step(population_list, p_transmission, p_recovery)
        count += 1

    return count


def simulate_many(population_size, p_transmission, p_recovery, first_positive_person, num_runs):
    num_steps_list = list()

    for run in range(num_runs):
        population_list = create_population_list(population_size)
        simulation = simulate_run_no_draw(population_list, p_transmission, p_recovery, first_positive_person)
        num_steps_list.append(simulation)

    average = np.mean(num_steps_list)
    return average


# CODE FOR SUBMISSION
simulate_run(create_population_list(15), 0.8, 0.1, 0)
average_steps = simulate_many(15, 0.8, 0.1, 0, 10000)
print("Avg. steps for complete transmission: ", average_steps)
