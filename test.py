import unittest
import pandas as pd
import matplotlib.pyplot as plt
from main import format_y_axis, sanitize_filename, flatten_columns

class TestMain(unittest.TestCase):

    def test_format_y_axis_large_values(self):
        fig, ax = plt.subplots()
        values = pd.Series([1e9, 2e9, 3e9])
        format_y_axis(ax, values)
        formatter = ax.yaxis.get_major_formatter()
        self.assertEqual(formatter(1e9), '1.0B')

    def test_format_y_axis_small_values(self):
        fig, ax = plt.subplots()
        values = pd.Series([10, 20, 30])
        format_y_axis(ax, values)
        formatter = ax.yaxis.get_major_formatter()
        self.assertEqual(formatter(10), '10')

    def test_sanitize_filename_special_characters(self):
        unsafe_name = 'output<>:"/\\|?*.png'
        safe_name = sanitize_filename(unsafe_name)
        self.assertEqual(safe_name, 'output.png')

    def test_sanitize_filename_no_change(self):
        safe_name = sanitize_filename('output.png')
        self.assertEqual(safe_name, 'output.png')

    def test_flatten_columns_multiindex(self):
        df = pd.DataFrame({
            ('A', 'B'): [1, 2],
            ('C', 'D'): [3, 4]
        })
        df_flattened = flatten_columns(df)
        self.assertListEqual(df_flattened.columns.tolist(), ['A B', 'C D'])

    def test_flatten_columns_singleindex(self):
        df = pd.DataFrame({
            'A': [1, 2],
            'B': [3, 4]
        })
        df_flattened = flatten_columns(df)
        self.assertListEqual(df_flattened.columns.tolist(), ['A', 'B'])

if __name__ == '__main__':
    unittest.main()
