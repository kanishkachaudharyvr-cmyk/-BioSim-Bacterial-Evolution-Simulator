import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("simulation_metrics.csv")

# population vs time
plt.plot(df["time_step"], df["total_population"])
plt.xlabel("Time Step")
plt.ylabel("Population")
plt.title("Population Growth")
plt.savefig("charts/population_growth.png")
plt.clf()

# resource dynamics
plt.plot(df["time_step"], df["resource_concentration"])
plt.xlabel("Time Step")
plt.ylabel("Resource Level")
plt.title("Resource Dynamics")
plt.savefig("charts/resource_dynamics.png")
plt.clf()

# mutation frequency
plt.plot(df["time_step"], df["mutation_frequency"])
plt.xlabel("Time Step")
plt.ylabel("Mutation Frequency")
plt.title("Mutation Evolution")
plt.savefig("charts/mutation_frequency.png")