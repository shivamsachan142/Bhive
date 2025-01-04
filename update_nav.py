from apscheduler.schedulers.background import BackgroundScheduler
import requests

scheduler = BackgroundScheduler()

def update_nav():
    # Logic to fetch latest NAV from RapidAPI and update the portfolio
    print("Updating NAV for all portfolios...")

scheduler.add_job(update_nav, "interval", hours=1)
scheduler.start()
