import boto3_dynamodb
set1 = boto3_dynamodb.get_product(817428)
print(type(set1))

set2 = {'price': '4500'}

print(type(set2))
print(set1)
print(set2)
set1.update(set2)
print(set1)