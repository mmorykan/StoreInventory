from xmlrpc.server import DocXMLRPCServer
import store_inventory_shared_data
from concurrent import futures
import uuid
import store_inventory_shared_data


#product info is a dictionary 
#** makes a dictionary of those fields

class XMLProductInventory():
    """
    Class for XMLRPC server and methods
    Server is run from store_inventory_shared_data.py 
    """


    def __init__(self):
        """
        Initializes the inventory object for the shared database
        """
        self.shared_database = store_inventory_shared_data.Inventory()


    with DocXMLRPCServer(("", 8000)) as server:
        server.register_introspective_functions()
        server.register_multicall_functions()

        #UpdateProductFields()

        @server.register_function()
        def add_product(self, id_number, name, description, manufacturer, wholesale_cost, sale_cost, stock):
            """
            Adds a product to the product id and name databases as well as obtains a unique id for the new product
            Returns a product id            
            """
            self.shared_database.add_product(name=name, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, amount_in_stock=stock)


            
        @server.register_function()
        def getProduct(self, identifier):
            """
            Returns the current product based on product id or name
            Returns a product
            """
            self.shared_database.getProductByIDorName(identifier)
            

        @server.register_function()
        def updateProduct(self, id_number, name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
            """
            Update the specified fields for the given project. Can update every field except product id and name
            Returns a product
            """
            product = self.shared_database.update_product(id_number=id_number, name=name, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, amount_in_stock=amount_in_stock)
            return product
            
                 


        @server.register_function()
        def listProducts(self, in_stock, manufacturer):
            """
            Lists all total products or just the products in stock and/or produced by a specified manufacturer
            Yields all appropriate products
            """
            self.shared_database.list_products(in_stock, manufacturer)
            

        #UpdateOrderFields()


        @server.register_function()
        def subtract_product_stock(self, list_of_product_demand):
            """
            Subtracts a product from the stock database
            """
            self.shared_database.subtract_product_stock(list_of_product_demand)

        @server.register_function()
        def add_product_stock(self):
            """
            Add a product to the stock database
            """
            self.shared_database.add_product()


        @server.register_function()
        def addOrder(self, id_number, destination, date, products, is_paid, is_shipped):
            """
            Add an order which contains a destination, date, list of products and counts, shipped status, and paid status
            Returns an order id
            """
            self.shared_database.add_order()

        @server.register_function()
        def getOrder(self, id_number):
            """
            Receive an order based on the specified id value
            Returns an order
            """
            self.shared_database.get_order(id_number)



        @server.register_function()
        def updateOrder(self, id_number, destination, date, is_paid, is_shipped):
            """
            Updates the specified fields for an order.
            Can update destination, date, shipped status, and paid status
            Returns an order
            """
            self.shared_database.update_order()



        @server.register_function()
        def addProductsToOrder(self, id_number, product_list):
            """
            Add products to an existing order or increase the amounts of existing products already in the order
            Returns an order
            """
            self.shared_database.add_products_to_order(id_number, product_list)
            



        @server.register_function()
        def removeProductsFromOrder(self, id_number, product_list):
            """
            Removes products from an order specified by the order id or decrease the amounts of existing products within the order
            Returns an order
            """
            self.shared_database.remove_products_from_order(id_number, product_list)



        @server.register_function()
        def list_orders(self, is_shipped, is_paid):
            """
            Lists all the orders based on shipped status and paid status
            Yields all appropriate orders
            """   
            self.shared_database.list_orders(is_shipped, is_paid)
            



    server.serve_forever()
