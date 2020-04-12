import random
import uuid
import time
import grpc
import gRPC_store_inventory_pb2
import gRPC_store_inventory_pb2_grpc


with grpc.insecure_channel('18.218.18.59:50052') as channel:
    client = gRPC_store_inventory_pb2_grpc.ProductInventoryStub(channel)

# This is used to populate the database if i accidentally delete it 
# for _ in range(1000):
#     client.addProduct(str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), random.random(), random.random(), random.randint(0, 1000))


    name_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    product_id = []
    order_id = []

    start_time = time.monotonic()


    for name in name_list:
        id_val = client.addProduct(gRPC_store_inventory_pb2.Product(name=name, description='something', manufacturer='me', wholesale_cost=4, sale_cost=5, amount_in_stock=900))
        product_id.append(id_val.id_number)
        print(id_val)


    for id_ in product_id:
        print(id_)
        client.getProduct(gRPC_store_inventory_pb2.ProductID(id_number=id_))
        print('yes')
        client.updateProduct(gRPC_store_inventory_pb2.UpdateProductInfo(id_number=id_, description='differetn description', manufacturer='mark', wholesale_cost=3, sale_cost=9, amount_in_stock=100))


    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='T', manufacturer='ehy'))
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='T', manufacturer='differnt descriptioin'))
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='F', manufacturer='diff'))
    client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock='F', manufacturer='aldkfj'))


    print('succesfful')
    for _ in range(len(product_id)):
        order_id1 = client.addOrder(gRPC_store_inventory_pb2.Order(destination='Easton', date='today', products=[gRPC_store_inventory_pb2.ProductAndDemand(product=gRPC_store_inventory_pb2.ProductID(id_number=product_id[_]), num_of_product=1)], is_shipped='T', is_paid='T'))
        order_id.append(order_id1.id_number)
        client.getOrder(gRPC_store_inventory_pb2.OrderID(id_number=order_id1.id_number))
        client.updateOrder(gRPC_store_inventory_pb2.UpdateOrderInfo(id_number=order_id1.id_number, destination='Wind Gap', date='Saturday', is_shipped='F', is_paid='T'))

    for id_ in range(len(product_id)):
        client.addProductsToOrder(gRPC_store_inventory_pb2.AddToOrder(id_number=order_id[id_], products=[gRPC_store_inventory_pb2.ProductAndDemand(product=gRPC_store_inventory_pb2.ProductID(id_number=product_id[id_]), num_of_product=1)]))
        client.removeProductsFromOrder(gRPC_store_inventory_pb2.RemoveFromOrder(id_number=order_id[id_], products=[gRPC_store_inventory_pb2.ProductAndDemand(product=gRPC_store_inventory_pb2.ProductID(id_number=product_id[id_]), num_of_product=1)]))


    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='', is_paid=''))
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='T', is_paid='F'))
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='F', is_paid='T'))
    client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped='T', is_paid='T'))

    end = time.monotonic()

    print(end - start_time)



