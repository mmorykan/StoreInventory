from concurrent import futures
import grpc
import uuid
import gRPC_store_inventory_server
import XML_store_inventory_server
import gRPC_store_inventory_pb2_grpc
from xmlrpc.server import DocXMLRPCServer
import pickle
import os


class Inventory:
    """
    All shared utility functions for both gRPC and XML-RPC servers and their inventory databases
    This file runs both servers and saves the database in store_inventory_database.bin on termination
    """

    def __init__(self):
        """
        Initializes the product id and name databases as well as the order database
        Creates the null product and null order for returning when the real order or product could not be found
        All databases are shared between both servers
        """
        self.product_id_database = {}
        self.product_name_database = {}
        self.order_database = {}
        self.null_product = {'id_number': 'null product', 'name': 'Product does not exist', 'description': 'Product does not exist', 'manufacturer': 'Product does not exist', 'wholesale_cost': -1, 'sale_cost': -1, 'amount_in_stock': -1}
        self.null_order = {'id_number': 'null order', 'destination': 'Order does not exist', 'date': 'Order does not exist', 'products': [], 'is_shipped': 'F', 'is_paid': 'F'}


    def invalid_product(self, name):
        """
        Used to check if a product with this name already exists
        """
        return name in self.product_name_database


    def getProductByIDorName(self, identifier):
        """
        Determines which database to use to access the product based on given id or name and then returns the product
        """
        if identifier['id_number']:
            product = self.getProductByID(identifier['id_number'])
        else:
            product = self.getProductByName(identifier['name'])

        return product


    def getProductByID(self, id_number):
        """
        Returns the current product from the product id database
        If the requested product could not be found, the null product is returned
        """
        try:
            product = self.product_id_database[id_number]
        except:
            product = self.null_product

        return product


    def getProductByName(self, name):
        """
        returns the current product from the product name database
        If the requested product could not be found, the null product is returned
        """
        try:
            product = self.product_name_database[name]
        except:
            product = self.null_product

        return product


    def add_product(self, **product_info):
        """
        Adds a product to the product id database and name database as well as assigns the new product a unique id
        Returns the null product if the name is already taken by another product, otherwise, returns the products new id value
        """
        id_number = str(uuid.uuid4())
        if self.invalid_product(product_info['name']):
            return self.null_product['id_number']
        else:
            product_info['id_number'] = id_number
            self.product_id_database[id_number] = product_info
            self.product_name_database[product_info['name']] = product_info
            return id_number


    def update_product(self, **product_info):
        """
        Updates any given field for a product except the products id number and name
        Returns the null product if requested product could not be found
        """
        if product_info['id_number']:
            product = self.getProductByID(product_info['id_number'])
        else:
            product = self.getProductByName(product_info['name'])
        
        if product == self.null_product:
            return product

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

        else:
            for product in self.product_id_database.values():
                product.append(product)

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

            else:
                products_to_delete.append(product_and_demand)

        for product in products_to_delete:
            list_of_product_demand.remove(product)

        return list_of_product_demand


    def add_order(self, **order_info):
        """
        Assigns an id value to an order
        Creates the order with destination, date, list of products and counts, shipped status, and paid status
        Creates the order even if products are invalid
        Returns the order id value
        """
        id_number = str(uuid.uuid4())
        order_info['id_number'] = id_number
        order_info['products'] = self.subtract_product_stock(order_info['products'])
        self.order_database[id_number] = order_info
        return id_number


    def get_order(self, id_number):
        """
        Returns the order with the specified id value
        If the requested order could not be found, the null order is returned
        """
        try:
            order = self.order_database[id_number]
        except:
            order = self.null_order

        return order


    def update_order(self, **order_info):
        """
        Updates the given fields of the order. 
        Cannot update the products of an order.
        Returns the order
        If the requested order could not be found, the null order is returned
        """
        try:
            order = self.get_order(order_info['id_number'])
        except:
            return self.null_order

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
        If the requested order could not be found, the null order is returned
        """
        order = self.get_order(id_number)
        if order == self.null_order:
            return order 

        for product_and_demand in product_list:
            product_found = False

            current_product = self.getProductByIDorName(product_and_demand)
            if current_product == self.null_product:
                continue

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
        If the requested order could not be found, the null order is returned
        """
        products_to_remove = []

        order = self.get_order(id_number)
        if order == self.null_order:
            return order 

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
        List all orders based on shipped status and paid status or all total orders
        Returns a list of orders
        """
        list_of_orders = []

        if is_shipped == '' and is_paid == '':
            for order in self.order_database.values():
                list_of_orders.append(order)
            
        elif is_shipped != '' and is_paid == '':
            for order in self.order_database.values():
                if order['is_shipped'] == is_shipped:
                    list_of_orders.append(order)

        elif is_shipped == '' and is_paid != '':
            for order in self.order_database.values():
                if order['is_paid'] == is_paid:
                    list_of_orders.append(order)

        for order in self.order_database.values():
            if order['is_shipped'] == is_shipped and order['is_paid'] == is_paid:
                list_of_orders.append(order)

        return list_of_orders


    def clear_database(self):
        """
        Completely wipes the the database file
        """
        open('store_inventory_database.bin', 'w').close()


def load_database(store_inventory):
    """
    Loads the database from the store_inventory_database.bin file using pickle
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
    The databases are stored in a list when saving them in the store_inventory_database.bin file
    We save the database as bytes because this is more efficient than human readable format
    """
    with open('store_inventory_database.bin', 'wb') as save_database:
            pickle.dump([store_inventory.product_id_database, store_inventory.product_name_database, store_inventory.order_database], save_database)


def main():
    """
    Starts gRPC and XML-RPC servers on different ports and loads the databases if they are pre-existing
    Saves the databases in store_inventory_database.bin on termination
    """
    store_inventory = Inventory()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    gRPC_store_inventory_pb2_grpc.add_ProductInventoryServicer_to_server(gRPC_store_inventory_server.ProductInventory(store_inventory), grpc_server)    
    grpc_server.add_insecure_port('[::]:50052')    
    grpc_server.start()

    with DocXMLRPCServer(('', 8000)) as xml_server:
        xml_server.register_instance(XML_store_inventory_server.XMLProductInventory(store_inventory))
        
        load_database(store_inventory)

        try:
            xml_server.serve_forever()
            grpc_server.wait_for_termination()
        except KeyboardInterrupt:
            save_database(store_inventory)
    

if __name__ == '__main__':
    main()

