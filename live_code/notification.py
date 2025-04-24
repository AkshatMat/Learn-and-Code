import logging
from typing import Optional

class NotificationService:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def send_customer_notification(self, email: str, message: str) -> bool:
        try:
            self.logger.info(f"Sending email to {email}: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send customer notification: {e}")
            return False

    def send_admin_notification(self, message: str) -> bool:
        try:
            self.logger.info(f"Admin notification: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send admin notification: {e}")
            return False