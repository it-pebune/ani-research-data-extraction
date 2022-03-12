from typing import List, Tuple
from PIL.PpmImagePlugin import PpmImageFile
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class StorageSupport:
    def get_input_pdf_path(self) -> str:
        """ Get the path of the input file

        Returns:
            str: the relative to the root path of the input file
        """
        pass
    
    def get_input_pdf_path_with_key(self) -> str:
        """ Get the input file URL with an access key

        Returns:
            str: input file URL
        """
        pass
    
    def get_pages_urls(self, cnt: OcrConstants) -> List[str]:
        """ Get urls of the images corresponding to each page of the input PDF file

        Returns:
            List[str]: List of URLs, one for each page, in order
        """
        pass
    
    def get_secure_file(self, path: str, filename: str, cnt: OcrConstants) -> str:
        """ Get the file defined by path and filename with the security info attached

        Args:
            path (str): relative path of the file (relative to the root of the storage)
            filename (str): file name

        Returns:
            str: URL with security access
        """
        pass
    
    def construct_input_document_path(self, path: str, file_name: str, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Get path of the input document with security info and stores it internally

        Args:
            path (str): relative path
            file_name (str): file name
            message (ProcessMessages): collects processing messages from this function

        Returns:
            ProcessMessages: contains all processing messages
        """
        pass

    def check_output_directory(self, path: str, cnt: OcrConstants, error: ProcessMessages) -> Tuple[ProcessMessages, str]:
        """ Check if the output directory exists in the storage. If the path is not valid,
                the methods returns the ProcessMessages with an error

        Args:
            path (str): relative path
            error (ProcessMessages): collects processing messages

        Returns:
            Tuple[ProcessMessages, str]: message storage and the validated output path
        """
        pass
    
    
    def check_file_exists(self, path: str, cnt: OcrConstants, error: ProcessMessages) -> Tuple[ProcessMessages, str]:
        """ Check if the file exists in the storage. If the path is not valid,
                the methods returns the ProcessMessages with an error

        Args:
            path (str): relative path
            error (ProcessMessages): collects processing messages

        Returns:
            Tuple[ProcessMessages, str]: message storage and the validated output path
        """
        pass
    
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
        pass
    
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
        pass
    
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
        pass