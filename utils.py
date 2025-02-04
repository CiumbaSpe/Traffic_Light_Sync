import matplotlib.pyplot as plt
import setting
import xml.etree.ElementTree as ET
import math
import pandas as pd
import setting

def display_setting():
    print(f"Number of semaphores {setting.SEMAPHORES}")
    print(f"Total TLS Cycle time {setting.TLS_TOTAL_TIME}")
    print(f"Number of configurations: {setting.CONFIGURATION} different offsets")
    print(f"Configuration step: {setting.CONFIGURATION_STEP}")
    print(f"Flow rate of tangential flow: {setting.TANGENTIAL_FLOW}")
    print(f"Number of runs per configuration: {setting.RUNS}")
    print(f"Numebr of steps per runs: {setting.STEP}")
    print(f"Number of warm-up steps: {setting.WARM_UP}")
    print(f"Results will be saved in {setting.NAME}\n")

# Function to modify the XML based on id values
def modify_rou_flow_rate(file_path, value, steps):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    for flow in root.findall('flow'):
        flow.set('end', str(steps))  # Set the end attribute to the number of steps

        if flow.get('id') in ['tan_ltr', 'tan_rtl']:
            flow.set('period', f'exp({str(value)})')  # Change this value as needed
        else:
            flow.set('period', f'exp({str(math.floor(value*1000/3)/1000)})')

    # Write the modified XML back to the file
    tree.write(file_path)


def applying_moving_average(x, window):
    y_series = pd.Series(x)
    return y_series.rolling(window=window, min_periods=1).mean().to_numpy()

def plot_simulation_graph(completed_lifetimes : list[int], arrival_times : list[int], name: str = None):
        
    # Applying moving average to the completed lifetimes
    y_values = applying_moving_average(completed_lifetimes, 5000)

    # Create the plot
    plt.scatter(arrival_times, y_values, 
            marker='o',           # Point shape
            s=3,                 # Point size
            alpha=0.7,            # Transparency
            color='blue',         # Point color
    )

    # Add labels and title
    plt.xlabel('Simulation Step')
    plt.ylabel('Average Lifetime (seconds)')
    plt.title('Average Vehicle Lifetime Over Simulation Steps')

    if(name is not None):
        plt.savefig(name)  # Save with high resolution

    # Show the plot
    plt.show()


def print_csv_files():
    # List of CSV file names and corresponding labels
    # csv_files = ['results/t15/03/_Network_tang_completed_lifetimes.csv']
    # csv_files = ['results/t15/flusses/_Network_tang_completed_lifetimes.csv']
    # csv_files = ['results/t15/FinalFlus/from03to05/_Network_tang_completed_lifetimes.csv']
    csv_files = ['results/prova/TightFluss/Network_tang_throughput.csv']
    labels = ['L0']

    plt.figure(figsize=(10, 6))

    for file, label in zip(csv_files, labels):
        # Read the CSV; assuming the first column (config_x) is the index
        df = pd.read_csv(file, index_col=0)
        
        # Extract x (configuration), y (lifetime mean), and confidence intervals
        x = df.index  # e.g., "config_0", "config_1", ...
        y = df['mean']
        lower = df['ci_lower']
        upper = df['ci_upper']
            
        # Plot the line with markers for each CSV file
        line = plt.plot(x, y, marker='o', label=label)
        
        # Add confidence interval as a shaded area
        plt.fill_between(x, lower, upper, alpha=0.2, color=line[0].get_color())

    # Add labels, title, legend, and grid
    plt.xlabel('L')
    plt.ylabel('Throughput')
    plt.title('Throughput over different values of L')
    # plt.legend()
    plt.xticks(rotation=55, ticks=x)  # Rotate x-axis labels if needed
    plt.grid(True)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    # Call the function with the XML file path
    # modify_rou_flow_rate('lightSync.rou.xml', 0.3, setting.STEP)  # Change 'input.xml' to the path of your XML file
    print_csv_files()  # Change to the list of CSV files you want to plot
    # plot_simulation_graph([63, 62, 65, 31], [3, 5, 6, 8])
    

