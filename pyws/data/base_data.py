from pyws import db
from pyws.helper import data_helper


class BaseData(object):

    def get(self, id):
        """
        Get a model by id

        :param id: primary key
        :return: model
        """

        return db.session.query(self.model_class).get(id)

    def create(self, info):
        """
        Create a new model with the given info

        :param info: dictionary
        :return: newly created model
        """

        data_helper.filter_private_columns(self.model_class, info)

        new_model = self.model_class(info)
        db.session.add(new_model)
        db.session.commit()

        return new_model

    def update(self, model, info):
        """
        Update the model with given info

        :param model: model to be updated
        :param info: dictionary
        :return: updated model
        """

        data_helper.filter_private_columns(self.model_class, info)

        for key in info.keys():
            if key in model.__table__.columns.keys():
                setattr(model, key, info[key])

        db.session.add(model)
        db.session.commit()

        return model

    def delete(self, model):
        """
        Remove the model row from database

        :param model: model to be deleted
        :return: True
        """

        db.session.delete(model)
        db.session.commit()
        return True
