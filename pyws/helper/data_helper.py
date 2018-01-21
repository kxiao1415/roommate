def clean_info(model, info):
    """
    recursively remove private columns of the model from the info

    :param model:
    :param info: dictionary
    :return:
    """
    if not isinstance(info, dict):
        raise Exception(u"'{0}' is not a invalid hash.".format(info))

    if '_relationships' in dir(model):
        for relationship in model.relationships():
            if relationship in info:
                if isinstance(info[relationship], list):
                    for i in info[relationship]:
                        clean_info(model.relationships()[relationship], i)
                else:
                    clean_info(model.relationships()[relationship], info[relationship])

    if '_private_columns' in dir(model):
        filter_columns(model.private_columns(), info)


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
