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


    def __init__(self, store_inventory):
        """
        Initializes the inventory object for the shared database
        """
        self.shared_database = store_inventory
        print('working')


    # @server.register_function()
    def add_product(self, id_number, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        """
        Adds a product to the product id and name databases as well as obtains a unique id for the new product
        Returns a product id            
        """
        valid_id = self.shared_database.add_product(name=name, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, amount_in_stock=stock)
        if valid_id:
            return valid_id
        else:
            return "A product with that name already exists"

        
    # @server.register_function()
    def getProduct(self, identifier):
        """
        Returns the current product based on product id or name
        Returns a product
        """
        return self.shared_database.getProductByIDorName(identifier)
         

    # @server.register_function()
    def updateProduct(self, id_number, name, description, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        """
        Update the specified fields for the given project. Can update every field except product id and name
        Returns a product
        """
        product = self.shared_database.update_product(id_number=id_number, name=name, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, amount_in_stock=amount_in_stock)
        return product
        

    # @server.register_function()
    def listProducts(self, in_stock, manufacturer):
        """
        Lists all total products or just the products in stock and/or produced by a specified manufacturer
        Yields all appropriate products
        """
        return self.shared_database.list_products(in_stock, manufacturer)
        

    # @server.register_function()
    def addOrder(self, destination, date, products, is_paid, is_shipped):
        """
        Add an order which contains a destination, date, list of products and counts, shipped status, and paid status
        Returns an order id
        """
        # Make sure to configure product list
        return self.shared_database.add_order(destination=destination, date=date, products=products, is_paid=is_paid, is_shipped=is_shipped)


    # @server.register_function()
    def getOrder(self, id_number):
        """
        Receive an order based on the specified id value
        Returns an order
        """
        return self.shared_database.get_order(id_number)


    # @server.register_function()
    def updateOrder(self, id_number, destination, date, is_paid, is_shipped):
        """
        Updates the specified fields for an order.
        Can update destination, date, shipped status, and paid status
        Returns an order
        """
        return self.shared_database.update_order(id_number = id_number, destination = destination, date = date, is_paid = is_paid, is_shipped = is_shipped)


    # @server.register_function()
    def addProductsToOrder(self, id_number, product_list):
        """
        Add products to an existing order or increase the amounts of existing products already in the order
        Returns an order
        """
        # Configure product list
        return self.shared_database.add_products_to_order(id_number, product_list)
        

    # @server.register_function()
    def removeProductsFromOrder(self, id_number, product_list):
        """
        Removes products from an order specified by the order id or decrease the amounts of existing products within the order
        Returns an order
        """
        #Configure product list
        return self.shared_database.remove_products_from_order(id_number, product_list)


    # @server.register_function()
    def list_orders(self, is_shipped, is_paid):
        """
        Lists all the orders based on shipped status and paid status
        Yields all appropriate orders
        """   
        return self.shared_database.list_orders(is_shipped, is_paid)
        
