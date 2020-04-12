from xmlrpc.client import ServerProxy
import random
import uuid
import time

client = ServerProxy(f'http://18.218.18.59:8000')

# for _ in range(1000):
#     client.addProduct(str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), random.random(), random.random(), random.randint(0, 1000))

client.addProduct('dog', 'furry', 'me', 5, 6, 7)

id = client.getProduct('', 'dog')
print(id)

start_time = time.monotonic()

client.addProduct('some', 'something', )



