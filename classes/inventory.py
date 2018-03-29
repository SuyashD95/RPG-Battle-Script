class Item:
    """ This class manages all the fundamental details of the items used in the game. """

    def __init__(self, name, type, description, prop):
        """ Creates an instance of Item.

        :param str name: Name of the Item.
        :param str type: Item type.
        :param str description: Additional information regarding the Item.
        :param int prop: Effect of Item on HP/MP.
        """
        self._name = name
        self._type = type
        self._description = description
        self._prop = prop

    def get_name(self):
        """ Returns the name of the Item. """
        return self._name

    def get_type(self):
        """ Returns the type of the Item. """
        return self._type

    def get_description(self):
        """ Returns the description of the Item. """
        return self._description

    def get_prop(self):
        """ Returns the property of Item. """
        return self._prop
