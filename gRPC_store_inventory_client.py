import grpc
import gRPC_store_inventory_pb2
import gRPC_store_inventory_pb2_grpc

CHANNEL = grpc.insecure_channel('localhost:50052')


class grpcStoreInventoryClient:

    def __init__(self):
        self.client = gRPC_store_inventory_pb2_grpc.ProductInventoryStub(CHANNEL)

    
    def addProduct(self, name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        product_id = self.client.addProduct(name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock)
        print(product_id)


    def getProductById(self, id_number):
        product = self.client.getProduct(id_number)
        print(product)


    def getProductByName(self, name):
        product = self.client.getProduct('', name)
        print(product)


    def updateProductById(self, id_number, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        product = self.client.updateProduct(id_number, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock)
        print(product)


    def updateProductByName(self, name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        product = self.client.updateProduct('', name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock)
        print(product)


    def listProducts(self, manufacturer, in_stock):
        list_of_products = self.client.listProducts(in_stock, manufacturer)
        print(list_of_products)


    def addOrder(self, destination, date, products, is_shipped, is_paid):
        order_id = self.client.addOrder(destination, date, products, is_shipped, is_paid)
        print(order_id)


    def getOrder(self, id_number):
        order = self.client.getOrder(id_number)
        print(order)


    def updateOrder(self, id_number, destination, date, is_shipped, is_paid):
        order = self.client.updateOrder(id_number, destination, date, is_shipped, is_paid)
        print(order)


    def addProductsToOrder(self, id_number, products):
        order = self.client.addProductsToOrder(id_number, products)
        print(order)

    def removeProductsFromOrder(self, id_number, products):
        order = self.client.removeProductsFromOrder(id_number, products)
        print(order)


    def listOrders(self, is_shipped, is_paid):
        list_of_orders = self.client.listOrders(is_shipped, is_paid)
        print(list_of_orders)

    # CHANNEL.close()
