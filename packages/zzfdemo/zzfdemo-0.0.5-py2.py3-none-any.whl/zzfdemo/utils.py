"""这是一个工具模块，提供了一些工具函数。
"""

def csv_to_df(csv_file):
    """将一个 CSV 文件转换为 DataFrame 对象。
    """
    import pandas as pd
    return pd.read_csv(csv_file)