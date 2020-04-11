from concurrent import futures
import grpc
import uuid
import gRPC_store_inventory_server
import XML_store_inventory_server
import gRPC_store_inventory_pb2_grpc
from xmlrpc.server import DocXMLRPCServer
import pickle


class Inventory:
    """
    All shared utility functions for both gRPC and XML-RPC servers and their inventory database
    This file runs both servers and saves the database on termination
    """


    def __init__(self):
        """
        Initializes the product id and name databases as well as the order database
        All databases are shared between both servers
        """
        self.product_id_database = {}
        self.product_name_database = {}
        self.order_database = {}


    def invalid_product(self, name):
        """
        Used to check if a product with this name already exists
        """
        return name in self.product_name_database


    def getProductByIDorName(self, identifier):
        """
        Determines which database to use to access the product based on given id or name and the gets the product
        """
        if identifier['id_number']:
            product = self.getProductByID(identifier['id_number'])
        else:
            product = self.getProductByName(identifier['name'])
        return product


    def getProductByID(self, id_number):
        """
        Returns the current product from the product id database
        """
        product = self.product_id_database[id_number]
        return product


    def getProductByName(self, name):
        """
        returns the current product from the product name database
        """
        product = self.product_name_database[name]
        return product


    def add_product(self, **product_info):
        """
        Adds a product to the product id database and name database as well as assigns the new product a unique id
        """
        id_number = str(uuid.uuid4())
        if self.invalid_product(product_info['name']):
            return 
        else:
            product_info['id_number'] = id_number
            self.product_id_database[id_number] = product_info
            self.product_name_database[product_info['name']] = product_info
            return id_number


    def update_product(self, **product_info):
        """
        Updates any given field for a product except the products id number and name
        """
        if product_info['id_number']:
            product = self.getProductByID(product_info['id_number'])
        else:
            product = self.getProductByName(product_info['name'])
        
        if product_info['description']:
            product['description'] = product_info['description']
        if product_info['manufacturer']:
            product['manufacturer'] = product_info['manufacturer']
        if product_info['wholesale_cost']:
            product['wholesale_cost'] = product_info['wholesale_cost']
        if product_info['sale_cost']:
            product['sale_cost'] = product_info['sale_cost']
        if product_info['amount_in_stock']:
            product['amount_in_stock'] = product_info['amount_in_stock']

        self.product_id_database[product['id_number']] = product
        return product


    def list_products(self, in_stock, manufacturer):
        """
        List all products based on whether or not they are in stock and/or the manufacturer or just list all total products
        """
        product_list = []
        if in_stock == 'T' and manufacturer:
            for product in self.product_id_database.values():
                if product['amount_in_stock'] > 0 and product['manufacturer'] == manufacturer:
                    product_list.append(product)
        elif in_stock == 'T':
            for product in self.product_id_database.values():
                if product['amount_in_stock'] > 0:
                    product_list.append(product)
        elif in_stock == 'F' and manufacturer:
            for product in self.product_id_database.values():
                if product['amount_in_stock'] == 0 and product['manufacturer'] == manufacturer:
                    product_list.append(product)
        elif in_stock == 'F':
            for product in self.product_id_database.values():
                if product['amount_in_stock'] == 0:
                    product_list.append(product)
        elif manufacturer:
            for product in self.product_id_database.values():
                if product['manufacturer'] == manufacturer:
                    product_list.append(product)
        else:
            for product in self.product_id_database.values():
                product_list.append(product)

        return product_list


    def subtract_product_stock(self, list_of_product_demand):
        """
        Subtracts stock from the current product that is being added to an order
        Does not add a product to an order if the demand is greater than the current stock of the product
        """
        products_to_delete = []
        for product_and_demand in list_of_product_demand:
            current_product = self.getProductByID(product_and_demand['id_number'])
            if current_product['amount_in_stock'] >= product_and_demand['number_of_product']:
                current_product['amount_in_stock'] -= product_and_demand['number_of_product']
                self.product_id_database[current_product['id_number']] = current_product
                self.product_name_database[current_product['name']] = current_product
            else:
                products_to_delete.append(product_and_demand)
        for product in products_to_delete:
            list_of_product_demand.remove(product)

        return list_of_product_demand


    def add_order(self, **order_info):
        """
        Assigns an id value to an order
        Creates the order with destination, date, list of products and counts, shipped status, and paid status
        Returns the order id value
        """
        id_number = str(uuid.uuid4())
        order_info['id_number'] = id_number
        order_info['products'] = self.subtract_product_stock(order_info['products'])
        self.order_database[id_number] = order_info
        return id_number


    def get_order(self, id_number):
        """
        Returns the order with the specified id
        """
        return self.order_database[id_number]


    def update_order(self, **order_info):
        """
        Updates the given fields of the order. 
        Cannot update the products of an order.
        Returns the order
        """
        order = self.get_order(order_info['id_number'])
        if order_info['destination']:
            order['destination'] = order_info['destination']
        if order_info['date']:
            order['date'] = order_info['date']
        if order_info['is_shipped']:
            order['is_shipped'] = order_info['is_shipped']
        if order_info['is_paid']:
            order['is_paid'] = order_info['is_paid']
        
        self.order_database[order_info['id_number']] = order
        return order


    def add_products_to_order(self, id_number, product_list):
        """
        Add the product list to the order with the given id.
        Updates product stocks
        Returns the order 
        """
        product_found = False
        order = self.get_order(id_number)
        for product_and_demand in product_list:
            current_product = self.getProductByIDorName(product_and_demand)
            if current_product['amount_in_stock'] >= product_and_demand['number_of_product']:
                self.product_id_database[current_product['id_number']]['amount_in_stock'] -= product_and_demand['number_of_product']
                for product in order['products']:
                    if product['id_number'] == current_product['id_number']:
                        product_found = True
                        product['number_of_product'] += product_and_demand['number_of_product']

                if not product_found:
                    order['products'].append({'id_number': current_product['id_number'], 'number_of_product': product_and_demand['number_of_product']})

        return order


    def remove_products_from_order(self, id_number, product_list):
        """
        Removes products or an amount of products from an order
        Updates product stocks
        Returns an order
        """
        products_to_remove = []
        order = self.get_order(id_number)
        for new_product_and_demand in product_list:
            for old_prod_dem in order['products']:
                if old_prod_dem['id_number'] == new_product_and_demand['id_number']:
                    if old_prod_dem['number_of_product'] > new_product_and_demand['number_of_product']:
                        old_prod_dem['number_of_product'] -= new_product_and_demand['number_of_product']
                    elif old_prod_dem['number_of_product'] == new_product_and_demand['number_of_product']:
                        products_to_remove.append(old_prod_dem)

                    self.product_id_database[old_prod_dem['id_number']]['amount_in_stock'] += new_product_and_demand['number_of_product']

        for product_and_demand in products_to_remove:
            order['products'].remove(product_and_demand)

        self.order_database[order['id_number']] = order
        return order


    def list_orders(self, is_shipped, is_paid):
        """
        List all orders based on shipped status and paid status
        Returns a list of orders
        """
        list_of_orders = []

        for order in self.order_database.values():
            if order['is_shipped'] == is_shipped and order['is_paid'] == is_paid:
                list_of_orders.append(order)

        return list_of_orders


def load_database(store_inventory):
    """
    Loads the database from the store_inventory_database.py file using pickle
    If the file is empty, the store_inventory object defaults to empty databases
    """
    with open('store_inventory_database.bin', 'rb') as load_database:
        try:
            product_id_database, product_name_database, order_database = pickle.load(load_database)
            store_inventory.product_id_database = product_id_database
            store_inventory.product_name_database = product_name_database
            store_inventory.order_database = order_database
        except EOFError:
            pass
    

def save_database(store_inventory):
    """
    Saves the database using pickle when the user terminates the server 
    The databases are stored in a list when saving them in the store_inventory_database.py file
    """
    with open('store_inventory_database.bin', 'wb') as save_database:
            pickle.dump([store_inventory.product_id_database, store_inventory.product_name_database, store_inventory.order_database], save_database)


def main():
    """
    Starts gRPC and XML-RPC servers on different ports and loads the databases if they are preexisting
    Saves the databases on termination
    """
    store_inventory = Inventory()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    gRPC_store_inventory_pb2_grpc.add_ProductInventoryServicer_to_server(gRPC_store_inventory_server.ProductInventory(store_inventory), grpc_server)    
    grpc_server.add_insecure_port('[::]:50052')    
    grpc_server.start()

    with DocXMLRPCServer(('', 8000)) as xml_server:
        xml_server.register_introspection_functions()
        xml_server.register_multicall_functions()
        xml_server.register_instance(XML_store_inventory_server.XMLProductInventory(store_inventory))
        
        load_database(store_inventory)

        try:
            xml_server.serve_forever()
            grpc_server.wait_for_termination()
            
        except KeyboardInterrupt:
            save_database(store_inventory)
            pass
        
    
if __name__ == '__main__':
    main()

