from client.db.connection import DatabaseConnection
from client.db.modules.notification_manager import NotificationManager
from client.config.settings import settings
from client.utils.email_utils import send_email
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def get_user_preferences(user_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            preferences_list = NotificationManager(cursor).get_user_preferences(user_id)
            
            preferences_dict = {}
            
            for category in settings.CATEGORIES:
                preferences_dict[category] = False
            
            for row in preferences_list:
                if isinstance(row, dict):
                    category = row.get('category')
                    is_enabled = row.get('is_enabled')
                else:
                    category = row[0]
                    is_enabled = row[1]
                
                if category in preferences_dict:
                    preferences_dict[category] = is_enabled
            
            return preferences_dict

    @staticmethod
    def update_category_preference(user_id: str, category: str, enabled: bool):
        with DatabaseConnection.get_cursor() as cursor:
            NotificationManager(cursor).update_category_preference(user_id, category, enabled)

    @staticmethod
    def get_keywords(user_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            keywords_list = NotificationManager(cursor).get_user_keywords(user_id)
            return keywords_list

    @staticmethod
    def update_keywords(user_id: str, keywords: list):
        with DatabaseConnection.get_cursor() as cursor:
            NotificationManager(cursor).update_user_keywords(user_id, keywords)

    @staticmethod
    def get_unviewed_notifications(user_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            notifications = NotificationManager(cursor).fetch_unviewed_notifications(user_id)
            
            result = []
            for row in notifications:
                if isinstance(row, dict):
                    result.append(row)
                else:
                    result.append({
                        'uuid': row[0],
                        'title': row[1],
                        'content': row[2],
                        'source': row[3],
                        'url': row[4],
                        'category': row[5],
                        'published_at': row[6],
                        'author': row[7]
                    })
            
            return result

    @staticmethod
    def mark_notification_as_viewed(user_id: str, article_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            NotificationManager(cursor).mark_notification_as_viewed(user_id, article_id)

    @staticmethod
    def mark_all_as_viewed(user_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            NotificationManager(cursor).mark_notifications_as_viewed(user_id)

    @staticmethod
    def send_notification_email(user_id: str, article_data: dict):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                user_email = NotificationManager(cursor).get_user_email(user_id)
                print("user_email : ", user_email)
                print("dtype of user_email: ", type(user_email))
                
                if not user_email:
                    logger.warning(f"No email found for user {user_id}")
                    return False
                
                subject = f"News Alert: {article_data.get('title', 'New Article')}"
                
                body = f"""
Dear User,

You have received a new news notification based on your preferences:

Title: {article_data.get('title', 'N/A')}
Category: {article_data.get('category', 'N/A')}
Source: {article_data.get('source', 'N/A')}
Author: {article_data.get('author', 'N/A')}
Published: {article_data.get('published_at', 'N/A')}

Content Preview:
{article_data.get('content', 'N/A')[:200]}...

Read full article: {article_data.get('url', 'N/A')}

Best regards,
News Application Team
                """
                
                send_email(user_email, subject, body)
                logger.info(f"Notification email sent to {user_email} for article {article_data.get('uuid')}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send notification email: {e}")
            return False

    @staticmethod
    def process_new_article_notifications(article_data: dict):
        try:
            with DatabaseConnection.get_cursor() as cursor:
                notification_manager = NotificationManager(cursor)
                
                users_to_notify = notification_manager.get_users_for_article_notification(
                    article_data.get('category'),
                    article_data.get('title', '') + ' ' + article_data.get('content', '')
                )
                
                for user_id in users_to_notify:
                    notification_manager.create_notification(user_id, article_data.get('uuid'))
                    
                    NotificationService.send_notification_email(user_id, article_data)
                
                logger.info(f"Processed notifications for {len(users_to_notify)} users for article {article_data.get('uuid')}")
                
        except Exception as e:
            logger.error(f"Failed to process article notifications: {e}")

    @staticmethod
    def get_user_email(user_id: str):
        with DatabaseConnection.get_cursor() as cursor:
            return NotificationManager(cursor).get_user_email(user_id)
