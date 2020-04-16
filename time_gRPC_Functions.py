import random
import uuid
import time
import grpc
import gRPC_store_inventory_pb2
import gRPC_store_inventory_pb2_grpc


name_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
product_id = []
order_id = []


def populate(client):
    for _ in range(1000):
        client.addProduct(gRPC_store_inventory_pb2.Product(name=str(uuid.uuid4()), description=str(uuid.uuid4()), manufacturer=str(uuid.uuid4()), wholesale_cost=random.random(), sale_cost=random.random(), amount_in_stock=random.randint(0, 1000)))


def add_products(client):
    for name in name_list:
        id_val = client.addProduct(gRPC_store_inventory_pb2.Product(name=name, description='something', manufacturer='me', wholesale_cost=4, sale_cost=5, amount_in_stock=900))
        product_id.append(id_val.id_number)


def get_update_products(client):
    for id_ in product_id:
        client.getProduct(gRPC_store_inventory_pb2.ProductID(id_number=id_))
        client.updateProduct(gRPC_store_inventory_pb2.UpdateProductInfo(id_number=id_, description='differetn description', manufacturer='mark', wholesale_cost=3, sale_cost=9, amount_in_stock=100))


def list_products(client):
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='T', manufacturer='ehy'))
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='T', manufacturer='differnt descriptioin'))
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='F', manufacturer='diff'))
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='F', manufacturer='aldkfj'))


def add_get_update_order(client):
    for _ in range(len(product_id)):
        order_id1 = client.addOrder(gRPC_store_inventory_pb2.Order(destination='Easton', date='today', products=[gRPC_store_inventory_pb2.ProductAndDemand(product=gRPC_store_inventory_pb2.ProductID(id_number=product_id[_]), num_of_product=1)], is_shipped='T', is_paid='T'))
        order_id.append(order_id1.id_number)
        client.getOrder(gRPC_store_inventory_pb2.OrderID(id_number=order_id1.id_number))
        client.updateOrder(gRPC_store_inventory_pb2.UpdateOrderInfo(id_number=order_id1.id_number, destination='Wind Gap', date='Saturday', is_shipped='F', is_paid='T'))


def amend_orders(client):
    for id_ in range(len(product_id)):
        client.addProductsToOrder(gRPC_store_inventory_pb2.AddToOrder(id_number=order_id[id_], products=[gRPC_store_inventory_pb2.ProductAndDemand(product=gRPC_store_inventory_pb2.ProductID(id_number=product_id[id_]), num_of_product=1)]))
        client.removeProductsFromOrder(gRPC_store_inventory_pb2.RemoveFromOrder(id_number=order_id[id_], products=[gRPC_store_inventory_pb2.ProductAndDemand(product=gRPC_store_inventory_pb2.ProductID(id_number=product_id[id_]), num_of_product=1)]))


def list_orders(client):
    start = time.monotonic()
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='', is_paid=''))
    print(time.monotonic() - start)
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='T', is_paid='F'))
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='F', is_paid='T'))
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='T', is_paid='T'))


def call_functions(client):
    add_products(client)
    get_update_products(client)
    list_products(client)
    add_get_update_order(client)
    amend_orders(client)
    list_orders(client)


def main():

    with grpc.insecure_channel('3.22.170.142:50052') as channel:
        client = gRPC_store_inventory_pb2_grpc.ProductInventoryStub(channel)

        client.clearDatabase(gRPC_store_inventory_pb2.Empty())
        populate(client)

        start_time = time.monotonic()
        call_functions(client)
        end_time = time.monotonic()

        print(end_time - start_time)

        client.clearDatabase(gRPC_store_inventory_pb2.Empty())


if __name__ == '__main__':
    main()
