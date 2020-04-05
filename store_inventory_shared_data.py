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

    def subtract_product_stock(self, list_of_product_demand):
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
        id_number = str(uuid.uuid4())
        order_info['id_number'] = id_number
        order_info['products'] = self.subtract_product_stock(order_info['products'])
        self.order_database[id_number] = order_info
        return id_number

    def get_order(self, id_number):
        return self.order_database[id_number]


    def update_order(self, **order_info):
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
        product_found = False
        order = self.get_order(id_number)
        for product_and_demand in product_list:
            current_product = self.getProductByIDorName(product_and_demand)
            if current_product['amount_in_stock'] >= product_and_demand['number_of_product']:
                self.product_id_database[current_product['id_number']]['amount_in_stock'] -= product_and_demand['number_of_product']
                # self.product_name_database[current_product['name']]['amount_in_stock'] -= product_and_demand['number_of_product']
                for product in order['products']:
                    if product['id_number'] == current_product['id_number']:
                        product_found = True
                        product['number_of_product'] += product_and_demand['number_of_product']

                if not product_found:
                    order['products'].append({'id_number': current_product['id_number'], 'number_of_product': product_and_demand['number_of_product']})

        return order


    def remove_products_from_order(self, id_number, product_list):
        pass



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
