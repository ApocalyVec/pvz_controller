from os import system
from Graph import Graph
from runtime import Runtime

import numpy
import math


class RuntimeCsp:
    def __init__(self):

        self.uin = {} # [key: variable name (str), value: list of values]
        self.uex = {} # [key: variable name (str), value: list of values]
        self.biconst = {}
        # binary constraint matrices: [key: two constraining variables, value: the matrix
        # with the first variable on rows and the second on columns]
        self.const_graph = Graph()  # a constraint graph contains all the variables that are connected by binary constraints
        # the constraint graph is represented by a dictionary with [key: node, value: connections]
        # self.assignment = {}  # represent the assignment of variabels [Key: Variable, Value: value (str)]
        self.values = []
        self.value_costs = {}
        self.runtime = None
        self.budget = 0
        self.threat_level = 0
        self.attack_power = 0
        self.rtcost = {}

    def __str__(self):
        return "Unary Inclusive: " + str(self.uin) + "\n" + \
               "Unary Exclusive: " + str(self.uex) + "\n" + \
               "Binary Constraint: " + str(self.biconst.items()) + "\n"

        # "Binary Constraint: " + [(str(key) + ":\n" + str(value) + "\n") for key, value in self.biconst.items()]

    def set_rtcost_for_value(self, value, cost):
        """
        The function also checks if the value is in the value list of this csp. If not, it will terminate the run
        Note that this function does not validate if all value has been assigned a value, to do so, call validate_rtcost
        :param value:
        :param cost:
        """
        if value not in self.values:
            print("Invalid value in value cost: " + value + "; Killed")
            system.exit()

        self.rtcost[value] = cost

    def validate_rtcost(self):
        """
        :returns true if each value in self.values has a rtcost
        """
        for v in self.values:
            if v not in self.rtcost.keys():
                return False
        return True

    def get_rtcost_for_value(self, value):
        return self.rtcost[value]

    def set_values(self, values):
        '''
        :except Disused
        set values of all variable domain
        '''
        self.values = values
        for var in self.get_all_variables():
            for value in self.values:
                var.domain.append(value)

    def add_value_cost(self, val, cost):
        self.value_costs[val] = cost

    def set_budget(self, budget):
        self.budget = budget

    def get_budget(self):
        return self.budget

    def set_threat_level(self, level):
        self.threat_level = level

    def get_threat_level(self):
        return self.threat_level

    def set_attack_power(self, power):
        self.attack_power = power

    def get_attack_powere(self):
        return self.attack_power

    def make_runtime(self):
        """
        this method must be called after values are set
        """
        self.runtime = Runtime(self.values)

    def add_value(self, value):
        """
        add a value to all variables' domain, and to the values field of the CSP object
        """
        self.values.append(value)
        for var in self.get_all_variables():
            var.domain.append(value)

    def get_values(self):
        return self.values

    def get_value_by_index(self, i):
        return self.values[i]

    def get_index_of_value(self, value):
        return self.values.index(value)

    def get_values_len(self):
        return len(self.values)

    def get_all_variables(self):
        return self.const_graph.get_all_vertices()

    def add_var_to_graph(self, var):
        self.const_graph.add_vertex(var)

    def add_uin(self, const_var, const_value):
        self.uin[const_var] = const_value

    def get_uin(self, var):
        if var.name in self.uin.keys():
            return self.uin[var.name]

    def add_uex(self, const_var, const_value):
        self.uex[const_var] = const_value

    def get_uex(self, var):
        if var.name in self.uex.keys():
            return self.uex[var.name]


    # TODO handle duplicate binary varible EXCEPTION
    # TODO should say NO ANSWER if a constraint matrix are all zeros
    def add_biconst(self, const_vars, equal):  # constraint type
        """
        Create a binary constraint matrix

        :param list const_vars: the variables to be constrained
        :param int equal: constraint type: 1 = binary equals, 0 = binary not equals
        """
        # TODO what if two bi_const have the same constrainting variable
        # The first value in the tuple takes the rows, and the second takes the columns
        self.const_graph.add_edge(self.const_graph.get_vertex(const_vars[0]), self.const_graph.get_vertex(const_vars[1]))

        if tuple(const_vars) in self.biconst.keys():
            print("duplicate binary constraint, killed")
            system.exit()
        else:
            if equal:
                const_matrix = self.biconst[tuple(const_vars)] = numpy.zeros(
                    shape=(len(self.values), len(self.values)), dtype=int)
            else:
                const_matrix = self.biconst[tuple(const_vars)] = numpy.ones(
                    shape=(len(self.values), len(self.values)), dtype=int)

            for i in range(len(self.values)):  # modify the constraint matrix
                for j in range(len(self.values)):

                    if self.values[i] == self.values[j]:  # if the values are the same value, they should be constrained
                        const_matrix[i, j] = equal  # 0 for not equal, 1 for equal

        self.consolidate_matrix()



    def add_bins(self, const_vars, const_values):
        """
        Create a binary constraint matrix for NOT SIMULTANEOUS constraint

        :param list const_vars: the variables to be constrained
        :param list const_values: the values to be constrained
        :param dic const_values: list of values [key: index, value: variable value]
        """
        # TODO what if two bi_const have the same constrainting variable
        # The first value in the tuple takes the rows, and the second takes the columns
        self.const_graph.add_edge(self.const_graph.get_vertex(const_vars[0]),
                                  self.const_graph.get_vertex(const_vars[1]))

        if tuple(const_vars) in self.biconst.keys():
            print("duplicate binary constraint, killed")
            system.exit()
        else:
            const_matrix = self.biconst[tuple(const_vars)] = numpy.ones(
                shape=(len(self.values), len(self.values)), dtype=int)
            for i in range(len(self.values)):  # modify the constraint matrix
                for j in range(len(self.values)):
                    if (self.values[i], self.values[j]) == (const_values[0], const_values[1]):# or (self.values[i], self.values[j]) == (const_values[1], const_values[0]):
                        const_matrix[i, j] = 0

        self.consolidate_matrix()


    # TODO efficiency??? running this for loop everytime
    def consolidate_matrix(self):
        """
        add unary constraint to all binary constraint matrices

        """
        for const_vars, const_matrix in self.biconst.items():
            for i in range(len(self.values)):  # modify the constraint matrix
                for j in range(len(self.values)):
                    for const_var in const_vars:
                        if const_var in self.uex.keys():  # the rows(indexed by i) corresponds to the zeroth const variable; the columns(indexed by j) corresponds to the first const variable
                            if const_vars.index(const_var) == 0 and self.values[i] in self.uex[const_var]:
                                const_matrix[i, j] = 0
                            if const_vars.index(const_var) == 1 and self.values[j] in self.uex[const_var]:
                                const_matrix[i, j] = 0

                        if const_var in self.uin.keys():
                            if const_vars.index(const_var) == 0 and self.values[i] not in self.uin[const_var]:
                                const_matrix[i, j] = 0
                            if const_vars.index(const_var) == 1 and self.values[j] not in self.uin[const_var]:
                                const_matrix[i, j] = 0

    # '''
    # :return the constraint matrix between two variables
    # '''
    # def get_biconst(self, var1, var2):
    #     for key, value in self.biconst.items():
    #         # because we keep connection in both direction, we only need to check the constraint matrix in one direction
    #         # if (var1.name == key[0] and var2.name == key[1]) or (var1.name == key[1] and var2.name == key[0]):
    #         if var1.name == key[0] and var2.name == key[1]:
    #             return value


    def get_biconst(self, var1, var2):
        """
        :return the constraint matrix between two variables
        """
        for key, value in self.biconst.items():
            # because we keep connection in both direction, we only need to check the constraint matrix in one direction
            # if (var1.name == key[0] and var2.name == key[1]) or (var1.name == key[1] and var2.name == key[0]):
            if var1.name == key[0] and var2.name == key[1]:
                return value
            elif var1.name == key[1] and var2.name == key[0]:
                return value.transpose()  # we transpose the matrix to match the variables' axises

    def get_arcs(self, var):
        """
        :return a list of pair(list) of variables
        """
        return self.const_graph.get_edges(var)

    def get_connecting_vars(self, var):
        return self.const_graph.get_connecting_vertices(var)

    def get_connecting_unassigned_vars(self, var, assignment):
        """
        :param var:
        :param assignment:
        :return: a list of unassigned vars (with the given assignment) that are connected to :param var
        """
        connecting_vars = self.const_graph.get_connecting_vertices(var)
        rtn = []
        for var in connecting_vars:
            if assignment[var] is None:
                rtn.append(var)
        return rtn

    def get_all_arcs(self):
        return self.const_graph.get_all_edges()

    def print_all_variable(self):
        for var in self.const_graph.get_all_vertices():
            print(var.name + ", Domain: " + str(var.domain))

    def get_run_time(self, processor, assignment):
        """
        get the time the processor needs to run its assignments
        :param str/value processor:
        :param dictionary [key = Variable, value = str/value] assignment:
        :return: the time the processor needs to run its assignments
        """
        return self.runtime.generate_run_time(processor, assignment, self.get_all_variables())

    def is_budget_met(self, assignment):
        return self.runtime.get_spending(assignment, self.value_costs) <= self.budget

    def print_process_time(self, assignment):
        print("Process Time for Each Processor:")
        for processor in self.get_values():
            print("Processor " + processor + ": " + str(self.get_run_time(processor, assignment)))

    def print_total_run_time(self, assignment):
        ordered_processor = self.get_values()
        ordered_processor.sort(key=lambda x: self.get_run_time(x, assignment), reverse=True)
        print("The total run time is: " + str(self.get_run_time(ordered_processor[0], assignment)) + ", by processor " + ordered_processor[0])
