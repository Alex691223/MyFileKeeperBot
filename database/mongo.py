from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

mongo = MongoClient(MONGO_URI)
db = mongo[DB_NAME]

warns = db["warns"]
rules = db["rules"]
