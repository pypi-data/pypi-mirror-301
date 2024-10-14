from typing import Protocol, BinaryIO

class DatalakeProtocol(Protocol):
    def download_object(self, bucket_name:str, obj_name:str, dest_file_path:str) -> None:
        ...
    def download_object_as_file(self, bucket_name:str,obj_name:str,f:BinaryIO ):
        ...