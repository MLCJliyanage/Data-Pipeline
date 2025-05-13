import schedule
import time
import logging
from datetime import datetime
import os
from src.pipeline import run_pipeline

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename=f'logs/scheduler_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('scheduler')

def job():
    """Job to run the pipeline on schedule"""
    logger.info("Running scheduled pipeline job")
    success = run_pipeline()
    logger.info(f"Scheduled job completed with status: {'Success' if success else 'Failed'}")

# Schedule the job
schedule.every().hour.do(job)  # Run every hour
# Alternative schedules:
# schedule.every().day.at("10:00").do(job)  # Run every day at 10 AM
# schedule.every(6).hours.do(job)  # Run every 6 hours

logger.info("Scheduler started")
print("Scheduler is running. Press Ctrl+C to exit.")

# Run the job immediately once
job()

# Keep the scheduler running
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    logger.info("Scheduler stopped by user")
    print("Scheduler stopped")