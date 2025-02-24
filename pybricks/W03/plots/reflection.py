import matplotlib.pyplot as plt

# Data
distances = [1.5, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 30]
reflections = [34, 13, 7, 4, 3, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0]

# Create figure and axis
plt.figure(figsize=(8, 5), dpi=100)
plt.plot(distances, reflections, marker="o", linestyle="-", color="#007acc", markersize=8, linewidth=2, label="Sensor Value")

# Improve readability
plt.title("Sensor Value vs. Distance", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Distance (cm)", fontsize=12)
plt.ylabel("Sensor Value", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)

# Add annotations
for x, y in zip(distances, reflections):
    plt.text(x, y, str(y), fontsize=10, ha="right", va="bottom", color="black")

# Show legend
plt.legend()

# Show the plot
plt.show()
