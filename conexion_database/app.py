import pymysql
import os


def lambda_handler(event, context):
    # Validaciones básicas
    required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASS', 'DB_NAME']
    for var in required_env_vars:
        if not os.environ.get(var):
            raise ValueError(f"Missing required environment variable: {var}")

    try:
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            database=os.environ['DB_NAME']
        )
        cursor = connection.cursor()

        # Ejecutar una consulta
        cursor.execute("SELECT NOW()")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return {
            'statusCode': 200,
            'body': {
                'message': 'Query executed successfully',
                'result': result
            }
        }

    except pymysql.MySQLError as e:
        return {
            'statusCode': 500,
            'body': {
                'message': 'Database connection failed',
                'error': str(e)
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'message': 'An error occurred',
                'error': str(e)
            }
        }
