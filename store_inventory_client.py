import XML_store_inventory_client
import gRPC_store_inventory_client
import argparse


# def main():
#     with grpc.insecure_channel('localhost:50052') as channel:
#         stub = store_inventory_pb2_grpc.ProductInventoryStub(channel)
#         # for response in stub.list_Products(ProductInfo_pb2.Filter(filter='w')):
#         #     print(response)

#         response1 = stub.addProduct(store_inventory_pb2.Product(name='some', description='its a widget', manufacturer='yes', wholesale_cost=1.23, amount_in_stock=5))
#         print(response1)

#         response2 = stub.addProduct(store_inventory_pb2.Product(name='sup', manufacturer='maaccccc', wholesale_cost=5.6, sale_cost=4.8, amount_in_stock=9))
#         print(response2)

#         response3 = stub.addProduct(store_inventory_pb2.Product(name='new', description='n', manufacturer='mak', amount_in_stock=55))
#         print(response3)

#         response4 = stub.addProduct(store_inventory_pb2.Product(name='fourth', description='fourth item', manufacturer='tv', wholesale_cost=3, sale_cost=90, amount_in_stock=90))
#         print(response4)
       
#         list_of_items = list(stub.listProducts(store_inventory_pb2.ListProductsInfo(in_stock=1)))
#         print(list_of_items)
        

#         # product1 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response1.id_number))
#         # print(product1)

#         # upd = stub.updateProduct(store_inventory_pb2.UpdateProductInfo(id_number=response1.id_number, wholesale_cost=890, description='something lame'))
#         # print(upd)
#         # product2 = stub.getProduct(store_inventory_pb2.ProductID(name=response2.name))
#         # print(product2)
#         # product3 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response3.id_number))
#         # product4 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response4.id_number))

#         order1 = stub.addOrder(store_inventory_pb2.Order(destination='here', date='today', products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response1.id_number), num_of_product=1)], is_shipped=1, is_paid=1))
#         print(order1)
#         # getorder1 = stub.getOrder(store_inventory_pb2.OrderID(id_number=order1.id_number))
#         # print(getorder1)

#         re_get_product1 = stub.getProduct(store_inventory_pb2.ProductID(id_number=response1.id_number))
#         print(re_get_product1)
#         # order2 = stub.addOrder(store_inventory_pb2.Order(destination='there', date='tomorrow', products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response2.id_number), num_of_product=3)], is_shipped=1, is_paid=-1))
#         # order3 = stub.addOrder(store_inventory_pb2.Order(destination='over', date='friday', products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response3.id_number), num_of_product=6)], is_shipped=1, is_paid=1))

#         # updated_order = stub.updateOrder(store_inventory_pb2.UpdateOrderInfo(id_number=order1.id_number, destination='shelby', date='tommorew', is_shipped=-1))
#         # print(updated_order)

#         # addprod = stub.addProductsToOrder(store_inventory_pb2.AddToOrder(id_number=order1.id_number, products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response1.id_number), num_of_product=1)]))
#         # print(addprod)

#         # g = stub.getProduct(store_inventory_pb2.ProductID(id_number=response1.id_number))
#         # print(g)

#         # rem = stub.removeProductsFromOrder(store_inventory_pb2.RemoveFromOrder(id_number=order1.id_number, products=[store_inventory_pb2.ProductAndDemand(product=store_inventory_pb2.ProductID(id_number=response1.id_number), num_of_product=1)]))
#         # print(rem)

#         # x = stub.getProduct(store_inventory_pb2.ProductID(id_number=response1.id_number))
#         # print(x)

#         list_of_orders = list(stub.listOrders(store_inventory_pb2.OrderStatus()))
#         print(list_of_orders)
#         # list_of_shipped_paid_orders = list(stub.listOrders(store_inventory_pb2.OrderStatus()))
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

def get_client(server):
    if server == 'xml':
        return XML_store_inventory_client.xmlrpcStoreInventoryClient()
    else:
        return gRPC_store_inventory_client.grpcStoreInventoryClient()


def product_fields(subparser):
    subparser.add_argument('description', help='The description of product')
    subparser.add_argument('manufacturer', help='The manufacturer of product')
    subparser.add_argument('wholesale_cost', type=float, help='The wholesale cost of the product')
    subparser.add_argument('sale_cost', type=float, help='The sale cost of the product')
    subparser.add_argument('amount_in_stock', type=int, help='Amount of product in stock')


def optional_product_fields(subparser):
    subparser.add_argument('--description', help='The description of product')
    subparser.add_argument('--manufacturer', help='The manufacturer of product')
    subparser.add_argument('--wholesale_cost', type=float, help='The wholesale cost of the product')
    subparser.add_argument('--sale_cost', type=float, help='The sale cost of the product')
    subparser.add_argument('--amount_in_stock', type=int, help='Amount of product in stock')


def order_fields(subparser):
    subparser.add_argument('destination', help='The destination of the order')
    subparser.add_argument('date', help='The date the order is to be shipped')
    subparser.add_argument('is_shipped', help='Whether or not the order has been shipped')
    subparser.add_argument('is_paid', help='Whether or not the order has been paid')


def optional_order_fields(subparser):
    subparser.add_argument('--destination', help='The destination of the order')
    subparser.add_argument('--date', help='The date the order is to be shipped')
    subparser.add_argument('--is_shipped', help='Whether or not the order has been shipped')
    subparser.add_argument('--is_paid', help='Whether or not the order has been paid')


def main():
    parser = argparse.ArgumentParser(description='Client to interact with either the gRPC or XML-RPC store inventory server')
    parser.add_argument('grpc_or_xml', choices=['grpc', 'xml'], help='Which server to interact with')

    subparsers = parser.add_subparsers(title='command', dest='cmd', required=True)

    add_product = subparsers.add_parser(name='add-product', help='Add a product to the inventory database')
    add_product.add_argument('name', help='The name of a product')
    product_fields(add_product)

    get_product_by_id = subparsers.add_parser(name='get-product-by-id', help='Get a product specified by id from the inventory database')
    get_product_by_id.add_argument('id_number', help='The id of a product')

    get_product_by_name = subparsers.add_parser(name='get-product-by-name', help='Get a product specified by its name from the inventory database')
    get_product_by_name.add_argument('name', help='the name of a product')

    update_product_by_id = subparsers.add_parser(name='update-product-by-id', help='Update a product specified by its id')
    update_product_by_id.add_argument('id_number', help='The id number of product')
    optional_product_fields(update_product_by_id)

    update_product_by_name = subparsers.add_parser(name='update-product-by-name', help='Update a product specified by its name')
    update_product_by_name.add_argument('name', help='The name of the product')
    optional_product_fields(update_product_by_name)
            
    list_products = subparsers.add_parser(name='list-products', help='List products based on manufacturer and/or products are in stock')
    list_products.add_argument('--manufacturer', help='The product manufacturer to search for')
    list_products.add_argument('--in-stock', help='Whether or not the product is in stock', default='F')




    add_order = subparsers.add_parser(name='add-order', help='Add an order to the inventory database')
    order_fields(add_order)
    add_order.add_argument('products', nargs='+', help='The list of product ids followed by their counts to be added to the order')

    get_order = subparsers.add_parser(name='get-order', help='Get an order from the inventory database')
    get_order.add_argument('id_number', help='The id of the desired order')

    update_order = subparsers.add_parser(name='update-order', help='Update the given order')
    update_order.add_argument('id_number', help='The id of the order to update')
    optional_order_fields(update_order)

    add_products_to_order = subparsers.add_parser(name='add-to-order', help='Add products to an order')
    add_products_to_order.add_argument('id_number', help='The id of the order to update')
    add_products_to_order.add_argument('products', nargs='+', help='A list of products followed by their counts to be added to the order')

    remove_products_from_order = subparsers.add_parser(name='remove-from-order', help='Remove products from an order')
    remove_products_from_order.add_argument('id_number', help='The id of the order to update')
    remove_products_from_order.add_argument('products', nargs='+', help='A list of products followed by their counts to be removed from an order')

    list_orders = subparsers.add_parser(name='list-orders', help='List all orders based on shipped status and paid status')
    list_orders.add_argument('--is_shipped', help='Whether or not the order has been shipped', default='F')
    list_orders.add_argument('--is_paid', help='Whether or not the order has been paid', default='F')

    args = parser.parse_args()

    client = get_client(args.grpc_or_xml)

    if args.cmd == 'add-product':
        client.addProduct(args.name, args.description, args.manufacturer, args.wholesale_cost, args.sale_cost, args.amount_in_stock)
    elif args.cmd == 'get-product-by-id':
        client.getProductById(args.id_number)
    elif args.cmd == 'get-product-by-name':
        client.getProductByName(args.name)
    elif args.cmd == 'update-product-by-id':
        client.updateProductById(args.id_number, args.description, args.manufacturer, args.wholesale_cost, args.sale_cost, args.amount_in_stock)
    elif args.cmd == 'update-product-by-name':
        client.updateProductByName(args.name, args.description, args.manufacturer, args.wholesale_cost, args.sale_cost, args.amount_in_stock)
    elif args.cmd == 'list-products':
        client.listProducts(args.manufacturer, args.in_stock)
    
    elif args.cmd == 'add-order':
        client.addOrder(args.destination, args.date, args.products, args.is_shipped, args.is_paid)
    elif args.cmd == 'get-order':
        client.getOrder(args.id_number)
    elif args.cmd == 'update-order':
        client.updateOrder(args.id_number, args.destination, args.date, args.is_shipped, args.is_paid)
    elif args.cmd == 'add-to-order':
        client.addProductsToOrder(args.id_number, args.products)
    elif args.cmd == 'remove-from-order':
        client.removeProductsFromOrder(args.id_number, args.products)
    else:
        client.listOrders(args.is_shipped, args.is_paid)


if __name__ == '__main__':
    main()

