import pandas
import seaborn as sns
from matplotlib import pyplot as plt

df = pandas.read_csv('data.csv')



# plt.figure(figsize=(14, 8))
# sns.lineplot(data=df, x='n', y='Time (s)', hue='Union-Find Class', style='Path Compression', markers=True)
# plt.title('Execution Time vs n')
# plt.xlabel('Number of elements (n)')
# plt.ylabel('Execution Time (s)')
# plt.legend(title='Union-Find & Path Compression')
# plt.grid(True)
# plt.savefig('execution_time.png')
# plt.show()

# # Plot TPU
# plt.figure(figsize=(14, 8))
# sns.lineplot(data=df, x='n', y='TPU', hue='Union-Find Class', style='Path Compression', markers=True)
# plt.title('Total Path Updates (TPU) vs n')
# plt.xlabel('Number of elements (n)')
# plt.ylabel('Total Path Updates (TPU)')
# plt.legend(title='Union-Find & Path Compression')
# plt.grid(True)
# plt.savefig('tpu.png')
# plt.show()

# Plot TPL
plt.figure(figsize=(14, 8))
sns.lineplot(data=df, x='n', y='Normalized TPL', hue='Union-Find Class', style='Path Compression', markers=True)
plt.title('Total Path Length (TPL) vs n')
plt.xlabel('Number of elements (n)')
plt.ylabel('Total Path Length (TPL)')
plt.legend(title='Union-Find & Path Compression')
plt.grid(True)
plt.savefig('tpl.png')
plt.show()

# # Plot time
# plt.figure(figsize=(14, 8))
# sns.lineplot(data=df, x='n', y='Time (s)', hue='Path Compression', style='Union-Find Class', markers=True)
# plt.title('Execution Time vs n')
# plt.xlabel('Number of elements (n)')
# plt.ylabel('Execution Time (s)')
# plt.legend(title='Path Compression & Union-Find')
# plt.grid(True)
# plt.savefig('execution_time_path.png')
# plt.show()