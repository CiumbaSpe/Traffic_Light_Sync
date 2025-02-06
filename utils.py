import matplotlib.pyplot as plt


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
    pass

