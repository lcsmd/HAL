#!/usr/bin/env python3
"""
Automated Email Processor Daemon
Continuously monitors for new emails and processes them automatically
"""

import time
import schedule
import signal
import sys
from pathlib import Path
from datetime import datetime, timedelta
import configparser
import logging

# Import our modules
from gmail_ingestion import GmailIngestion
from rule_engine import RuleEngine
from ai_categorization_engine import AICategorizationEngine


class EmailProcessorDaemon:
    """Automated email processing daemon"""
    
    def __init__(self, config_file: Path, qm_account='EMAILSYS'):
        self.config_file = config_file
        self.qm_account = qm_account
        self.running = True
        self.last_email_id = None
        
        # Load configuration
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Setup logging
        log_dir = Path(self.config.get('system', 'log_dir', 
                       fallback=str(Path.home() / 'email_management_system' / 'logs')))
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / 'processor_daemon.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.base_dir = Path(self.config.get('system', 'base_dir',
                            fallback=str(Path.home() / 'email_management_system')))
        
        self.gmail_ingestion = None
        self.rule_engine = None
        self.ai_engine = None
        
        # Processing settings
        self.check_interval_minutes = int(self.config.get('daemon', 'check_interval_minutes', 
                                                          fallback='15'))
        self.batch_size = int(self.config.get('daemon', 'batch_size', fallback='50'))
        self.auto_categorize = self.config.getboolean('daemon', 'auto_categorize', 
                                                       fallback=True)
        self.ai_categorize_threshold = int(self.config.get('daemon', 'ai_categorize_threshold',
                                                           fallback='100'))
        
    def initialize_components(self):
        """Initialize all processing components"""
        self.logger.info("Initializing components...")
        
        try:
            # Gmail ingestion
            config_dir = self.base_dir / 'config'
            self.gmail_ingestion = GmailIngestion(
                config_dir=config_dir,
                base_dir=self.base_dir,
                qm_account=self.qm_account
            )
            self.gmail_ingestion.authenticate()
            self.logger.info("✓ Gmail ingestion initialized")
            
        except Exception as e:
            self.logger.error(f"Gmail ingestion failed: {e}")
            self.gmail_ingestion = None
        
        try:
            # Rule engine
            self.rule_engine = RuleEngine(qm_account=self.qm_account)
            self.logger.info("✓ Rule engine initialized")
            
        except Exception as e:
            self.logger.error(f"Rule engine failed: {e}")
            self.rule_engine = None
        
        try:
            # AI engine (optional)
            if self.auto_categorize:
                self.ai_engine = AICategorizationEngine(
                    config_file=self.config_file,
                    qm_account=self.qm_account
                )
                self.logger.info("✓ AI categorization engine initialized")
                
        except Exception as e:
            self.logger.warning(f"AI engine not available: {e}")
            self.ai_engine = None
            self.auto_categorize = False
    
    def process_new_emails(self):
        """Process new emails from Gmail"""
        self.logger.info("="*60)
        self.logger.info("Processing New Emails")
        self.logger.info("="*60)
        
        if not self.gmail_ingestion:
            self.logger.error("Gmail ingestion not initialized")
            return
        
        try:
            # Get new messages
            messages = self.gmail_ingestion.get_messages(
                max_results=self.batch_size,
                query='is:unread'
            )
            
            if not messages:
                self.logger.info("No new emails to process")
                return
            
            self.logger.info(f"Found {len(messages)} new emails")
            
            # Process each message
            new_email_ids = []
            
            for i, msg in enumerate(messages, 1):
                self.logger.info(f"[{i}/{len(messages)}] Processing {msg['id']}...")
                
                email_id = self.gmail_ingestion.ingest_message(msg['id'])
                if email_id:
                    new_email_ids.append(email_id)
                    self.last_email_id = email_id
            
            self.logger.info(f"✓ Imported {len(new_email_ids)} new emails")
            
            # Apply rules to new emails
            if self.rule_engine and new_email_ids:
                self.logger.info("Applying rules to new emails...")
                
                for email_id in new_email_ids:
                    result = self.rule_engine.apply_rules_to_email(email_id, verbose=False)
                    if result['rules_matched'] > 0:
                        self.logger.info(f"  {email_id}: {result['rules_matched']} rules applied")
                
                self.logger.info("✓ Rules applied to new emails")
            
            # Check if we should run AI categorization
            if self.ai_engine and len(new_email_ids) >= self.ai_categorize_threshold:
                self.logger.info(f"Running AI categorization on {len(new_email_ids)} emails...")
                self.run_ai_categorization(new_email_ids)
            
            self.logger.info("="*60)
            self.logger.info(f"Processing Complete: {len(new_email_ids)} emails processed")
            self.logger.info("="*60)
            
        except Exception as e:
            self.logger.error(f"Error processing emails: {e}", exc_info=True)
    
    def run_ai_categorization(self, email_ids: list):
        """Run AI categorization on emails"""
        try:
            result = self.ai_engine.analyze_emails_for_categories(
                email_ids,
                max_emails=min(len(email_ids), 100)
            )
            
            if result['categories']:
                self.logger.info(f"AI proposed {len(result['categories'])} categories")
                stats = self.ai_engine.apply_categorization(result)
                self.logger.info(f"AI categorization applied: {stats}")
            
        except Exception as e:
            self.logger.error(f"AI categorization failed: {e}", exc_info=True)
    
    def run_maintenance(self):
        """Run maintenance tasks"""
        self.logger.info("Running maintenance tasks...")
        
        try:
            # Apply all rules to any uncategorized emails
            if self.rule_engine:
                from openqm_interface import OpenQMInterface, EmailRecord
                
                qm = OpenQMInterface(account=self.qm_account)
                email_rec = EmailRecord(qm)
                
                # Find uncategorized emails
                email_ids = qm.select_records('EMAILS', '')
                uncategorized = []
                
                for email_id in email_ids:
                    email = email_rec.get(email_id)
                    if email:
                        cats = email.get('categories', [])
                        if not cats or (isinstance(cats, list) and len(cats) == 0):
                            uncategorized.append(email_id)
                
                if uncategorized:
                    self.logger.info(f"Found {len(uncategorized)} uncategorized emails")
                    
                    # Apply rules
                    for email_id in uncategorized[:100]:  # Limit to 100 per run
                        self.rule_engine.apply_rules_to_email(email_id, verbose=False)
                    
                    self.logger.info("✓ Maintenance complete")
                else:
                    self.logger.info("No uncategorized emails found")
                    
        except Exception as e:
            self.logger.error(f"Maintenance failed: {e}", exc_info=True)
    
    def health_check(self):
        """Perform system health check"""
        self.logger.info("Performing health check...")
        
        checks = {
            'Gmail Connection': False,
            'Rule Engine': False,
            'AI Engine': False,
            'OpenQM Connection': False
        }
        
        # Check Gmail
        if self.gmail_ingestion and self.gmail_ingestion.gmail_service:
            checks['Gmail Connection'] = True
        
        # Check Rule Engine
        if self.rule_engine:
            try:
                rules = self.rule_engine.get_all_rules()
                checks['Rule Engine'] = True
            except:
                pass
        
        # Check AI Engine
        if self.ai_engine:
            checks['AI Engine'] = True
        
        # Check OpenQM
        try:
            from openqm_interface import OpenQMInterface
            qm = OpenQMInterface(account=self.qm_account)
            qm.read_record('SYSTEM.CONFIG', 'COUNTERS')
            checks['OpenQM Connection'] = True
        except:
            pass
        
        # Log results
        for check, status in checks.items():
            status_str = "✓ OK" if status else "✗ FAILED"
            self.logger.info(f"  {check}: {status_str}")
        
        all_passed = all(checks.values())
        if not all_passed:
            self.logger.warning("Some health checks failed!")
        
        return all_passed
    
    def schedule_jobs(self):
        """Schedule periodic jobs"""
        self.logger.info("Scheduling jobs...")
        
        # Process new emails
        schedule.every(self.check_interval_minutes).minutes.do(self.process_new_emails)
        self.logger.info(f"  • Process emails: Every {self.check_interval_minutes} minutes")
        
        # Run maintenance daily at 2 AM
        schedule.every().day.at("02:00").do(self.run_maintenance)
        self.logger.info("  • Maintenance: Daily at 2:00 AM")
        
        # Health check every hour
        schedule.every().hour.do(self.health_check)
        self.logger.info("  • Health check: Hourly")
        
        # Initial health check
        self.health_check()
    
    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Shutdown signal received. Stopping daemon...")
        self.running = False
    
    def run(self):
        """Main daemon loop"""
        self.logger.info("="*60)
        self.logger.info("Email Processor Daemon Starting")
        self.logger.info("="*60)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        # Initialize
        self.initialize_components()
        self.schedule_jobs()
        
        # Run initial processing
        self.logger.info("Running initial email processing...")
        self.process_new_emails()
        
        # Main loop
        self.logger.info("Daemon running. Press Ctrl+C to stop.")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(60)
        
        self.logger.info("Daemon stopped.")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Email Processor Daemon')
    parser.add_argument('--config', type=Path,
                       default=Path.home() / 'email_management_system' / 'config' / 'config.ini',
                       help='Configuration file path')
    parser.add_argument('--account', default='EMAILSYS', help='OpenQM account')
    parser.add_argument('--once', action='store_true', help='Run once and exit (no daemon)')
    
    args = parser.parse_args()
    
    daemon = EmailProcessorDaemon(
        config_file=args.config,
        qm_account=args.account
    )
    
    if args.once:
        # Run once and exit
        daemon.initialize_components()
        daemon.process_new_emails()
    else:
        # Run as daemon
        daemon.run()


if __name__ == '__main__':
    main()
