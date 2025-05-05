import numpy as np
import matplotlib.pyplot as plt

def save_heatmap(array, filename='heatmap.png', cmap='viridis'):
    """
    Generates and saves a heatmap from a 2D array.

    Parameters:
        array (2D list or numpy.ndarray): The input 2D data.
        filename (str): Path to save the image file.
        cmap (str): Colormap used for the heatmap.
    """
    array = np.array(array)  # Ensure input is a NumPy array
    plt.figure(figsize=(8, 6))
    plt.imshow(array, cmap=cmap, aspect='auto')
    plt.colorbar(label='Value')
    plt.title('Heatmap')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Heatmap saved to {filename}")
