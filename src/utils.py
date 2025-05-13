import os

def get_project_root():
    """Returns the absolute path to the project root directory."""
    # src directory is one level down from the project root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_path(subdir='', filename=''):
    """Returns the absolute path to the data directory or a file within it."""
    data_dir = os.path.join(get_project_root(), 'data', subdir)
    os.makedirs(data_dir, exist_ok=True)
    
    if filename:
        return os.path.join(data_dir, filename)
    return data_dir

def get_logs_path(filename=''):
    """Returns the absolute path to the logs directory or a file within it."""
    logs_dir = os.path.join(get_project_root(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    if filename:
        return os.path.join(logs_dir, filename)
    return logs_dir

def get_visualizations_path(filename=''):
    """Returns the absolute path to the visualizations directory or a file within it."""
    viz_dir = os.path.join(get_project_root(), 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    if filename:
        return os.path.join(viz_dir, filename)
    return viz_dir