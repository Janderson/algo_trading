from app.indicators.base_indicator import BaseIndicator


class IndicatorsCollection:
    
    def __init__(self):
        self.__indicators = []

    def add(self, obj: BaseIndicator):
        if not BaseIndicator.is_type_obj(obj):
            raise Exception("should be a BaseIndicator object")
            return False
        if obj.is_valid():
            self.__indicators.append(obj)
            return True
        return False
    
    def append(self, obj: BaseIndicator):
        return self.add(obj)
    
    def get(self, index):
        return self.__indicators[index]
    
    def __getitem__(self, index):
        return self.get(index)