from app.core.cdataframe import CDataFrame


class CDataFrameCollection:
    def __init__(self):
        self.collection = []
    
    def add(self, item: CDataFrame):
        if not CDataFrame.is_type_obj(item):
            raise Exception("should be a CDataFrame object")
            return False
        self.collection.append(item)
        return True