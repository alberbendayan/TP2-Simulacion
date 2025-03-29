import matplotlib.pyplot as plt
import numpy as np

def plot_monte_carlo_differences(filename):
    try:
        # Read the data from the file
        data = np.loadtxt(filename)
        
        # Create x-axis (step numbers)
        steps = np.arange(1, len(data) + 1)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(steps, data, 'b-', linewidth=1)
        plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        
        # Add labels and title
        plt.xlabel('Monte Carlo Step')
        plt.ylabel('Difference (1 - (-1))')
        plt.title('Difference between 1 and -1 in Monte Carlo Simulation')
        
        # Add grid for better readability
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1)
        
        # Show the plot
        plt.tight_layout()
        plt.savefig('monte_carlo_differences.png')
        plt.show()
        
        # Check if stationary state is reached
        # (You might want to modify this criterion based on your specific definition)
        window_size = min(100, len(data)//10)  # Use last 10% or 100 points, whichever is smaller
        if window_size > 0:
            recent_data = data[-window_size:]
            mean = np.mean(recent_data)
            std_dev = np.std(recent_data)
            print(f"Last {window_size} steps statistics:")
            print(f"Mean: {mean:.4f}")
            print(f"Standard Deviation: {std_dev:.4f}")
            print(f"Coefficient of Variation: {std_dev/abs(mean) if mean != 0 else float('inf'):.4f}")
            
    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    # Replace with the path to your data file
    file_path = "../result/general/results_0.01.txt"
    plot_monte_carlo_differences(file_path)