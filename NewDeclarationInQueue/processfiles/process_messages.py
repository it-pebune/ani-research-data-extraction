class OperationError:
    """ Represents an error in the processing operation
    """
    name = ''
    value = ''
    
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        
        
class OperationMessage:
    """ Represents a message generated in the processing operation
    """
    name = ''
    value = ''
    comment = ''
    
    def __init__(self, name: str, value: str, comm: str):
        self.name = name
        self.value = value
        self.comment = comm


class ProcessMessages:
    """ Represents the object that will collect all the messages, warnings and errors generated in the processing workflow.
            Will be sent and returned from all functions that participates in the processing workflow.
    """
    operation = ''
    input_message_id = ''
    errors = []
    messages = []
    
    def __init__(self, operation: str, input_id: str):
        self.operation = operation
        self.input_message_id = input_id
        self.errors = []
        self.messages = []
        
        
    def add_exception(self, name: str, inst: Exception):
        """ Adds message for an exception that was thrown in the processing workflow.
                will add an error internally.

        Args:
            name (str): name of the exception
            inst (Exception): the exception that was thrown
        """
        exception_error = ''
        for arg in inst.args:
            exception_error = exception_error + (' ' if len(exception_error) > 0 else '') + arg
                
        self.add_error(name, exception_error)
        
    def add_error(self, name: str, value: str):
        """ Adds an error from the processing worlfowl

        Args:
            name ([str]): name of the error
            value ([str]): description of the error
        """
        self.errors.append(OperationError(name, value))
        
    def add_message(self, name: str, value: str, comm: str):
        """ Adds a message from the processing worflow

        Args:
            name (str): name of the message
            value (str): description
            comm (str): an extra comment
        """
        self.messages.append(OperationMessage(name, value, comm))
        
    def has_errors(self):
        """ Checks if there are errors stored in this object until now
        """
        return (0 < len(self.errors))
    
    def get_error_json(self) -> dict:
        dict = []
        for err in self.errors:
            dict.append({
                'title': err.name,
                'value': err.value
            })
        return dict
    
    def get_message_json(self) -> dict:
        dict_msg = []
        
        for msg in self.messages:
            dict_msg.append({
                'title': msg.name,
                'value': msg.value,
                'comments': msg.comment
            } if len(msg.comment) > 0 else {
                'title': msg.name,
                'value': msg.value
            })
            
        return dict_msg
    
    def get_json(self):
        """ Gets a JSON form of the data in this class
        """
        str = {} #'process status': 'started'
        dict = []
        dict_msg = []
        
        for err in self.errors:
            dict.append({
                'title': err.name,
                'value': err.value
            })
            
            
        for msg in self.messages:
            dict_msg.append({
                'title': msg.name,
                'value': msg.value,
                'comments': msg.comment
            } if len(msg.comment) > 0 else {
                'title': msg.name,
                'value': msg.value
            })
            
        
        str["input_message_id"] = self.input_message_id
        str[self.operation] = {
            'errors': dict,
            'messages': dict_msg  
        }
        
        return str
    