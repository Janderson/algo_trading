from abc import abstractmethod, ABC
from app.core.cdataframe import CDataFrame, CCalcDataFrame

class BaseIndicator(ABC):
    def __init__(self, user_params):
        self.__user_params = user_params
    
    @property
    def name(self):
        return self.name()

    def is_valid(self):
        if self.params is None:
            return False
        if len(self.params.keys())==0:
            return True
        params_is_valid=len(list(set(self.params.keys())-set(self.__user_params.keys())))==0
        for col in list(set(self.base_params())-set(self.params.keys())):
            self.params[col] = self.base_params()[col]            
        return all([params_is_valid])

    @property
    def params(self):
        return self.__user_params

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def base_params(self):
        return {}

    @abstractmethod
    def col_name(self):
        pass

    def __call__(self, cdataframe):
        if CDataFrame.is_type_obj(cdataframe):
            new_dataframe = self.calc(cdataframe.get())
            return CCalcDataFrame(new_dataframe, info=cdataframe.info)
        return None

    @abstractmethod
    def calc(self, dataframe):
        pass
    
    @staticmethod
    def is_type_obj(obj):
        return any([
            isinstance(obj, BaseIndicator),
            issubclass(obj.__class__, BaseIndicator)
        ])
