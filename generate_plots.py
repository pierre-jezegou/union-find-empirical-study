import pandas as pd
from jinja2 import Template

CSV_ROOT = 'data'
TEX_ROOT = 'documentation/plots'


def generate_plot(n_value: int, metric: str, ymax: int = 5):
    csv_file_path = f'{CSV_ROOT}/union_find_experiments_results_{n_value}.csv'
    data = pd.read_csv(csv_file_path)

    # Create a list of dictionaries to hold the data for templating
    plot_data = []

    # Group the data by 'Union-Find Class', 'Path Compression', and 'k', then calculate the mean TPL
    grouped_data = data.groupby(['Union-Find Class', 'Path Compression', 'k']).mean().reset_index()

    # Group the data by 'Union-Find Class' and 'Path Compression' again for plotting
    final_grouped_data = grouped_data.groupby(['Union-Find Class', 'Path Compression'])

    colors = {
        'QuickUnion': 'violet',
        'UnionRank': 'blue',
        'UnionWeight': 'orange',
    }

    teintes = {
        'NC': 25,
        'FC': 50,
        'PS': 75,
        'PH': 100
    }

    symbols = {
        'NC': '*',
        'FC': 'o',
        'PS': '+',
        'PH': 'x'
    }

    for (uf_class, path_compression), group in final_grouped_data:
        coordinates = list(zip(group['k'], group[metric]))
        color = colors.get(uf_class, 'black')  # default to black if not found
        teinte = teintes.get(path_compression, 100)
        symbol = symbols.get(path_compression, 'o')  # default to 'o' if not found
        plot_data.append({
            'label': f"{uf_class} with Path Compression {path_compression}",
            'coordinates': coordinates,
            'color': f"{color}!{teinte}",
            'symbol': symbol
        })

    # Jinja2 template for PGFPlots
    with open('resources/template_serie.tex.jinja') as f:
        pgf_template = f.read()

    # Create a Jinja2 template object
    template = Template(pgf_template)

    # Render the template with the data
    pgf_code = template.render(plots=plot_data, x_label='k', y_label=metric, n_value=n_value, y_max=ymax)

    # Output the generated PGF code
    return pgf_code


def save_code_in_file(code: str, filename: str):
    with open(f'{TEX_ROOT}/{filename}', 'w') as f:
        f.write(code)

print(generate_plot(1000, 'Normalized TPL'))

if __name__ == '__main__':
    n_values = [1000, 5000, 10000]
    metrics = ['Normalized TPU', 'Normalized TPL']
    
    for n_value in n_values:
        for metric in metrics:
            pgf_code = generate_plot(n_value, metric)
            save_code_in_file(pgf_code, f'plot_{n_value}_{metric}.tex')
