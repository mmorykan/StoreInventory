from concurrent import futures
import grpc
import uuid
import store_inventory_pb2
import store_inventory_pb2_grpc
import store_inventory_shared_data

class ProductInventory(store_inventory_pb2_grpc.ProductInventoryServicer):
    product_id_database = {}
    product_name_database = {}
    order_database = {}
    shared_database = store_inventory_shared_data.Inventory()

    def update_product_fields(self, product):
        """
        Creates the gRPC product object from the given product
        """
        return store_inventory_pb2.Product(id_number=product['id_number'], name=product['name'], description=product['description'], manufacturer=product['manufacturer'], wholesale_cost=product['wholesale_cost'], sale_cost=product['sale_cost'], amount_in_stock=product['amount_in_stock'])

    def addProduct(self, request, context):
        """
        Adds a product to the product id and name databases as well as obtains a unique id for the new product and returns a product ID
        """
        valid_id = self.shared_database.add_product(name=request.name, description=request.description, manufacturer=request.manufacturer, wholesale_cost=request.wholesale_cost, sale_cost=request.sale_cost, amount_in_stock=request.amount_in_stock)
        if valid_id:
            return store_inventory_pb2.ProductID(id_number=valid_id, name=request.name)


    def getProduct(self, request, context):
        """
        Returns the current product based on product id or name
        """
        product = self.shared_database.getProductByIDorName(request.id_number, request.name)
        return self.update_product_fields(product)

    def updateProduct(self, request, context):
        """
        Update the specified fields for the given project. Can update every field except product id and name
        """
        product = self.shared_database.update_product(id_number=request.id_number, name=request.name, description=request.description, manufacturer=request.manufacturer, wholesale_cost=request.wholesale_cost, sale_cost=request.sale_cost, amount_in_stock=request.amount_in_stock)
        return self.update_product_fields(product)    

    def listProducts(self, request, context):
        """
        Lists all total products or just the products in stock and/or produced by a specified manufacturer
        """
        product_list = self.shared_database.list_products(request.in_stock, request.manufacturer)
        for product in product_list:
            yield self.update_product_fields(product)


        ################################################################


    def subtract_product_stock(self, product_list): # Fixxxx
        products = []
        print(product_list)
        for product_demand in product_list:
            print(product_demand)
            if product_demand.product.id_number:
                print(product_demand.product.id_number)
                current_product_by_id = self.getProductByID(product_demand.product.id_number)
                current_product_by_name = self.getProductByName(current_product_by_id.name)
            elif product_demand.product.name:
                current_product_by_name = self.getProductByName(product_demand.product.name)
                current_product_by_id = self.getProductByID(current_product_by_name.id_number)


            print('stock variable')

            if current_product_by_id.stock >= product_demand.num_of_product:
                print('inside if statemtn')
                self.product_id_database[current_product_by_name.id_number].stock -= product_demand.num_of_product
                print('inbetween')
                self.product_name_database[current_product_by_id.name].stock -= product_demand.num_of_product
                print('after everything')
                products.append(product_demand)

        return products


    def add_product_stock(self, products_to_remove): # Fixxxxxx
        pass


    def addOrder(self, request, context):
        id_number = str(uuid.uuid4())
        destination = request.destination
        date = request.date
        print(request.products)
        products = self.subtract_product_stock(request.products)
        is_paid = request.is_paid
        is_shipped = request.is_shipped
        
        self.order_database[id_number] = store_inventory_pb2.Order(id_number=id_number, 
                                                                   destination=destination, 
                                                                   date=date,
                                                                   products=products, 
                                                                   is_paid=is_paid, 
                                                                   is_shipped=is_shipped)
        return store_inventory_pb2.OrderID(id_number=id_number)


    def getOrderHelper(self, request, context):
        return self.order_database[request.id_number]

    
    def getOrder(self, request, context):
        return self.getOrderHelper(request, context)


    def updateOrderHelper(self, request, context):
        order = self.getOrderHelper(request, context)
        if request.destination:
            order.destination = request.destination
        if request.date:
            order.date = request.date
        if request.is_paid:
            order.is_paid = request.is_paid
        if request.is_shipped:
            order.is_shipped = request.is_shipped

        self.order_database[request.id_number] = store_inventory_pb2.Order(destination=order.destination, 
                                                                           date=order.date,
                                                                           is_paid=order.is_paid,
                                                                           is_shipped=order.is_shipped)
        return order


    def updateOrder(self, request, context):
        return self.updateOrderHelper(request, context)


    def addProductsToOrder(self, request, context):
        current_order = self.getOrderHelper(request, context)
       
       # Fiiiiixxxxxxx
        products_to_add = self.subtract_product_stock(request.products)
        for i in range(len(products_to_add)):
            products_to_add[i].num_of_product += current_order.products[i].num_of_product

        current_order.products.extend(products_to_add)
        self.order_database[request.id_number] = current_order 
        return current_order


    def removeProductsFromOrder(self, request, context):
        """Remember to add the stock back in"""
        elements_to_remove = []
        order = self.getOrderHelper(request, context)

        for product_and_demand in request.products:
            if product_and_demand.product.id_number:
                current_product_by_id = self.getProductByID(product_and_demand.product.id_number)
                current_product_by_name = self.getProductByName(current_product_by_id.name)
            elif product_and_demand.product.name:
                current_product_by_name = self.getProductByName(product_and_demand.product.name)
                current_product_by_id = self.getProductByID(current_product_by_name.id_number)

            for prod in order.products:
                if prod.product.id_number == current_product_by_name.id_number:
                    if prod.num_of_product > product_and_demand.num_of_product:
                        prod.num_of_product -= product_and_demand.num_of_product
                        self.product_id_database[current_product_by_name.id_number].stock += product_and_demand.num_of_product
                        self.product_name_database[current_product_by_id.name].stock += product_and_demand.num_of_product
                    elif prod.num_of_product == product_and_demand.num_of_product:
                        self.product_id_database[current_product_by_name.id_number].stock += product_and_demand.num_of_product
                        self.product_name_database[current_product_by_id.name].stock += product_and_demand.num_of_product
                        elements_to_remove.append(prod)

        for product in elements_to_remove:
            order.products.remove(product)
                
        self.order_database[request.id_number] = order

        return order


    def listOrders(self, request, context):
        if request.is_shipped == 1 and request.is_paid == 1:
            for order in self.order_database.values():
                if order.is_shipped and order.is_paid:
                    yield order

        elif request.is_shipped == 1:
            for order in self.order_database.values():
                if order.is_shipped:
                    yield order

        elif request.is_paid == 1:
            for order in self.order_database.values():
                if order.is_paid:
                    yield order

        elif request.is_shipped == 1 and request.is_paid == -1:
            for order in self.order_database.values():
                if order.is_shipped and not request.is_paid:
                    yield order

        elif request.is_shipped == -1 and request.is_paid == 1:
            for order in self.order_database.values():
                if not order.is_paid and request.is_shipped:
                    yield order

        elif request.is_shipped == -1 and request.is_paid == -1:
            print('not everyting')
            for order in self.order_database.values():
                if not order.is_shipped and not order.is_paid:
                    yield order

        else:
            print('made it here')
            for order in self.order_database.values():
                yield order


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    
    store_inventory_pb2_grpc.add_ProductInventoryServicer_to_server(ProductInventory(), server)    

    server.add_insecure_port('[::]:50052')    
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        # Remember to pickle the database to a file
        pass


if __name__ == '__main__':    
    main()

