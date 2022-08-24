import sys
from msrest.exceptions import HttpOperationError
from azure.iot.hub import IoTHubRegistryManager

CONNECTION_STRING = "HostName=wonshub.azure-devices.net;SharedAccessKeyName=serviceAndRegistryReadWrite;SharedAccessKey=Q/WvHylQAtoTuXLFumyKzxW8bw04OmR86zQCY8M97X0="
DEVICE_ID = "myFirstDevice"
MODULE_ID = "myFirstModule"

try:
    # RegistryManager
    iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

    try:
        # CreateDevice - let IoT Hub assign keys
        primary_key = ""
        secondary_key = ""
        device_state = "enabled"
        new_device = iothub_registry_manager.create_device_with_sas(
            DEVICE_ID, primary_key, secondary_key, device_state
        )
    except HttpOperationError as ex:
        if ex.response.status_code == 409:
            # 409 indicates a conflict. This happens because the device already exists.
            new_device = iothub_registry_manager.get_device(DEVICE_ID)
        else:
            raise

    print("device <" + DEVICE_ID +
          "> has primary key = " + new_device.authentication.symmetric_key.primary_key)

    try:
        # CreateModule - let IoT Hub assign keys
        primary_key = ""
        secondary_key = ""
        managed_by = ""
        new_module = iothub_registry_manager.create_module_with_sas(
            DEVICE_ID, MODULE_ID, managed_by, primary_key, secondary_key
        )
    except HttpOperationError as ex:
        if ex.response.status_code == 409:
            # 409 indicates a conflict. This happens because the module already exists.
            new_module = iothub_registry_manager.get_module(DEVICE_ID, MODULE_ID)
        else:
            raise

    print("device/module <" + DEVICE_ID + "/" + MODULE_ID +
          "> has primary key = " + new_module.authentication.symmetric_key.primary_key)

except Exception as ex:
    print("Unexpected error {0}".format(ex))
except KeyboardInterrupt:
    print("IoTHubRegistryManager sample stopped")