def filter_private_columns(model_class, info):
    """
    Filter out private columns of given model class from info

    :param model_class: model class
    :param info: dictionary
    :return: filtered info
    """

    for key in model_class.private_columns():
        if key in info:
            del info[key]


def filter_deleted_model(model):
    """
    filter out deleted model

    :param model: model
    :return: model or None
    """
    if model is None or model.deleted:
        return None
    return model