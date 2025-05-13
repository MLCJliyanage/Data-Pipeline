#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the data pipeline.
"""

import os
import sys

# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()