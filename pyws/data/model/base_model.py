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
            if isinstance(self.__dict__[key], datetime):
                jsonified_obj[key] = self.__dict__[key].isoformat()
            else:
                jsonified_obj[key] = self.__dict__[key]

        if filter_hidden_columns:
            hidden_columns = self.hidden_columns()
            for hidden_column in hidden_columns:
                del jsonified_obj[hidden_column]

        return jsonified_obj
