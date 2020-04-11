import grpc
import gRPC_store_inventory_pb2
import gRPC_store_inventory_pb2_grpc


class grpcStoreInventoryClient:
    """
    Client for the gRPC server
    """

    def __init__(self, address, port):
        """
        Creates the channel to connect to based on the given address and port
        """
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.client = gRPC_store_inventory_pb2_grpc.ProductInventoryStub(channel)

    
    def successful_connection(self):
        """
        Determines if a successful connection to the server can be made
        """
        try:
            self.client.determineSuccessfulConnection(gRPC_store_inventory_pb2.Empty())
            return True
        except Exception:
            return False


    def get_list_of_products(self, products):
        """
        Returns a list of products and their quantities as a list of ProductAndDemand gRPC objects
        """
        product_list = []
        for product in range(0, len(products) - 1, 2):
            product_and_demand = gRPC_store_inventory_pb2.ProductAndDemand(
                                                                           product=gRPC_store_inventory_pb2.ProductID(
                                                                           id_number=products[product]), 
                                                                           num_of_product=int(products[product + 1]))
            product_list.append(product_and_demand)

        return product_list

    
    def addProduct(self, name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        product_id = self.client.addProduct(gRPC_store_inventory_pb2.Product(name=name, 
                                                                             description=description, 
                                                                             manufacturer=manufacturer, 
                                                                             wholesale_cost=wholesale_cost, 
                                                                             sale_cost=sale_cost, 
                                                                             amount_in_stock=amount_in_stock))
        print(product_id)


    def getProductById(self, id_number):
        product = self.client.getProduct(gRPC_store_inventory_pb2.ProductID(id_number=id_number))
        print(product)


    def getProductByName(self, name):
        product = self.client.getProduct(gRPC_store_inventory_pb2.ProductID(name=name))
        print(product)


    def updateProductById(self, id_number, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        product = self.client.updateProduct(gRPC_store_inventory_pb2.UpdateProductInfo(id_number=id_number, 
                                                                                     description=description, 
                                                                                     manufacturer=manufacturer, 
                                                                                     wholesale_cost=wholesale_cost, 
                                                                                     sale_cost=sale_cost, 
                                                                                     amount_in_stock=amount_in_stock))
        print(product)


    def updateProductByName(self, name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        product = self.client.updateProduct(gRPC_store_inventory_pb2.UpdateProductInfo(name=name, 
                                                                                       description=description, 
                                                                                       manufacturer=manufacturer, 
                                                                                       wholesale_cost=wholesale_cost, 
                                                                                       sale_cost=sale_cost, 
                                                                                       amount_in_stock=amount_in_stock))
        print(product)


    def listProducts(self, manufacturer, in_stock):
        list_of_products = list(self.client.listProducts(gRPC_store_inventory_pb2.ListProductsInfo(in_stock=in_stock, 
                                                                                                   manufacturer=manufacturer)))
        print(list_of_products)


    def addOrder(self, destination, date, products, is_shipped, is_paid):
        product_list = self.get_list_of_products(products)
        order_id = self.client.addOrder(gRPC_store_inventory_pb2.Order(destination=destination, date=date, products=product_list, is_shipped=is_shipped, is_paid=is_paid))
        print(order_id)


    def getOrder(self, id_number):
        order = self.client.getOrder(gRPC_store_inventory_pb2.OrderID(id_number=id_number))
        print(order)


    def updateOrder(self, id_number, destination, date, is_shipped, is_paid):
        order = self.client.updateOrder(gRPC_store_inventory_pb2.UpdateOrderInfo(id_number=id_number, 
                                                                                 destination=destination, 
                                                                                 date=date, 
                                                                                 is_shipped=is_shipped, 
                                                                                 is_paid=is_paid))
        print(order)


    def addProductsToOrder(self, id_number, products):
        product_list = self.get_list_of_products(products)
        order = self.client.addProductsToOrder(gRPC_store_inventory_pb2.AddToOrder(id_number=id_number, products=product_list))
        print(order)


    def removeProductsFromOrder(self, id_number, products):
        product_list = self.get_list_of_products(products)
        order = self.client.removeProductsFromOrder(gRPC_store_inventory_pb2.RemoveFromOrder(id_number=id_number, products=product_list))
        print(order)


    def listOrders(self, is_shipped, is_paid):
        list_of_orders = list(self.client.listOrders(gRPC_store_inventory_pb2.OrderStatus(is_shipped=is_shipped, is_paid=is_paid)))
        print(list_of_orders)

