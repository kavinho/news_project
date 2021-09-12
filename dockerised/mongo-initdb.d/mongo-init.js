print('Start #################################################################');

db = db.getSiblingDB('items');
db.news_items.createIndex({"headline":"text"});
print('END #################################################################');