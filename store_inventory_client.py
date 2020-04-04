import grpc
import store_inventory_pb2
import store_inventory_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = store_inventory_pb2_grpc.ProductInventoryStub(channel)
        # for response in stub.list_Products(ProductInfo_pb2.Filter(filter='w')):
        #     print(response)

        response1 = stub.addProduct(store_inventory_pb2.Product(name='some', description='its a widget', manufacturer='yes', wholesale_cost=1.23, amount_in_stock=5))
        print(response1)

        response2 = stub.addProduct(store_inventory_pb2.Product(name='sup', description='is someting', manufacturer='maaccccc', wholesale_cost=5.6, sale_cost=4.8, amount_in_stock=9))
        print(response2)

        response3 = stub.addProduct(store_inventory_pb2.Product(name='new', description='n', manufacturer='mak', amount_in_stock=55))
        print(response3)

        response4 = stub.addProduct(store_inventory_pb2.Product(name='fourth', description='fourth item', manufacturer='tv', wholesale_cost=3, sale_cost=90, amount_in_stock=90))
        print(response4)
       
        list_of_items = list(stub.listProducts(store_inventory_pb2.ListProductsInfo(in_stock=1)))
        print(list_of_items)
        

        product1 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response1.id_number))
        print(product1)

        upd = stub.updateProduct(store_inventory_pb2.UpdateProductInfo(id_number=response1.id_number, wholesale_cost=890, description='something lame'))
        print(upd)
        product2 = stub.getProduct(store_inventory_pb2.ProductID(name=response2.name))
        print(product2)
        product3 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response3.id_number))
        # product4 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response4.id_number))

        # order1 = stub.addOrder(store_inventory_pb2.Order(destination='here', date='today', products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response1.id_number), num_of_product=1)], is_shipped=1, is_paid=1))
        # order2 = stub.addOrder(store_inventory_pb2.Order(destination='there', date='tomorrow', products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response2.id_number), num_of_product=3)], is_shipped=1, is_paid=-1))
        # order3 = stub.addOrder(store_inventory_pb2.Order(destination='over', date='friday', products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response3.id_number), num_of_product=6)], is_shipped=1, is_paid=1))

        # list_of_shipped_paid_orders = list(stub.listOrders(store_inventory_pb2.OrderStatus()))
        # print(list_of_shipped_paid_orders)

        # list_of_shipped_orders = list(stub.listOrders(store_inventory_pb2.OrderStatus(is_shipped=True, is_paid=False)))
        # print(list_of_shipped_orders)

        # list_of_paid_orders = list(stub.listOrders(store_inventory_pb2.OrderStatus(is_shipped=False, is_paid=True)))
        # print(list_of_paid_orders)

        # list_of_orders = list(stub.listOrders(store_inventory_pb2.OrderStatus(is_shipped=False, is_paid=False)))
        # print(list_of_orders)


        # add_prod = stub.addProductsToOrder(store_inventory_pb2.AddToOrder(id_number=order3.id_number, products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response3.id_number), num_of_product=8)]))
        # print(add_prod)

        # get = stub.getProduct(store_inventory_pb2.ProductID(id_number=response3.id_number))
        # print(get)

        # remo = stub.removeProductsFromOrder(store_inventory_pb2.RemoveFromOrder(id_number=order3.id_number, products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response3.id_number), num_of_product=6)]))
        # print(remo)

        # up = stub.updateOrder(store_inventory_pb2.UpdateOrderInfo(id_number=order3.id_number, date='blah'))
        # print(up)

        # ord = stub.getOrder(store_inventory_pb2.OrderID(id_number=order3.id_number))
        # print(ord)

        # x = stub.getProduct(store_inventory_pb2.ProductID(id_number=response3.id_number))
        # print(x)

        # up = stub.updateOrder(store_inventory_pb2.UpdateOrderInfo())

        # response = stub.getProduct(store_inventory_pb2.ProductID(name='sup'))
        # print(response)

        # response = list(stub.listProducts(store_inventory_pb2.ProductID(manufacturer='yes')))
        # print(response)

        # response = stub.updateProduct(store_inventory_pb2.UpdateProductInfo(name='sup', description='oh hey there', manufacturer='Mark Morka', wholesale_cost=3))
        # print(response)

        # print('i am doing it')
        # product1 = store_inventory_pb2.Product(name='hello', description='first item', manufacturer='Rielye', wholesale_cost=54.2, sale_cost=60)
        # product2 = store_inventory_pb2.Product(name='different', description='second item', manufacturer='matt', wholesale_cost=76, sale_cost=90)

        # response = stub.addOrder(store_inventory_pb2.Order(destination='moravain', date='today', products=[product1, product2], is_paid=False, is_shipped=False))
        # print(response)

        # # response = stub.getOrder(store_inventory_pb2.OrderID(id_number=response.id_number))
        # # print(response)

        # # response = stub.updateOrder(store_inventory_pb2.UpdateOrderInfo(id_number=response.id_number, destination='Lehigh', date='tomorrow', is_paid=True))
        # # print(response)

        # response = stub.getOrder(store_inventory_pb2.OrderID(id_number=response.id_number))
        # print(response)
        # response = stub.addOrder(store_inventory_pb2.Order(destination='house', date='rug', products=[product1, product2], is_paid=True))

        # test = store_inventory_pb2.Product(name='more tests', description='need more', manufacturer='yes please', wholesale_cost=5)
        # print('made the test')
        # response = stub.addProductsToOrder(store_inventory_pb2.ManageProductsInOrder(id_number=response.id_number, products=[test]))
        # print(response)
        # # response = stub.addProduct(ProductInfo_pb2.Product(id='', name='product', description='its a product'))
        # # print(response.value)

        # # response = stub.addProduct(ProductInfo_pb2.Product(id='', name='beans', description='its a bean'))
        # # print(response.value)

        # # response = stub.getProduct(ProductInfo_pb2.ProductID(value='23'))
        # # print(response.name, response.description)


if __name__ == '__main__':
    main()


