class Variable:

    def __init__(self):
        self.name = None
        self.value = None
        self.domain = []

    def __init__(self, name):
        """
        Create a Variable

        :param string name: name of the variable
        :param int equal: constraint type: 1 = binary equals, 0 = binary not equals

        var value: value to which this variable will be assigned
        """
        self.name = name
        self.value = None
        self.domain = []

    def __init__(self, name):
        """
        Create a Variable

        :param string name: name of the variable

        var value: value to which this variable will be assigned
        """
        self.name = name
        self.value = None
        self.domain = []

    def __str__(self):
        return str(self.name) + ": " + str(self.value) + str(self.domain)

    def set_value(self, value):
        self.value = value

    def set_domain(self, domain):
        """
        set the domain the variable
        :param dictionary domain: values [key: index, value: variable value]
        """
        self.domain = domain
