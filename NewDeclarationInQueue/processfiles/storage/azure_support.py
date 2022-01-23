from typing import List, Tuple
from urllib.parse import urljoin, quote
from azure.storage.fileshare import ShareClient, ShareFileClient, ShareDirectoryClient
from PIL.PpmImagePlugin import PpmImageFile
from io import BytesIO, StringIO
import json
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages

from NewDeclarationInQueue.processfiles.storage.storage_support import StorageSupport

class AzureSupport(StorageSupport):
    """ Storage support for Azure, extends StorageSupport and overrides all functions
    """
    input_pdf_doc_with_key = ''
    input_pdf_doc = ''
    pages_urls = []
    
    
    def get_input_pdf_path_with_key(self) -> str:
        """ Get the input file URL with an SAS key

        Returns:
            str: input file URL
        """
        return self.input_pdf_doc_with_key.replace(' ', '%20')
    
    def get_input_pdf_path(self) -> str:
        """ Get the path of the input file

        Returns:
            str: the relative to the root path of the input file
        """
        return self.input_pdf_doc
    
    def get_pages_urls(self, cnt: OcrConstants) -> List[str]:
        """ Get urls of the images corresponding to each page of the input PDF file

        Returns:
            List[str]: List of URLs, one for each page, in order
        """
        return [urljoin(cnt.STORAGE_AZURE_BASE, v) + '?' + cnt.SAS_URL for v in self.pages_urls]
    
    def save_page(self, path: str, page: PpmImageFile, count: int, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Save page images

        Args:
            path (str): output path where images have to be saved
            page (PpmImageFile): image object
            count (int): page number to be used in the way the image file is named
            message (ProcessMessages): colects processing messages

        Returns:
            ProcessMessages: messages from the processing workflow
        """
        try:
            file_path = path + ('page' if path.endswith('/') else '/page') + str(count) + '.jpg'
            self.pages_urls.append(file_path)
            file_client = ShareFileClient.from_connection_string(conn_str=cnt.AZURE_CONNECTION_STRING, 
                                                        share_name=cnt.AZURE_SHARE_NAME, 
                                                        file_path= file_path.replace('%20', ' '))
            imagefile = BytesIO()
            page.save(imagefile, format='JPEG')   
            
            file_client.upload_file(imagefile.getvalue())
            
            message.add_message('Save page image', file_path, '')
        except Exception as exex:
            message.add_exception('save_page function call', exex)
            
        return message
    
    def save_ocr_json(self, path: str, filename: str, lines: dict, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Save JSON generated from OCR service call

        Args:
            path (str): output path
            filename (str): file name
            lines (dict): lines to put in the JSON document
            message (ProcessMessages): collects processing messages

        Returns:
            ProcessMessages: collects processing messages
        """
        try:
            file_path = path + ('' if path.endswith('/') else '/') + filename + '.json'
            file_client = ShareFileClient.from_connection_string(conn_str=cnt.AZURE_CONNECTION_STRING, 
                                                        share_name=cnt.AZURE_SHARE_NAME, 
                                                        file_path= file_path.replace('%20', ' '))
            jsonfile = StringIO()
            json.dump(lines, jsonfile)
            file_client.upload_file(jsonfile.getvalue())
            
            message.add_message('Ocr service called', 'Json file saved ' + file_path, '')
        except Exception as exex:
            message.add_exception('save_ocr_json function call', exex)
            
        return message
    
    def save_initial_file(self, input_path: str, output_path: str, filename: str, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Save the initial PDF file in the output path

        Args:
            input_path (str): input path
            output_path (str): output path
            filename (str): initial file name
            message (ProcessMessages): collects processing messages

        Returns:
            ProcessMessages: collects processing messages
        """
        try:
            input_file_client = ShareFileClient.from_connection_string(conn_str=cnt.AZURE_CONNECTION_STRING, 
                                                        share_name = cnt.AZURE_SHARE_NAME, 
                                                        file_path = input_path)
            #message.add_message('save initial file', input_path + '/' + filename, '')
            
            output_file_client = ShareFileClient.from_connection_string(conn_str=cnt.AZURE_CONNECTION_STRING, 
                                                        share_name = cnt.AZURE_SHARE_NAME, 
                                                        file_path = output_path + '/' + filename)
            
            pdf_file = BytesIO()
            
            #message.add_message('save initial file', output_path + '/' + filename, '')
            
            
            data = input_file_client.download_file()
            data.readinto(pdf_file)
            output_file_client.upload_file(pdf_file.getvalue())
            
            
        except Exception as exex:
            message.add_exception('save_initial_file function call', exex)
            
        return message
    
    def construct_input_document_path(self, path, filename, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Get path of the input document with security info and stores it internally

        Args:
            path (str): relative path
            file_name (str): file name
            message (ProcessMessages): collects processing messages from this function

        Returns:
            ProcessMessages: contains all processing messages
        """
        try:
            self.input_pdf_doc = urljoin(path, filename)
            
            self.input_pdf_doc_with_key = urljoin(cnt.STORAGE_AZURE_BASE, path)
            self.input_pdf_doc_with_key = self.input_pdf_doc_with_key.strip('/') + '/' + filename + '?' + cnt.SAS_URL
        except Exception as inst:
            message.add_exception('construct_input_document_path function call', inst)
            
            
        return message

    def get_secure_file(self, path, filename, cnt: OcrConstants) -> str:
        """ Get the file defined by path and filename with the security info attached

        Args:
            path (str): relative path of the file (relative to the root of the storage)
            filename (str): file name

        Returns:
            str: URL with security access
        """
        str_result = urljoin(cnt.STORAGE_AZURE_BASE, path)
        str_result = str_result.strip('/') + '/' + filename + '?' + cnt.SAS_URL
        return str_result
    
    def check_output_directory(self, path, cnt: OcrConstants, error: ProcessMessages) -> Tuple[ProcessMessages, str]:
        """ Check if the output directory exists in the storage. If the path is not valid,
                the methods returns the ProcessMessages with an error

        Args:
            path (str): relative path
            error (ProcessMessages): collects processing messages

        Returns:
            Tuple[ProcessMessages, str]: message storage and the validated output path
        """
        
        sv = path.split('/')
        
        share = ShareClient.from_connection_string(cnt.AZURE_CONNECTION_STRING, cnt.AZURE_SHARE_NAME)
        
        path = ''
        for one_path in sv:
            path = path + ('' if len(path) == 0 else '/') + one_path
            try:
                share.get_directory_client(directory_path=path)
            except:
                error.add_error('output directory not found', path)
            
            
        return error, path
    
    