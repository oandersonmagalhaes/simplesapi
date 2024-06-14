"""
SimplesAPI
"""

from .app import SimplesAPI as SimplesAPI, SimplesConfig as SimplesConfig

from .types import Database as Database, Cache as Cache

from .lifespan import database as database
