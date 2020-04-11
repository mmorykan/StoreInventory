
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


    def determine_successful_connection(self):
        return True


    def get_list_of_products(self, products):
        """
        Converts a list of products and their quantities from the command line to a list of dictionaries
        """
        list_of_products = []
        for product_id in range(0, len(products) - 1, 2):
            print(product_id)
            product_dict = {'id_number': products[product_id], 'number_of_product': int(products[product_id + 1])}
            list_of_products.append(product_dict)

        return list_of_products


    def addProduct(self, name, description='', manufacturer='', wholesale_cost=-1, sale_cost=-1, stock=0):
        """
        Adds a product to the product id and name databases as well as obtains a unique id for the new product
        Returns a product id            
        """
        valid_id = self.shared_database.add_product(name=name, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, amount_in_stock=stock)
        if valid_id:
            return valid_id
        else:
            return "A product with that name already exists"

        
    def getProduct(self, id_number='', name=''):
        """
        Returns the current product based on product id or name
        Returns a product
        """
        return self.shared_database.getProductByIDorName({'id_number': id_number, 'name': name})
         

    def updateProduct(self, id_number, name, descriptionn, manufacturer, wholesale_cost, sale_cost, amount_in_stock):
        """
        Update the specified fields for the given project. Can update every field except product id and name
        Returns a product
        """
        product = self.shared_database.update_product(id_number=id_number, name=name, description=descriptionn, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, amount_in_stock=amount_in_stock)
        return product
        

    def listProducts(self, in_stock, manufacturer):
        """
        Lists all total products or just the products in stock and/or produced by a specified manufacturer
        Yields all appropriate products
        """
        if in_stock is None:
            in_stock = 0
        elif in_stock == 'True':
            in_stock = 1
        else:
            in_stock = -1
        return self.shared_database.list_products(in_stock, manufacturer)
        

    def addOrder(self, destination, date, product_list, is_paid, is_shipped):
        """
        Add an order which contains a destination, date, list of products and counts, shipped status, and paid status
        Returns an order id
        """

        list_of_products = self.get_list_of_products(product_list)
        print(list_of_products)
        return self.shared_database.add_order(destination=destination, date=date, products=list_of_products, is_paid=is_paid, is_shipped=is_shipped)


    def getOrder(self, id_number):
        """
        Receive an order based on the specified id value
        Returns an order
        """
        return self.shared_database.get_order(id_number)


    def updateOrder(self, id_number, destination, date, is_paid, is_shipped):
        """
        Updates the specified fields for an order.
        Can update destination, date, shipped status, and paid status
        Returns an order
        """
        return self.shared_database.update_order(id_number = id_number, destination = destination, date = date, is_paid = is_paid, is_shipped = is_shipped)


    def addProductsToOrder(self, id_number, product_list):
        """
        Add products to an existing order or increase the amounts of existing products already in the order
        Returns an order
        """
        list_of_products = self.get_list_of_products(product_list)
        return self.shared_database.add_products_to_order(id_number, list_of_products)
        

    def removeProductsFromOrder(self, id_number, product_list):
        """
        Removes products from an order specified by the order id or decrease the amounts of existing products within the order
        Returns an order
        """
        list_of_products = self.get_list_of_products(product_list)
        return self.shared_database.remove_products_from_order(id_number, list_of_products)


    def listOrders(self, is_shipped, is_paid):
        """
        Lists all the orders based on shipped status and paid status
        Yields all appropriate orders
        """   
        return self.shared_database.list_orders(is_shipped, is_paid)
        
