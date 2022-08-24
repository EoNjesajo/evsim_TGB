import time
from azure.iot.device import IoTHubModuleClient

import sys
from time import sleep
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult

CONNECTION_STRING = "HostName=wonshub.azure-devices.net;DeviceId=maze;SharedAccessKey=SxpLYy/45qe50l9C3ZoKoL7kSpBCqDrH7LfbeH/Tvb4="

IOTHUB_CONNECTION_STRING = "HostName=wonshub.azure-devices.net;SharedAccessKeyName=serviceAndRegistryRead;SharedAccessKey=Hx96nI5ZXPKa4xRT80nAA5hpgmYzwxZzO7vwl8sMChw="
DEVICE_ID = "maze"

def iothub_service_sample_run():
    try:
        iothub_registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)


        new_tags = {
                'map' : [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 3, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]
            }

        twin = iothub_registry_manager.get_twin(DEVICE_ID)
        twin_patch = Twin(tags=new_tags, properties= TwinProperties(desired={'power_level' : 1}))
        twin = iothub_registry_manager.update_twin(DEVICE_ID, twin_patch, twin.etag)

        sleep(1)

        query_spec = QuerySpecification(query="SELECT tags FROM devices WHERE is_defined(tags.values)")
        query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)

        for twin in query_result.items:
            data_dic  = eval(str(twin))
    
    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("IoT Hub Device Twin service sample stopped")


def create_client():
    # Instantiate client
    client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)

    # Define behavior for receiving twin desired property patches
    def twin_patch_handler(twin_patch):
        print("Twin patch received:")
        print(twin_patch)
    

    try:
        # Set handlers on the client
        client.on_twin_desired_properties_patch_received = twin_patch_handler
    except:
        # Clean up in the event of failure
        client.shutdown()

    return client

def main():
   
    client = create_client()


    iothub_service_sample_run()
    try:
        # Update reported properties with cellular information
        print ( "Sending data as reported property..." )
        reported_patch = {"connectivity": "cellular"}
        client.patch_twin_reported_properties(reported_patch)
        print ( "Reported properties updated" )

        # Wait for program exit
        while True:
            time.sleep(1000000)
    except KeyboardInterrupt:
        print ("IoT Hub Device Twin device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()

if __name__ == '__main__':
    main()