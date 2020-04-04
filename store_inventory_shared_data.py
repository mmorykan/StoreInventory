from concurrent import futures
import grpc
import uuid
import store_inventory_server
# import xml server
import store_inventory_pb2
import store_inventory_pb2_grpc

# Need the argparse between clients
class Inventory:
    """
    All shared utility functions for both gRPC and XML-RPC servers and their inventory database
    This file runs both servers and saves the database on termination
    """

    product_id_database = {}
    product_name_database = {}
    order_database = {}

    def invalid_product(self, name):
        """
        Used to check if a product with this name already exists
        """
        return name in self.product_name_database

    def getProductByIDorName(self, id_number, name):
        """
        Determines which database to use to access the product based on given id or name and the gets the product
        """
        if id_number:
            product = self.getProductByID(id_number)
        else:
            product = self.getProductByName(name)
        return product

    def getProductByID(self, id_number):
        """
        returns the current product from the product id database
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
            return ''
        else:
            product_info['id_number'] = id_number
            self.product_id_database[id_number] = product_info
            self.product_name_database[product_info['name']] = product_info
            return id_number

    def update_product(self, **product_info):
        """
        Updates any given field for a product except the products id number and name
        """
        product = self.getProductByIDorName(product_info['id_number'], product_info['name'])
        
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
        self.product_id_database[product['name']] = product
        return product


    def list_products(self, in_stock, manufacturer):
        """
        List all products based on whether or not they are in stock and/or the manufacturer or just list all total products
        """
        product_list = []
        if in_stock == 1 and manufacturer:
            for product in self.product_id_database.values():
                if product['amount_in_stock'] > 0 and product['manufacturer'] == manufacturer:
                    product_list.append(product)
        elif in_stock == 1:
            for product in self.product_id_database.values():
                if product['amount_in_stock'] > 0:
                    product_list.append(product)
        elif in_stock == -1 and manufacturer:
            for product in self.product_id_database.values():
                if product['amount_in_stock'] == 0 and product['manufacturer'] == manufacturer:
                    product_list.append(product)
        elif in_stock == -1:
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



def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    store_inventory_pb2_grpc.add_ProductInventoryServicer_to_server(store_inventory_server.ProductInventory(), server)    

    server.add_insecure_port('[::]:50052')    
    server.start()

    # Run XMl
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        # Remember to pickle the database to a file
        pass

        
if __name__ == '__main__':
    main()
