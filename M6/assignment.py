import time
import sys
import os
from os import listdir
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobClient

PATHTOFILE = "/home/pi/edureka_iot_works/M6/files"
CONNECTION_STRING = "HostName=eduhub.azure-devices.net;DeviceId=eduPi;SharedAccessKey=UzxPLCDYYIorfE3gxMQqUZF+3oHgnvsBV089lDtMfMc="

async def store_blob(blob_info, file_name):
    try:
        sas_url = "https://{}/{}/{}{}".format(
            blob_info["hostName"],
            blob_info["containerName"],
            blob_info["blobName"],
            blob_info["sasToken"]
        )

        print("\nUploading file: {} to Azure Storage as blob: {} in container {}\n".format(file_name, blob_info["blobName"], blob_info["containerName"]))

        # Upload the specified file
        with BlobClient.from_blob_url(sas_url) as blob_client:
            with open(file_name, "rb") as f:
                result = blob_client.upload_blob(f, overwrite=True)
                return (True, result)

    except FileNotFoundError as ex:
        # catch file not found and add an HTTP status code to return in notification to IoT Hub
        ex.status_code = 404
        return (False, ex)

    except AzureError as ex:
        # catch Azure errors that might result from the upload operation
        return (False, ex)
    
async def main():
    print ( "IoT Hub file upload sample, press Ctrl-C to exit" )

    conn_str = CONNECTION_STRING
    #file_name = PATH_TO_FILE
    #blob_name = os.path.basename(file_name)
    
    for f in listdir(PATHTOFILE):
        if os.path.isfile(os.path.join(PATHTOFILE, f)):
            try:
                device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

                # Connect the client
                await device_client.connect()
                print(os.path.join(PATHTOFILE, f))
                file_name = os.path.join(PATHTOFILE, f)
                blob_name = os.path.basename(file_name)

                # Get the storage info for the blob
                storage_info = await device_client.get_storage_info_for_blob(blob_name)

                # Upload to blob
                success, result = await store_blob(storage_info, file_name)

                if success == True:
                    print("Upload succeeded. Result is: \n") 
                    print(result)
                    print()

                    await device_client.notify_blob_upload_status(
                        storage_info["correlationId"], True, 200, "OK: {}".format(file_name)
                    )

                else :
                    # If the upload was not successful, the result is the exception object
                    print("Upload failed. Exception is: \n") 
                    print(result)
                    print()

                    await device_client.notify_blob_upload_status(
                        storage_info["correlationId"], False, result.status_code, str(result)
                    )

            except Exception as ex:
                print("\nException:")
                print(ex)

            except KeyboardInterrupt:
                print ( "\nIoTHubDeviceClient sample stopped" )

            finally:
                # Finally, disconnect the client
                await device_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    #loop.close()
