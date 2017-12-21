from datetime import datetime


class BaseModel(object):

    def to_json(self):
        """
        Transform the model into a json object

        :return: jsonified model
        """

        self.id # important: need to access id first to populate

        jsonified_obj = {}
        for key in self.__dict__.keys():
            if key.startswith('_'):
                pass
            elif isinstance(self.__dict__[key], datetime):
                jsonified_obj[key] = self.__dict__[key].isoformat()
            else:
                jsonified_obj[key] = self.__dict__[key]

        return jsonified_obj
