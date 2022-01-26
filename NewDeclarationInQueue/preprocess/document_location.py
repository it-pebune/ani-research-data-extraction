from NewDeclarationInQueue.preprocess.models import DocumentType


class DocumentLocation:
    """Class for all the parameters necessary for processing a file
    """
    type = DocumentType.DOC_WEALTH
    storage = 'azure'
    path = ''
    filename = ''
    out_path = ''
    page_image_filename = ''
    ocr_json_filename = ''
    ocr_table_json_filename = ''
    ocr_custom_json_filename = ''
    formular_type = ''
    
    def __init__(self, type, storage, path, filename, outpath, pageimage, jsonfilename, tablefilename, customfilename, formulartype):
        """Constructor containg all the parameters for processing a file

        Args:
            type ([type]): Type of declaration (welth of interest)
            storage ([type]): Type of storage: azure or something else
            path ([type]): Relative path to the file to process
            filename ([type]): Name of the file to be processed
            outpath ([type]): Relative path where the output files should be saved
            pageimage ([type]): Relative path where the page images should be saved
            jsonfilename ([type]): Relative path where the JSON file obtained from OCR service should be saved
            tablefilename ([type]): Relative path where the JSON file obtained from 
                                        processing the file obtained from OCR services should be saved
            customfilename ([str]): Relative path where the custom JSON file will be saved 
                                        (obtained after processing the data from OCR service)
            formulartype ([str]): Type of the formular (structure)
        """
        self.type = type
        self.storage = storage
        self.path = path
        self.filename = filename
        self.out_path = outpath
        self.page_image_filename = pageimage
        self.ocr_json_filename = jsonfilename
        self.ocr_table_json_filename = tablefilename
        self.ocr_custom_json_filename = customfilename
        self.formular_type = formulartype
    
    def __str__(self):
       return self.storage
    



 
    