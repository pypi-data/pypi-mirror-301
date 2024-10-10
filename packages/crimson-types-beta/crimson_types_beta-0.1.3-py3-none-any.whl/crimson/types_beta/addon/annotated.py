class AnnotatedType:
    """
    Make the metadata injection possible.
    You must inherit it before `type`.
    """

    def __class_getitem__(cls, params):
        pass
