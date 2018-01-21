from datetime import datetime


class BaseModel(object):

    def to_json(self, filter_hidden_columns=False):
        """
        Transform the model into a json object

        :return: jsonified model
        """

        self.id # important: need to access id first to populate

        jsonified_obj = {}
        for key in self.__table__.columns.keys():
            if isinstance(getattr(self, key), datetime):
                jsonified_obj[key] = getattr(self, key).isoformat()
            else:
                jsonified_obj[key] = getattr(self, key)

        if '_relationships' in dir(self):
            for key in self.relationships().keys():
                if getattr(self, key):
                    if isinstance(getattr(self, key), list):
                        jsonified_obj[key] = []
                        for model in getattr(self, key):
                            jsonified_obj[key].append(self.to_json(model, filter_hidden_columns))
                    else:
                        jsonified_obj[key] = getattr(self, key).to_json(filter_hidden_columns)

        if '_hidden_columns' in dir(self):
            if filter_hidden_columns:
                hidden_columns = self.hidden_columns()
                for hidden_column in hidden_columns:
                    del jsonified_obj[hidden_column]

        return jsonified_obj
