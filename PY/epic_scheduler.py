#!/usr/bin/env python3
"""
Epic FHIR API Scheduler
Run automated syncs on schedule
"""
import sys
import os
import time
from datetime import datetime

try:
    import schedule
except ImportError:
    print("schedule library not installed")
    print("Install with: pip install schedule")
    sys.exit(1)

# Configuration
PERSON_ID = "P001"  # Change to your QM person ID
SYNC_INTERVAL_HOURS = 24  # Sync every 24 hours
SYNC_TIME = "02:00"  # Or sync at specific time (2 AM)

def run_sync():
    """Run the sync process"""
    print("\n" + "="*60)
    print(f"Running scheduled sync: {datetime.now()}")
    print("="*60)
    
    # Import and run sync
    sys.path.insert(0, os.path.dirname(__file__))
    from epic_api_sync import main as sync_main
    
    try:
        # Run sync
        result = sync_main([sys.argv[0], PERSON_ID])
        
        if result == 0:
            print(f"\n✓ Sync completed successfully at {datetime.now()}")
        else:
            print(f"\n✗ Sync failed at {datetime.now()}")
    
    except Exception as e:
        print(f"\n✗ Sync error: {e}")

def main():
    print("="*60)
    print("Epic FHIR API Scheduler")
    print("="*60)
    print(f"Person ID: {PERSON_ID}")
    print(f"Schedule: Every {SYNC_INTERVAL_HOURS} hours (or at {SYNC_TIME})")
    print("\nPress Ctrl+C to stop")
    print("="*60)
    
    # Schedule options (choose one):
    
    # Option 1: Sync every N hours
    # schedule.every(SYNC_INTERVAL_HOURS).hours.do(run_sync)
    
    # Option 2: Sync at specific time daily
    schedule.every().day.at(SYNC_TIME).do(run_sync)
    
    # Run once immediately on startup
    print("\nRunning initial sync...")
    run_sync()
    
    # Keep running
    print(f"\nNext sync scheduled for: {schedule.next_run()}")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
        return 0

if __name__ == "__main__":
    sys.exit(main())
