"""
Simple visualization script for basic data analysis.
"""
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Optional

from .config import PROCESSED_DATA_DIR
from .load import execute_query

logger = logging.getLogger(__name__)

def setup_plot_style():
    """Configure the style for all plots."""
    plt.style.use('seaborn')
    sns.set_palette("husl")

def plot_time_series(df: pd.DataFrame,
                    date_column: str,
                    value_column: str,
                    title: str,
                    output_path: Optional[Path] = None) -> None:
    """
    Create a time series plot.
    
    Args:
        df: DataFrame containing the data
        date_column: Name of the date column
        value_column: Name of the value column to plot
        title: Plot title
        output_path: Optional path to save the plot
    """
    setup_plot_style()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df[date_column], df[value_column])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(value_column)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        logger.info(f"Saved plot to {output_path}")
    else:
        plt.show()
    
    plt.close()

def plot_distribution(df: pd.DataFrame,
                     column: str,
                     title: str,
                     output_path: Optional[Path] = None) -> None:
    """
    Create a distribution plot.
    
    Args:
        df: DataFrame containing the data
        column: Name of the column to plot
        title: Plot title
        output_path: Optional path to save the plot
    """
    setup_plot_style()
    
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=column, kde=True)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        logger.info(f"Saved plot to {output_path}")
    else:
        plt.show()
    
    plt.close()

def plot_correlation_matrix(df: pd.DataFrame,
                          columns: Optional[List[str]] = None,
                          title: str = 'Correlation Matrix',
                          output_path: Optional[Path] = None) -> None:
    """
    Create a correlation matrix heatmap.
    
    Args:
        df: DataFrame containing the data
        columns: Optional list of columns to include
        title: Plot title
        output_path: Optional path to save the plot
    """
    setup_plot_style()
    
    if columns:
        df = df[columns]
    
    corr_matrix = df.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title(title)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        logger.info(f"Saved plot to {output_path}")
    else:
        plt.show()
    
    plt.close()

def generate_visualizations(query: str,
                          output_dir: Optional[Path] = None) -> None:
    """
    Generate a set of visualizations from a database query.
    
    Args:
        query: SQL query to fetch data
        output_dir: Optional directory to save visualizations
    """
    try:
        # Fetch data
        df = execute_query(query)
        
        # Create output directory if specified
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate visualizations based on data types
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                # Time series plot for datetime columns
                for value_col in df.select_dtypes(include=['number']).columns:
                    title = f'{value_col} over time'
                    output_path = output_dir / f'{value_col}_time_series.png' if output_dir else None
                    plot_time_series(df, column, value_col, title, output_path)
            
            elif pd.api.types.is_numeric_dtype(df[column]):
                # Distribution plot for numeric columns
                title = f'Distribution of {column}'
                output_path = output_dir / f'{column}_distribution.png' if output_dir else None
                plot_distribution(df, column, title, output_path)
        
        # Correlation matrix for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_cols) > 1:
            output_path = output_dir / 'correlation_matrix.png' if output_dir else None
            plot_correlation_matrix(df, numeric_cols, output_path=output_path)
            
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    query = "SELECT * FROM processed_data"
    output_dir = PROCESSED_DATA_DIR / 'visualizations'
    generate_visualizations(query, output_dir) 