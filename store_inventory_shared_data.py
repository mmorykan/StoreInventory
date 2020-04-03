from concurrent import futures
import grpc
import uuid
import store_inventory_server
# import xml
import store_inventory_pb2
import store_inventory_pb2_grpc



""" Helper functions"""














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