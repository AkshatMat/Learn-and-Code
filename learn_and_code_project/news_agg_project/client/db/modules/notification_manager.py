from client.utils.exception import DatabaseError, NotificationError
from client.utils.logger import logger

class NotificationManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_user_preferences(self, user_id):
        try:
            query = """
                SELECT category, is_enabled
                FROM user_notification_config_table
                WHERE user_id = %s
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching preferences: {e}")
            raise NotificationError(f"Failed to fetch notification preferences: {str(e)}")

    def update_category_preference(self, user_id, category, is_enabled):
        try:
            query = """
                INSERT INTO user_notification_config_table (user_id, category, is_enabled)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, category)
                DO UPDATE SET is_enabled = EXCLUDED.is_enabled;
            """
            self.cursor.execute(query, (user_id, category, is_enabled))
        except Exception as e:
            logger.error(f"Error updating preference: {e}")
            raise NotificationError(f"Failed to update category preference: {str(e)}")

    def get_user_keywords(self, user_id):
        try:
            query = "SELECT keyword FROM user_keyword_table WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            return [row["keyword"] for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching keywords: {e}")
            raise NotificationError(f"Failed to fetch keywords: {str(e)}")

    def update_user_keywords(self, user_id, keywords):
        try:
            delete_query = "DELETE FROM user_keyword_table WHERE user_id = %s"
            self.cursor.execute(delete_query, (user_id,))
            insert_query = "INSERT INTO user_keyword_table (user_id, keyword) VALUES (%s, %s)"
            for keyword in keywords:
                self.cursor.execute(insert_query, (user_id, keyword))
        except Exception as e:
            logger.error(f"Error updating keywords: {e}")
            raise NotificationError(f"Failed to update keywords: {str(e)}")

    def fetch_unviewed_notifications(self, user_id):
        try:
            query = """
                SELECT a.uuid, a.title, a.content, a.source, a.url, a.category, a.published_at, a.author
                FROM user_notification_table u
                JOIN news_table a ON u.article_id = a.uuid
                WHERE u.user_id = %s AND u.viewed = FALSE
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching unviewed notifications: {e}")
            raise NotificationError(f"Failed to fetch notifications: {str(e)}")

    def mark_notification_as_viewed(self, user_id, article_id):
        try:
            query = """
                UPDATE user_notification_table
                SET viewed = TRUE
                WHERE user_id = %s AND article_id = %s
            """
            self.cursor.execute(query, (user_id, article_id))
        except Exception as e:
            logger.error(f"Error marking notification as viewed: {e}")
            raise NotificationError(f"Failed to mark notification as viewed: {str(e)}")

    def mark_notifications_as_viewed(self, user_id):
        try:
            query = """
                UPDATE user_notification_table
                SET viewed = TRUE
                WHERE user_id = %s AND viewed = FALSE
            """
            self.cursor.execute(query, (user_id,))
        except Exception as e:
            logger.error(f"Error marking as viewed: {e}")
            raise NotificationError(f"Failed to update viewed status: {str(e)}")
        
    def get_all_users(self):
        try:
            query = """
                SELECT DISTINCT u.user_id, u.email
                FROM user_table u
                JOIN user_notification_config_table c ON u.user_id = c.user_id
                LEFT JOIN user_keyword_table k ON u.user_id = k.user_id
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching users for notification: {e}")
            raise NotificationError(f"Failed to fetch users for notification: {str(e)}")

    def get_users_for_article_notification(self, category, content):
        try:
            category_query = """
                SELECT DISTINCT user_id
                FROM user_notification_config_table
                WHERE category = %s AND is_enabled = TRUE
            """
            self.cursor.execute(category_query, (category,))
            category_users = [row['user_id'] for row in self.cursor.fetchall()]
            
            keyword_query = """
                SELECT DISTINCT k.user_id
                FROM user_keyword_table k
                WHERE LOWER(%s) LIKE LOWER(CONCAT('%%', k.keyword, '%%'))
            """
            self.cursor.execute(keyword_query, (content,))
            keyword_users = [row['user_id'] for row in self.cursor.fetchall()]
            
            all_users = list(set(category_users + keyword_users))
            
            logger.info(f"Found {len(all_users)} users to notify for category '{category}'")
            return all_users
            
        except Exception as e:
            logger.error(f"Error finding users for notification: {e}")
            raise NotificationError(f"Failed to find users for notification: {str(e)}")

    def create_notification(self, user_id, article_id):
        try:
            query = """
                INSERT INTO user_notification_table (user_id, article_id, viewed, notified_at)
                VALUES (%s, %s, FALSE, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id, article_id) DO NOTHING
            """
            self.cursor.execute(query, (user_id, article_id))
            logger.info(f"Created notification for user {user_id}, article {article_id}")
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise NotificationError(f"Failed to create notification: {str(e)}")

    def get_user_email(self, user_id):
        try:
            query = "SELECT email FROM user_table WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            return result['email'] if result else None
            
        except Exception as e:
            logger.error(f"Error fetching user email: {e}")
            raise NotificationError(f"Failed to fetch user email: {str(e)}")
