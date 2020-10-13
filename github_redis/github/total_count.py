import logging

import pymongo

from github.settings import MONGO_DB,MONGO_URL,COLLECTION

def get_data_from_mongo(has_email=None):
    try:
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
    except:
        logging.error("数据库连接超时或异常，请检查！")
        raise ConnectionError("数据库连接超时或异常，请检查！")
    if has_email:
        total_nums = db[COLLECTION].find().count()
        email_nums = db[COLLECTION].find({"email": {"$ne": ''}}).count()
        print(email_nums)


if __name__ == '__main__':
    get_data_from_mongo(has_email=True)