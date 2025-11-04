import time
import os
import httpx
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
TRANSACTIONS_SERVICE_URL = os.getenv("TRANSACTIONS_SERVICE_URL", "http://transactions-service:8000")
AI_INSIGHTS_SERVICE_URL = os.getenv("AI_INSIGHTS_SERVICE_URL", "http://ai-insights-service:8000")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

headers = {"X-Internal-API-Key": INTERNAL_API_KEY}

def daily_summary_job():
    logger.info("Starting daily summary job...")
    
    if not INTERNAL_API_KEY:
        logger.error("INTERNAL_API_KEY not set. Skipping job.")
        return

    try:
        # This is a mock implementation.
        # In a real app, you would have internal endpoints to fetch data.
        # 1. Get all users from Auth Service
        # resp_users = httpx.get(f"{AUTH_SERVICE_URL}/internal/users", headers=headers)
        # resp_users.raise_for_status()
        # users = resp_users.json()
        
        # logger.info(f"Found {len(users)} users to process.")
        
        # for user in users:
        #    user_id = user['id']
        #    # 2. Get user's transactions
        #    resp_tx = httpx.get(f"{TRANSACTIONS_SERVICE_URL}/internal/transactions/{user_id}", headers=headers)
        #    ...
        #    # 3. Post to AI service for summary
        #    resp_ai = httpx.post(f"{AI_INSIGHTS_SERVICE_URL}/internal/generate-summary", json=..., headers=headers)
        #    ...
        #    # 4. Save summary to DB or send email
        
        logger.info("Mock job: Fetched users, generated summaries, and sent emails.")
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during daily job: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logger.error(f"An error occurred during daily job: {e}")

    logger.info("Daily summary job finished.")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # Run every day at 2 AM
    # scheduler.add_job(daily_summary_job, 'cron', hour=2)
    
    # For demonstration, run every 5 minutes
    scheduler.add_job(daily_summary_job, 'interval', minutes=5)
    
    logger.info("Starting worker service...")
    logger.info("Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass