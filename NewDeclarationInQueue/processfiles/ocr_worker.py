from typing import Tuple

from NewDeclarationInQueue.preprocess.document_location import DocumentLocation
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.image_generation_service import ImageGenerationService
from NewDeclarationInQueue.processfiles.ocr_service import OcrService
from NewDeclarationInQueue.processfiles.ocr_table_service import OcrTableService
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.storage.azure_support import AzureSupport
from NewDeclarationInQueue.processfiles.storage.storage_support import StorageSupport


class OcrWorker:
    """ Main class for document processing, contains the parameters for processing
            storage access object (depending on the type of storage in the parameters)
            service for document processing.
        This class will check the validity of storage, will take the documents from
        storage and will send them to the processing service.
    """
    doc_location: DocumentLocation
    storage: StorageSupport
    service: OcrService
    
    def __init__(self, doc: DocumentLocation):
        """ Initializer receiving the valid processing parameter

        Args:
            doc ([DocumentLocation]): Validated processing parameters for the processing.
        """
        self.doc_location = doc
        
        
    def check_paths(self, cnt: OcrConstants, messages: ProcessMessages) -> Tuple[ProcessMessages, str, str]:
        """ Create the storage management object and 
                check the storage path for input and output paths and files
            The storage object is of type StorageSupport but this is an interface,
                the type of the storage object will be determined by the parameter 
                doc_location_storage and if this is of type AZURE, an object of type
                AzureSupport (implementing StorageSupport) will be created.

        Args:
            messages (ProcessMessages): Messages and warnings in the processing workflow
                until now

        Returns:
            Tuple[ProcessMessages, str, str]: ProcessMessage is the received object with messages
                and warnings added from this function.
                first string is the output path
                second string is the initial filename
        """
        
        #add message that this function has started processing
        messages.add_message('Processing', 'process started', '')
        
        #if the type of the storage is azure, create an object of type
        #AzureSupport, if it is not of type azure, and an error in the 
        #ProcessMessasge object
        if self.doc_location.storage == cnt.STORAGE_TYPE_AZURE:
            self.storage = AzureSupport()
            messages.add_message('Storage identified', 'Azure storage', '')
        else:
            messages.add_error('Wrong storage type: ', self.doc_location.storage)      
            
        #if there are errors until now, return
        if messages.has_errors():
            return messages, None, None   

        #construct the input document path, check the output path and if there are errors, return. 
        #If there are not errors, add a message in the ProcessMessage object
        messages = self.storage.construct_input_document_path(self.doc_location.path, self.doc_location.filename, cnt, messages)

        messages, output_path = self.storage.check_output_directory(self.doc_location.out_path, cnt, messages)
        if messages.has_errors():
            return messages
        else:
            messages.add_message('Check output directory', output_path, '')
            
        initial_filename = self.doc_location.filename
            
        #return the messages object, the output path and the initial filename
        return messages, output_path.replace(' ', '%20'), initial_filename.replace(' ', '%20')
    
    
    def process(self, cnt: OcrConstants, ocr_formular: dict, result: ProcessMessages) -> ProcessMessages:
        """ Process the document, this method is called from the API and it is
                the entry point of this class.
            The function will:
                1) create a ProcessMessages object to keep the messages and warnings
                2) create a StorageSupport (AzureSupport) object depending of the storage type 
                        (only azure is supported at the moment)
                3) check the input and output paths
                4) create the ImageGenerationService, generate the page images 
                    and copy the original file in the output path
                5) create the OcrTableService and call the service for the input document,
                    generating the two JSON files
                6) check if there are errors and return the processing messages

        Returns:
            ProcessMessages: messages and warnings from the processing workflow
        """
        
        #create the ProcessMessage object and check the paths
        #if there are errors, return
        result, output_path, initial_filename = self.check_paths(cnt, result)
        if result.has_errors():
            return result
        
        # create the image generation service object and
        # generate the page images and copy the initial file to the output folder
        # section used only if we want to generate images for each page
        #image_generation_service = ImageGenerationService()
        #result, pages = image_generation_service.\
        #    generate_pages_and_save_images_and_original_file(output_path, initial_filename, self.storage, cnt, result)        
        #if result.has_errors():
        #    return result
        #else:
        #    result.add_message('ocr worker process', 'Images generated for pages and initial file copied', '')
        # end section used to generate images for each page
        
        #not used section, used to call the OCR only service from Azure, 
        # this call is replace with the call to Forms Recognizer service
        
        #  ocr_service = OcrService(pages)
        #result = ocr_service.ocr_service_call(self.storage, output_path, self.doc_location.ocr_json_filename, result)
        #if result.has_errors():
        #    return result
        #else:
        #    result.add_message('ocr worker process', 'Ocr service called and ocr json file saved: ' + self.doc_location.ocr_json_filename)
        
        # create the OcrTableService, used to call the Forms Recognizer service
        table_service = OcrTableService()
        # call the service and generate the two output JSON files
        result = table_service.\
            table_recognizer_service_call(self.storage, output_path, initial_filename, 
                                          self.doc_location.ocr_table_json_filename, 
                                          self.doc_location.ocr_custom_json_filename,
                                          self.doc_location.type,
                                          self.doc_location.formular_type,
                                          ocr_formular,
                                          cnt, result)
            
        #check if there are errors and if not add the status message for successfully processed
        if result.has_errors():
            return result
        else:
            result.add_message('ocr worker process', 'Ocr form recognizer service called and ocr json file saved -> '
                               + self.doc_location.ocr_table_json_filename, ' - ' + self.doc_location.ocr_custom_json_filename)
        
        return result
    
    
    def process_custom_file(self, cnt: OcrConstants, config_tables: dict, \
                                ocr_dict: dict, result: ProcessMessages) -> dict:
        result, output_path, initial_filename = self.check_paths(cnt, result)
        if result.has_errors():
            return result
    
        
        # create the OcrTableService, used to call the Forms Recognizer service
        table_service = OcrTableService()
        result = table_service.\
            generate_and_save_custom_json(self.storage, output_path,  ocr_dict, config_tables,
                                          self.doc_location.ocr_custom_json_filename,
                                          self.doc_location.type,
                                          self.doc_location.formular_type,
                                          config_tables, cnt, result)
         
        return result