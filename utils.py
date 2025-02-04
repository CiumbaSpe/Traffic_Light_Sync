import matplotlib.pyplot as plt
import itertools

def unique_permutations(arr):
    permutations = list(itertools.permutations(arr))    # generate all permutations
    permutations = [list(p) for p in permutations]      # convert tuples to lists
    unique_perms = []                                   # store unique permutations
    for perm in permutations:                           # iterate through all permutations
        if perm[::-1] not in unique_perms:              # avoid adding reverse duplicates
            unique_perms.append(perm)                   # add the permutation to the list
    return unique_perms


def plot_simulation_graph(step, warm_up, completed_lifetimes):

    # Generate the x and y values for the plot
    x_values = list(range(step-warm_up))
    y_values = []

    # Calculate the average lifetime at each step
    for i in range(step-warm_up):
        current_lifetimes = [lifetime for j, lifetime in enumerate(completed_lifetimes) if j <= i]
        if current_lifetimes:
            average_lifetime = sum(current_lifetimes) / len(current_lifetimes)
            y_values.append(average_lifetime)
        else:
            y_values.append(0)

    # Create the plot
    plt.plot(x_values, y_values)

    # Add labels and title
    plt.xlabel('Simulation Step')
    plt.ylabel('Average Lifetime (seconds)')
    plt.title('Average Vehicle Lifetime Over Simulation Steps')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # plot_simulation_graph(1000, 100, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    a = unique_permutations([1, 2, 3, 4])
    print(a)
    print(len(a)) 

