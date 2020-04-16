from xmlrpc.client import ServerProxy
import random
import uuid
import time
import subprocess

"""
This file times the xml-rpc functions on the server one time and prints the output
"""

client = ServerProxy('http://3.22.170.142:8000', allow_none=True)

name_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
product_id = []
order_id = []

# def populate():
#     for _ in range(1000):
#         client.addProduct(str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), random.random(), random.random(), random.randint(0, 1000))


def add_products():
    for name in name_list:
        id = client.addProduct(name, 'something', 'me', 4, 5, 900)
        product_id.append(id)


def get_and_update_products():
    for id_ in product_id:
        client.getProduct(id_, '')
        client.updateProduct(id_, '', 'different description', 'mark', 3, 9, 100)


def list_products():
    client.listProducts('T', '')
    client.listProducts('T', 'different descriptioin')
    client.listProducts('F', 'diff')
    client.listProducts('F', '')


def add_get_update_orders():
    for _ in range(26):
        order_id1 = client.addOrder('Easton', 'today', [product_id[_], 1], 'T', 'T')
        order_id.append(order_id1)
        client.getOrder(order_id1)
        client.updateOrder(order_id1, 'Wind Gap', 'Saturday', 'F', 'T')


def amend_orders():
    for id_ in range(26):
        client.addProductsToOrder(order_id[id_], [product_id[id_], 1])
        client.removeProductsFromOrder(order_id[id_], [product_id[id_], 1])


def list_orders():
    client.listOrders('', '')
    client.listOrders('T', 'F')
    client.listOrders('F', 'T')
    client.listOrders('T', 'T')


def call_all_functions():
    add_products()
    get_and_update_products()
    list_products()
    add_get_update_orders()
    amend_orders()
    list_orders()


def main():
    host = 'ec2-user@aws-project2'
    kill_command = 'kill -9 \$(ps aux | grep python3 | awk \'{print \$2}\' | head -n 1)'
    start_command = 'python3 store_inventory_run_servers.py'
    subprocess.Popen(['ssh', host, kill_command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    client.clearDatabase()
    subprocess.Popen(['ssh', host, start_command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # populate()
    
    start_time = time.monotonic()
    call_all_functions()
    end_time = time.monotonic()

    print(end_time - start_time)


if __name__ == '__main__':
    main()
