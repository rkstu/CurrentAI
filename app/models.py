import pymysql
import ssl
import random
import string
# from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from .config import Config
from .utils import queries_and_response

class TiDBDatabaseComponent:
    def __init__(self):
        # Setup the SSL context
        # ssl_context = ssl.create_default_context(cafile="/etc/ssl/certs/ca-certificates.crt")
        # ssl_context.check_hostname = False
        # ssl_context.verify_mode = ssl.CERT_REQUIRED

        # Establish the connection
        self.connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            ssl={
                'ca': None  # Disable SSL for Windows
            }        )

    def generate_user_id(self, length=5):
        """
        Generates a random userId of specified length.

        :param length: The length of the userId to be generated (default is 5).
        :return: A random string of the specified length.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def add_user(self, emailId, password, first_name, last_name):
        """
        Adds a user to the user table with a randomly generated userId.

        :param emailId: The email address of the user.
        :param password: The user's password.
        :param first_name: The first name of the user.-
        :param last_name: The last name of the user.
        :return: The generated userId for the new user.
        """
        userId = self.generate_user_id()
        with self.connection.cursor() as cursor:
            sql = """
            INSERT INTO user (userId, emailId, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (userId, emailId, password, first_name, last_name))
        self.connection.commit()
        return userId

    def add_queries(self, userId, chat_history): # Need to DO
        """
        Adds multiple entries to the query table.

        :param userId: The unique identifier for the user.
        :param queries: A list of dictionaries containing 'query' and 'response' as key-value pairs.
        """
        with self.connection.cursor() as cursor:
            sql = """
            INSERT INTO query (userId, query, response)
            VALUES (%s, %s, %s)
            """
            for entry in chat_history:
                cursor.execute(sql, (userId, entry[0], entry[1]))
        self.connection.commit()

    def user_exists(self, emailId, password):
        """
        Checks if a user exists in the user table based on emailId and password.

        :param emailId: The email address of the user.
        :param password: The user's password.
        :return: True if the user exists, otherwise False.
        """
        with self.connection.cursor() as cursor:
            sql = """
            SELECT COUNT(*) FROM user
            WHERE emailId = %s AND password = %s
            """
            cursor.execute(sql, (emailId, password))
            result = cursor.fetchone()
            return result[0] > 0

    def get_user_queries(self, userId):
        """
        Retrieves all queries and responses for a given userId from the query table, in the order they were saved.

        :param userId: The unique identifier for the user.
        :return: A list of dictionaries containing 'query' and 'response' for the user.
        """
        with self.connection.cursor() as cursor:
            sql = """
            SELECT query, response FROM query
            WHERE userId = %s
            ORDER BY id ASC
            """
            cursor.execute(sql, (userId,))
            result = cursor.fetchall()
            return [{'query': row[0], 'response': row[1]} for row in result]

    def update_user_password(self, userId, new_password):
        """
        Updates the password for an existing user in the user table.

        :param userId: The unique identifier for the user.
        :param new_password: The new password to be set for the user.
        """
        with self.connection.cursor() as cursor:
            sql = """
            UPDATE user
            SET password = %s
            WHERE userId = %s
            """
            cursor.execute(sql, (new_password, userId))
        self.connection.commit()

    def get_user_id_by_email(self, emailId):
        """
        Fetches the userId for a given emailId from the user table.

        :param emailId: The email address of the user.
        :return: The userId associated with the given emailId, or None if not found.
        """
        with self.connection.cursor() as cursor:
            sql = """
            SELECT userId FROM user
            WHERE emailId = %s
            """
            cursor.execute(sql, (emailId,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_first_name_by_email(self, emailId):
        """
        Fetches the first_name for a given emailId from the user table.

        :param emailId: The email address of the user.
        :return: The first_name associated with the given emailId, or None if not found.
        """
        with self.connection.cursor() as cursor:
            sql = """
            SELECT first_name FROM user
            WHERE emailId = %s
            """
            cursor.execute(sql, (emailId,))
            result = cursor.fetchone()
            return result[0] if result else None

# def analyze_sentiment(sentences):
#     finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
#     tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
#     nlp_pipeline = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
#     results = nlp_pipeline(sentences)
#     return results

# Function to save query and response
# query_response = []

# def save_query_and_response(user_query: str):
#     response = run_agent(user_query)
#     query_response.append({"response": response, "query": user_query})

# Your LangChain agent code (run_agent function) from the provided code
