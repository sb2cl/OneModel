class Scope:
    """The Scope defines which namespaces can be accesed and referenced.

    Not all namespaces are visibible at the same time, the Scope defines which
    namespaces can be accesed and referenced. The Scope behaves as a stack that
    stores namespaces in a Last-In/First-Out (LIFO) manner.

    Parameters
    ----------
    namespaces : :obj:`list` of :obj:`Namespace`
        List of accesible namespaces.

    identifiers : :obj:`list` of :obj:`str`
        List of the identifier name for each namespace.
    """

    def __init__(self):
        self.namespaces = []
        self.identifiers = []

    def push(self, namespace, indentifier=""):
        """Inserts a namespace in the Scope."""

        self.namespaces.append(namespace)
        self.identifiers.append(indentifier)

    def pop(self):
        """Removes the last inserted namespace in the Scope."""

        if self.namespaces:
            self.namespaces.pop()
            self.identifiers.pop()
        else:
            raise Exception("Scope is empty")

    def peek(self):
        """Returns the last inserted namespace in the Scope. """

        if self.namespaces:
            return self.namespaces[-1]
        else:
            return None

    def set(self, name, value):
        """ Defines a value in the last inserted namespace. """ 
        self.peek()[name] = value

    def get(self, name):
        """ Gets a value by its name. 

        First, we look for the name in the last inserted namespace: 

        * If the name is defined there, the value is returned. 
        * If the name is not defined there, we look for it recursibely in the
          previous namespaces.
        * If the name is nof found in any of the namespaces, return None.

        """

        for namespace in reversed(self.namespaces):
            if name in namespace:
                return namespace[name]
        return None

    def get_fullname(self, name):
        """ Returns the unique name (fullname) to referer to that name.

        The names of a nampespace are unique inside that namespace, but the
        same name can be used in different namespaces. During modeling
        flattening, we need unique names for the objects that define the model.
        This unique names are generated by taking into account the name of the
        namespace where the object resides.
        """

        i = len(self.namespaces)
        for namespace in reversed(self.namespaces):
            if name in namespace:
                break
            i -= 1
        position_namespace_has_name = i

        basename = ""
        i = 0
        while i < position_namespace_has_name:
            if self.identifiers[i] != "":
                basename += self.identifiers[i] + "__"
            i += 1
        
        result = basename + name

        return result

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)
