from concurrent import futures
import grpc
import uuid
import store_inventory_pb2
import store_inventory_pb2_grpc

class ProductInventory(store_inventory_pb2_grpc.ProductInventoryServicer):
    product_id_database = {}
    product_name_database = {}
    order_database = {}


    def same_name(self):
        pass


    def getProductByIDorName(self, request, context):
        if request.id_number:
            return self.getProductByID(request.id_number)
        else:
            return self.getProductByName(request.name)


    def getProductByID(self, id_number):
        return self.product_id_database[id_number]


    def getProductByName(self, name):
        return self.product_name_database[name]
        

    def addProduct(self, request, context):
        id_number = str(uuid.uuid4())
        # for key in self.product_id_database:
        #     if request.name == self.product_database[key].name:
        #         print('cant have same name') 
                # Make so that products cant have same name
        name = request.name
        description = request.description
        manufacturer = request.manufacturer
        wholesale_cost = request.wholesale_cost
        sale_cost = request.sale_cost
        stock = request.stock
        self.product_id_database[id_number] = store_inventory_pb2.Product(name=name, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, stock=stock)
        self.product_name_database[name] = store_inventory_pb2.Product(id_number=id_number, description=description, manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, stock=stock)
        # print(self.product_id_database[id_number])
        # print(self.product_name_database[name])
        return store_inventory_pb2.ProductID(id_number=id_number, name=name)


    def getProduct(self, request, context):
        return self.getProductByIDorName(request, context)


    def updateProduct(self, request, context):
        product = self.getProductByIDorName(request, context)
        if request.description:
            product.description = request.description
        if request.manufacturer:
            product.manufacturer = request.manufacturer
        if request.wholesale_cost:
            product.wholesale_cost = request.wholesale_cost
        if request.sale_cost:
            product.sale_cost = request.sale_cost
        if request.stock:
            product.stock = request.stock
        return product
    

    def listProducts(self, request, context):
        if request.in_stock and request.manufacturer:
            for product in self.product_id_database.values():
                if product.stock > 0 and product.manufacturer == request.manufacturer:
                    yield product
        elif request.manufacturer:
            for product in self.product_id_database.values():
                if product.manufacturer == request.manufacturer:
                    yield product
        elif request.in_stock:
             for product in self.product_id_database.values():
                if product.stock > 0:
                    yield product
        else:
            for product in self.product_id_database.values():
                yield product


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

            if current_product_by_id.stock >= product_demand.num_of_product:
                print('inside if statemtn')
                self.product_id_database[current_product_by_name.id_number].stock -= product_demand.num_of_product
                print('inbetween')
                self.product_name_database[current_product_by_id.name].stock -= product_demand.num_of_product
                print('after efvetyting')
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
        if request.is_paid is not None:
            order.is_paid = request.is_paid
        if request.is_shipped is not None:
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
        # for order_id, order in self.order_database.items():
        #     if current_order == order:
        #         current_order_id = order_id

        current_order.products.extend(self.subtract_product_stock(request.products))
        self.order_database[request.id_number] = current_order 
        return current_order


    def removeProductsFromOrder(self, request, context):
        """Remember to add the stock back in"""
        elements_to_remove = []
        order = self.getOrderHelper(request, context)

        for product_and_demand in request.products:
            if product_and_demand.product.id_number:
                current_product_by_id = self.getProductByID(product_and_demand.product.id_number)
                current_product_by_name = self.getProductByName(current_product_by_name.name)
            elif product_and_demand.product.name:
                current_product_by_name = self.getProductByName(product_and_demand.product.name)
                current_product_by_id = self.getProductByID(current_product_by_name.product.id_number)


            for prod in order.products:
                if prod.product.name == current_product_by_id.name:
                    if prod.num_of_product > product_and_demand.num_of_product:
                        prod.num_of_product -= product_and_demand.num_of_product
                        self.product_id_database[current_product_by_name.id_number].stock += product_and_demand.num_of_product
                        self.product_name_database[current_product_by_id.name].stock += product_and_demand.num_of_product
                    elif prod.num_of_product == product_and_demand.num_of_product:
                        self.product_id_database[current_product_by_name.id_number].stock += product_and_demand.num_of_product
                        self.product_name_database[current_product_by_id.name].stock += product_and_demand.num_of_product
                        elements_to_remove.append(prod)

        order.products = [product for product in order.products if product not in elements_to_remove]
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

