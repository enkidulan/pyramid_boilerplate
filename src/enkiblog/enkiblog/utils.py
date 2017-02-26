from slugify import slugify as base_slugify


def get_max_length(field):
    try:
        return getattr(field.class_.__table__.c, field.key).type.length
    except AttributeError:
        pass


def slugify(text, field, dbsession):
    for i in range(99):
        unifier = str(i)
        slug = base_slugify(text, max_length=get_max_length(field) - len(unifier))
        slug += unifier if i else ''
        if dbsession.query(field.class_).filter(field == slug).one_or_none() is None:
            break
    else:
        raise RuntimeError('Wasn\'t able to generate slug')
    return slug
