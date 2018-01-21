from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseData(object):

    def get(self, id):
        """
        Get a model by id

        :param id: primary key
        :return: model
        """

        return db.session.query(self.model_class).get(id)

    def create(self, model):
        """
        Create the new model

        :param model: new model to be created
        :return: newly created model
        """

        db.session.add(model)
        db.session.commit()

        return model.id

    def update(self, model, info):
        """
        Update the model with given info

        :param model: model to be updated
        :param info: dictionary
        :return: updated model
        """

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
