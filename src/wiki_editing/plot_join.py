# Yea I didn't bother writing any of this myself

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Get the directory where this script is located
csv = os.path.join(os.path.abspath("./Data/member_join.csv"))

# Read the CSV file with proper delimiter (comma)
df = pd.read_csv(csv, sep=r',', engine='python')

# Create a proper date column for plotting
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Create the plot
plt.figure(figsize=(12, 8))

# Plot both count lines
plt.plot(df['date'], df['count_modding'], marker='o', linewidth=2, label='Modding Count', color='blue')
plt.plot(df['date'], df['count_mapping'], marker='s', linewidth=2, label='Mapping Count', color='red')

# Customize the plot
plt.title('Member Count Growth Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Format x-axis to show months nicely
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
# plt.show()
plt.savefig(os.path.abspath("./Files/Plot modding communities join count.png"))

# Print some statistics
print("\nLast growth:")
print(f"Modding growth: {df['count_modding'].iloc[-1] - df['count_modding'].iloc[-2]} members")
print(f"Mapping growth: {df['count_mapping'].iloc[-1] - df['count_mapping'].iloc[-2]} members")
print(f"Time period: {df['date'].iloc[-2].strftime('%B %Y')} to {df['date'].iloc[-1].strftime('%B %Y')}")