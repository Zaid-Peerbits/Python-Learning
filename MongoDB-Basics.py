# brew services start mongodb-community
# brew services stop mongodb-community
# mysql -u root
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
my_databse = client["zaid"]
my_collection = my_databse["contacts"]

# my_collection.insert_one({'name':'Zaid','phone':'886-663-0101' ,'email':'zaid@example.com' })

# data = [{'name':'Eric','phone':'467-946-9363' ,'email':'ericmiller@gmail.com' }, 
#         {'name':'Sabastian','phone':'726-133-0098' ,'email':'sabastian88@gmail.com' },
#         {'name':'Nemesis','phone':'231-982-4507' ,'email':'nemesis@gmail.com' }]
# my_collection.insert_many(data)

# my_query = my_collection.find_one_and_update({'name':'Nemesis'},{'$set':{'phone':'231-982-4507'}})
my_query = my_collection.find_one({'name':'Nemesis'})
print(my_query)

# for x in my_collection.find():
#     print(x)

# my_collection.drop()