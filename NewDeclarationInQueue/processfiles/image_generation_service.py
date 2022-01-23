from typing import Tuple

from pdf2image import convert_from_path
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants

from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.storage.storage_support import StorageSupport




class ImageGenerationService:
    """ Class used for the process of generating images for each page of the input PDF file
            and for copying the original file to the output folder
    """
    pages: list
    
    def generate_pages_and_save_images_and_original_file(self, path: str, filename: str, storage: StorageSupport, \
            cnt: OcrConstants, messages: ProcessMessages) -> Tuple[ProcessMessages, list]:
        """ Entry method for this class, this is called from the processing worker. 
                It will generate images for each page of the input PDF file and 
                will copy the input file in the output folder.

        Args:
            path (str): relative input path
            filename (str): input file name
            storage (StorageSupport): StorageSupport object to intermediate storage information
            messages (ProcessMessages): ProcessMessage object to collect messages and warnings 
                                            in this process step

        Returns:
            Tuple[ProcessMessages, list]: returns the ProcessMessages object containing the messages
                                            from this section and a list of pages
        """
        
        # get images for each page and store them in the self.pages 
        messages = self.generate_pages_from_input_file(storage, messages)
        if messages.has_errors():
            return messages
        
        # save the page images in the output folder
        messages = self.save_all_pages(path, storage, cnt, messages)
        if messages.has_errors():
            return messages
        else:
            messages.add_message('Image generation for all pages', 'Done', '')
            
        #save the initial file in the output folder
        messages = self.save_initial_file(path, filename, storage, cnt, messages)
            
        return messages, self.pages
    
    def generate_pages_from_input_file(self, storage: StorageSupport, message: ProcessMessages) -> ProcessMessages:
        """ Generates the page images for each page of the input PDF file

        Args:
            storage (StorageSupport): intermediates the operations with the storage
            message (ProcessMessages): collects processing messages

        Returns:
            ProcessMessages: messages collected in the process and modifies the self.pages property of this class
        """
        try:
            # generate images using pdf2image library and accesses the input file
            # using the storage object
            self.pages = convert_from_path(storage.get_input_pdf_path_with_key(), 500)    
            message.add_message('Generate pages from input pages', 'image for each page is generated', '')
        except Exception as exex:
            message.add_exception('generate_pages_from_input_files function call', exex)
            
        return message
    
    def save_all_pages(self, path: str, storage: StorageSupport, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Save all pages from the internal property self.pages to the output path, 
                using a convention based on the page number for naming each file

        Args:
            path (str): output path
            storage (StorageSupport): supports operations with the storage
            message (ProcessMessages): collects processing messages

        Returns:
            ProcessMessages: messages collected in the processing workflow
        """
        count = 1
        for page in self.pages:
            storage.save_page(path, page, count, cnt, message)
            count += 1
            
        return message
    
    def save_initial_file(self, output_path: str, filename: str, storage: StorageSupport, cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Save the inital file in the output path

        Args:
            output_path (str): output path
            filename (str): intial filename
            storage (StorageSupport): intermediates operations with the storage
            message (ProcessMessages): collects processing messages

        Returns:
            ProcessMessages: [description]
        """
        message = storage.save_initial_file(storage.get_input_pdf_path(), output_path, filename, cnt, message)
        return message