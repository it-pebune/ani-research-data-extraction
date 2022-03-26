

from typing import Tuple
from NewDeclarationInQueue.preprocess.models import DocumentType
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.cm_formular_base import CmFormularBase
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.cm_interest_formular import CmInterestFormular
from NewDeclarationInQueue.processfiles.cmodelprocess.formulars.cm_wealth_formular import CmWealthFormular
from NewDeclarationInQueue.processfiles.process_messages import ProcessMessages


class ModelDefinition:
    FORMULAR_DA_1 = "declaratii-de-integritate-cmodel:declaratii-de-avere-F01" 
    FORMULAR_DA_2 = "declaratii-de-integritate-cmodel:declaratii-de-avere-F02" 
    FORMULAR_DI_1 = "declaratii-de-integritate-cmodel:declaratii-de-interese-F01"
    FORMULAR_DI_2 = "declaratii-de-integritate-cmodel:declaratii-de-interese-F02"
    
    
    def get_formular_from_model(self, identified_forms: dict, messages: ProcessMessages) -> Tuple[CmFormularBase, int, ProcessMessages]:
        confidence = 0
        main_key = None
        for key in identified_forms.keys():
            form = identified_forms[key]
            if confidence < form[CmFormularBase.FORM_CONFIDENCE]:
                main_key = key
                
                
        if main_key is None:
            messages.add_error('Formular not found in the custom model results')
            return None, 0, messages
        
        #declaratii-de-integritate-cmodel:declaratii-de-avere-F01
        form = identified_forms[main_key]
        form_type = form[CmFormularBase.FORM_TYPE]
        
        formular, document_type = self.get_formular_by_type(form_type)
        if formular is None:
            messages.add_error('Formular type not found: ' + form_type)
            return None, 0, messages
        
        formular.load_from_model(form)
        return formular, document_type, messages
        
        
    def get_formular_by_type(self, form_type: str) -> Tuple[CmFormularBase, int]:
        
        if form_type == ModelDefinition.FORMULAR_DA_1:
            return CmWealthFormular(), DocumentType.DOC_WEALTH
        
        if form_type == ModelDefinition.FORMULAR_DI_1:
            return CmInterestFormular(), DocumentType.DOC_INTERESTS
        
        return None