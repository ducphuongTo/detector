import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import re

def format_y_axis(ax, values):
    """
    Formats the y-axis based on the maximum value in the data to avoid duplicate labels.
    """
    max_value = values.max()

    if max_value >= 1e9:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e9:.1f}B'))
    elif max_value >= 1e6:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
    elif max_value >= 1e3:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.1f}K'))
    else:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}'))

    # Use MaxNLocator to let Matplotlib decide the best tick positions
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=6))

def sanitize_filename(name):
    """
    Sanitizes a string to make it safe for use as a filename.
    """
    return re.sub(r'[<>:"/\\|?*]', '', name)

def flatten_columns(df):
    """
    Flattens MultiIndex columns in a DataFrame by joining column levels into a single string.
    """
    df.columns = [' '.join(filter(None, map(str, col))).strip() if isinstance(col, tuple) else col for col in df.columns]
    return df

def select_label_and_value_columns(table):
    """
    Selects potential label and value columns from the table based on data characteristics.
    """
    label_column = None
    value_columns = []
    total_rows = len(table)

    for col in table.columns:
        # Skip columns without proper headers
        if "Unnamed" in str(col):
            continue

        numeric_data = pd.to_numeric(table[col], errors='coerce')
        num_numeric = numeric_data.count()

        # Skip columns with sequential numbers (e.g., indices)
        diffs = numeric_data.dropna().diff()
        if diffs.nunique() == 1 and diffs.iloc[0] == 1:
            continue

        if num_numeric / total_rows >= 0.5:
            value_columns.append(col)
        else:
            if label_column is None and table[col].nunique() > total_rows * 0.5:
                label_column = col

    return label_column, value_columns

def plot_data(label_column, value_column, data):
    """
    Plots the data using Matplotlib and saves the figure as an image file.
    """
    labels = data[label_column]
    values = data[value_column]

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    plt.title(f"{value_column} by {label_column}")
    plt.xlabel(label_column)
    plt.ylabel(value_column)
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Format y-axis
    ax = plt.gca()
    format_y_axis(ax, values)

    # Save the plot
    safe_label = sanitize_filename(label_column)
    safe_value_column = sanitize_filename(value_column)
    output_file = f"output_{safe_value_column}_by_{safe_label}.png"
    plt.savefig(output_file)
    print(f"Saved plot to {output_file}")
    plt.close()

def process_tables(tables):
    """
    Processes each table to find suitable columns and generates plots.
    """
    for idx, table in enumerate(tables):
        table = flatten_columns(table)

        label_column, value_columns = select_label_and_value_columns(table)

        if label_column and value_columns:
            labels = table[label_column].astype(str)
            for value_column in value_columns:
                values = pd.to_numeric(table[value_column], errors='coerce')

                # Create DataFrame and drop NaNs
                data = pd.DataFrame({label_column: labels, value_column: values})
                data.dropna(subset=[value_column], inplace=True)

                # Limit to first 30 items
                data = data.iloc[:30]

                plot_data(label_column, value_column, data)

            return  # Process only the first suitable table

    print("No suitable columns found for plotting in the tables.")

def main():
    url = input("Enter the Wikipedia page URL: ")

    try:
        tables = pd.read_html(url, header=0)
    except Exception as e:
        print(f"Error reading tables from URL: {e}")
        return

    process_tables(tables)

if __name__ == "__main__":
    main()
