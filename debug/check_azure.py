from azure.storage.fileshare import ShareServiceClient

from azure.storage.fileshare import ShareDirectoryClient

connection_string = "DefaultEndpointsProtocol=https;AccountName=aniocrstore;AccountKey=oY9xt3xcC4cN21c7nVA7xK9S2kiJuhr3Fb3MKlW5UYs/91CugX0lCQOt9d1w7hOIpEGP2rUbWcOYlv0/pzb/Rw==;EndpointSuffix=core.windows.net"
# service = ShareServiceClient.from_connection_string(conn_str=connection_string)

parent_dir = ShareDirectoryClient.from_connection_string(conn_str=connection_string, share_name="declaratii", directory_path="")

my_list = list(parent_dir.list_directories_and_files())
print(my_list)