# Data Pipeline

A modular and extensible data pipeline for ETL (Extract, Transform, Load) operations.

## Project Structure

```
├── src/                  # Source code directory
│   ├── __init__.py       # Makes src a proper package
│   ├── config.py         # Configuration settings
│   ├── extract.py        # Data extraction module
│   ├── transform.py      # Data transformation module
│   ├── load.py          # Database loading module
│   ├── pipeline.py      # Main pipeline orchestration
│   ├── scheduler.py     # Scheduling script
│   ├── visualize.py     # Simple visualization script
│   └── utils.py         # Helper functions
├── data/                 # Data directory
│   ├── raw/             # Raw data storage
│   └── processed/       # Processed data storage
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Features

- Modular ETL pipeline architecture
- Support for multiple data sources (API, CSV files)
- Data transformation and cleaning utilities
- Database integration with PostgreSQL
- Automated scheduling of pipeline runs
- Basic data visualization capabilities
- Comprehensive logging and error handling
- Configuration management

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd data-pipeline
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the project root with the following variables:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=data_pipeline
DB_USER=your_username
DB_PASSWORD=your_password
```

## Usage

### Running the Pipeline

1. Configure your pipeline in `src/config.py` or create a custom configuration file.

2. Run the pipeline:

```python
from src.pipeline import DataPipeline

pipeline = DataPipeline(
    source_type='api',
    source_config={
        'url': 'https://api.example.com/data',
        'save_raw': True,
        'raw_filename': 'raw_data.csv'
    },
    transform_config={
        'date_columns': ['created_at', 'updated_at'],
        'save_processed': True,
        'processed_filename': 'processed_data.csv'
    },
    load_config={
        'table_name': 'processed_data',
        'schema': 'public'
    }
)

pipeline.run()
```

### Scheduling Pipeline Runs

```python
from src.scheduler import schedule_pipeline

pipeline_config = {
    'source_type': 'api',
    'source_config': {
        'url': 'https://api.example.com/data',
        'save_raw': True,
        'raw_filename': 'raw_data.csv'
    },
    'transform_config': {
        'date_columns': ['created_at', 'updated_at'],
        'save_processed': True,
        'processed_filename': 'processed_data.csv'
    },
    'load_config': {
        'table_name': 'processed_data',
        'schema': 'public'
    }
}

# Schedule pipeline to run daily at midnight
schedule_pipeline(pipeline_config, schedule_interval='daily', time='00:00')
```

### Generating Visualizations

```python
from src.visualize import generate_visualizations
from src.config import PROCESSED_DATA_DIR

# Generate visualizations from database query
query = "SELECT * FROM processed_data"
output_dir = PROCESSED_DATA_DIR / 'visualizations'
generate_visualizations(query, output_dir)
```
