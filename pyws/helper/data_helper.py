def filter_columns(columns, info):
    """
    Filter out columns from info

    :param columns: model class
    :param info: dictionary
    :return: filtered info
    """

    for key in columns:
        if key in info:
            del info[key]
    return info


def filter_deleted_model(model):
    """
    filter out deleted model

    :param model: model
    :return: model or None
    """

    if model is None or model.deleted:
        return None
    return model
