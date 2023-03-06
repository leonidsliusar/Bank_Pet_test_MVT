from abc import ABC, abstractmethod
class QuerySetSerializer(ABC):
    @abstractmethod
    def create_serializer(self, data):
        pass

class JSON(QuerySetSerializer):
    def create_serializer(self, data):
        query_list = []
        for q in data:
            q['balance'] = str(q['balance'])
            query_list.append(q)
        dict = {'wallet_data': query_list}
        return dict

class DataFactory(ABC):
    @abstractmethod
    def _get_format(self):
        pass

class JSONFactory(DataFactory):
    def _get_format(self, data):
        serializer = JSON()
        return serializer.create_serializer(data)

def query_serializer(data):
    if data == None:
        return None
    elif str(type(data)) == "<class 'django.db.models.query.QuerySet'>":
        factory = JSONFactory()
        return factory._get_format(data)

