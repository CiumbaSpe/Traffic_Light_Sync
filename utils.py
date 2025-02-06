import matplotlib.pyplot as plt
import setting
import xml.etree.ElementTree as ET


def setting_to_stdout():
    print(f"Number of semaphores {setting.SEMAPHORES}")
    print(f"Total TLS Cycle time {setting.TLS_TOTAL_TIME}")
    print(f"Number of configurations: {setting.CONFIGURATION} different offsets")
    print(f"Flow rate of tangential flow: {setting.TANGENTIAL_FLOW}")
    print(f"Number of runs per configuration: {setting.RUNS}")
    print(f"Numebr of steps per runs: {setting.STEP}")
    print(f"Number of warm-up steps: {setting.WARM_UP}")
    print(f"Results will be saved in {setting.NAME}\n")

# Function to modify the XML based on id values
def modify_rou_flow_rate(file_path, value):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    for flow in root.findall('flow'):
        if flow.get('id') in ['tan_ltr', 'tan_rtl']:
            flow.set('period', f'exp({str(value)})')  # Change this value as needed

    # Write the modified XML back to the file
    tree.write(file_path)


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
    # Call the function with the XML file path
    modify_xml('prova.xml', 0.1)  # Change 'input.xml' to the path of your XML file