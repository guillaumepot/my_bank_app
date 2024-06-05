#####
# TEMPORARY VARIABLES
#####
#
#
#
postgres_host="bank_app_postgres"
postgres_port=5432
postgres_user="root"
postgres_password= "root"
postgres_db = 'bank_db'
#
#
#
#####
# END OF TEMPORARY VARIABLES
#####


"""
PostGres Database connectors for the API
"""


"""
LIBS
"""
import os
from sqlalchemy import create_engine


"""
VARS
"""

# REMOVE COMMENT WHEN TEMP VARS ARE REMOVED
"""
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
"""


# Postgres engine
engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_user}/{postgres_db}")

