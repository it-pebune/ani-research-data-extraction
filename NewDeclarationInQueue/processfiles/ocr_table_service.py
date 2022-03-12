from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from NewDeclarationInQueue.preprocess.ocr_constants import OcrConstants
from NewDeclarationInQueue.processfiles.customprocess.table_extractor import TableExtractor

from NewDeclarationInQueue.processfiles.formatter.ocr_table_formatter import OcrTableFormatter
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages
from NewDeclarationInQueue.processfiles.storage.storage_support import StorageSupport


class OcrTableService:
    """ Class to call the Azure Form Recognizer Cognitive Services and process the result 
            to save it on output directory
            and to generate a custom JSON and save it on output directory too
    """
    pdf_file: str
    form_recognizer_client: FormRecognizerClient = None
    formatter: OcrTableFormatter = OcrTableFormatter()
    
    def create_form_recognizer_client(self, cnt: OcrConstants):
        """ Create the Form Recognizer service client
        """
        self.form_recognizer_client = FormRecognizerClient(cnt.COMPUTER_VISION_FORM_ENDPOINT, 
                                        AzureKeyCredential(cnt.COMPUTER_VISION_FORM_SUBSCRIPTION_KEY))
        
    def get_form_recognizer(self, cnt: OcrConstants) -> FormRecognizerClient:
        """ Get the Form Recognizer service client

        Returns:
            FormRecognizerClient:  FormRecognizerClient current object, initialized in constructor
        """
        if not self.form_recognizer_client:
            self.create_form_recognizer_client(cnt)
        
        return self.form_recognizer_client
    
    def table_recognizer_service_call(self, storage: StorageSupport, output_path: str, initial_filename: str, 
                                      ocr_json_table_filename: str, ocr_json_custom_filename: str,
                                      declaration_type: int, formular_type: int, ocr_formular: dict, 
                                      cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        """ Call the form recognizer service, save the result and generate a custom JSON and save it.
                This is the entry point for the processing in this class.
                The service is called with the entire PDF file as input parameter, and the result will contain
                        lines and tables from all pages of the PDF input file.

        Args:
            storage (StorageSupport): storage intermediate object
            output_path (str): output path
            initial_filename (str): initial file name
            ocr_json_table_filename (str): output JSON file based on response received from Form Recognizer service
            ocr_json_custom_filename (str): result JSON output filename
            declaration_type (int): type of declaration: DAVERE or DINTERES
            formular_type (int): structure of the formular (this is a constant)
            message (ProcessMessages): processing messages

        Returns:
            ProcessMessages: [description]
        """
        
        # get the form recognizer service and if it not exist, return error
        client = self.get_form_recognizer(cnt)
        if client is None:
           message.add_error('Form recognizer creation', 'Form recognizer service could not be created') 
           return message
        
        # call the service and wait for results
        input_file_url = storage.get_secure_file(output_path, initial_filename, cnt)
        
        #check file exists
        message, output_path = storage.check_file_exists(output_path + initial_filename, cnt, message)
        if message.has_errors():
            return message
        
        try:
            poller = client.begin_recognize_content_from_url(input_file_url) #, language='ro')
            analyze_result = poller.result()
        except Exception as exex:
            message.add_exception('File OCR call failed: ' + input_file_url, exex)
            
        if message.has_errors():
            return message
        
       
        
        # if result is received, generate the JSON from the service
        if analyze_result:
            message, dict_ocr = self.formatter.get_json_from_form_recognizer_response(message, analyze_result)
    
        # save the obtained JSON from the service   
        message.add_message('form recognizer service call', 'service called for the initial pdf file', '')
        message = storage.save_ocr_json(output_path, ocr_json_table_filename, dict_ocr, cnt, message)
        
        message = self.generate_and_save_custom_json(storage, output_path, dict_ocr, 
                                                     ocr_formular, ocr_json_custom_filename,
                                                     declaration_type, formular_type, ocr_formular, cnt, message)
        
        # process the JSON obtained from the service and generate a custom JSON
        #extractor = TableExtractor()
        #message, custom_json = extractor.extract_from_doc_to_json(declaration_type, formular_type, dict_ocr, message)
        #message = storage.save_ocr_json(output_path, ocr_json_custom_filename, custom_json, cnt, message)
        
        return message
    
    def generate_and_save_custom_json(self, storage: StorageSupport, output_path: str, dict_ocr: dict,
                                config_tables: dict, ocr_json_custom_filename: str,
                                declaration_type: int, formular_type: int, ocr_formular: dict, 
                                cnt: OcrConstants, message: ProcessMessages) -> ProcessMessages:
        extractor = TableExtractor(ocr_formular)
        message, custom_json = extractor.extract_from_doc_to_json(declaration_type, formular_type, dict_ocr, message)
        message = storage.save_ocr_json(output_path, ocr_json_custom_filename, custom_json, cnt, message)
        
        return message