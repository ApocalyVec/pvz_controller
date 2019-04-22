import math
import queue
import sys


def inference(var, value, csp):
    """
    inference using ac_3, it is very similar to ac_3 except it start only the arcs connecting to Xj
    there’s no point of running forward checking if we have already done arc consistency as a preprocessing step

    special case of ac_3
    :param Variable var:
    :param String value:
    :param runtimecsp csp:
    :return: Boolean; False if a var's domain results in empty
    """
    return True


def get_affected_value_num(var, value, csp):
    """
    only considers neighbors, otherwise very similar to inference_revise
    pruned values
    :param var:
    :param value:
    :param csp:
    :return:
    """
    prune_count = 0
    connections = csp.get_connecting_vars(var)

    for c in connections:
        biconst = csp.get_biconst(c, var)
        if biconst is not None:
            prune = False
            i = csp.get_index_of_value(value)

            for j in range(csp.get_values_len()):
                if value in c.domain:
                    prune = prune or biconst[i, j]
            if not prune:
                prune_count = prune_count + 1

    return prune_count


# TODO arcs should not have duplicate arcs
def ac_3(csp):
    """
    apply Arc Consistency to the given list of variables
    :param runtimecsp csp: constraint object against which to check arc consistency
    :return None, it modifies the domain of the given variable to be arc consistent
    """
    arcs = queue.Queue()

    # put arcs in the queue
    for a in csp.get_all_arcs():
        arcs.put(a)

    while not arcs.empty():
        arc = arcs.get()
        if revise(arc[0], arc[1], csp):  # revising the domain of arc[0]
            if not arc[0].domain:
                return False
            for propagating_arc in csp.get_arcs(arc[0]):
                arcs.put(propagating_arc)

    return True


def revise(X, Y, csp):
    """
        revise the domain of x, NOTE that it only checks the unary constraint for variables that are connected with arcs
        :param X Variable
        :param Y Variable
        :return bool true iff we revised the domain of x
    """
    revised = False
    const_mat = csp.get_biconst(X, Y)
    pruning_values = []

    for x in X.domain:
        if not is_constraint_satisfied(x, Y, const_mat, csp):
            pruning_values.append(x)
            revised = True

    for pv in pruning_values:
        X.domain.remove(pv)

    return revised  # return true if revised


def is_constraint_satisfied(x, Y, const_mat, csp):
    """

    :param x: the value in X.domain
    :param Y: the variable to check against
    :param csp:
    :return True is there are value in y that allows (x, y) to satisfy the constraint between X and Y_
    """
    rtn = False
    for y in Y.domain:
        i = csp.get_index_of_value(x)
        j = csp.get_index_of_value(y)
        rtn = rtn or const_mat[i, j]
    return rtn


def backtrack(assignment, csp, is_rtcost):
    """
    NOTE that the Constraint object keeps all the variables. Thus it also keeps all the assignment to variables
    :param assignment:
    :param csp:
    :return:
    """
    if is_assignment_complete(assignment): return assignment
    var = select_unassigned_var(assignment, csp)
    # print()
    # print("Considering: " + var.name + ", Trying: ")
    for value in ordered_domain_threat_level(var, assignment, csp):
        # print("[value " + value + "]")
        if check_value_consistency(var, value, assignment, csp):
            assignment[var] = value
            # print("Assignment is " + str([(key.name + "-" + str(value)) for key, value in assignment.items()]))
            if not check_budget(assignment, csp):
                print("Assignment violated budget constraint")
                assignment[var] = None
                continue
                return None

            if inference(var, value, csp):  # if inference left any variable's domain to be empty
                # print("Assignment after inference is " + str([(key.name + "-" + str(value)) for key, value in assignment.items()]))
                result = backtrack(assignment, csp, is_rtcost)  # recursion call
                if result is not None:
                    return result
            # print("Backtracking, removing " + var.name)
            assignment[var] = None  # remove this assignment

    return None


def ordered_domain_threat_level(var, assignment, csp):
    domain_copy = var.domain.copy()

    return domain_copy


def ordered_domain(var, csp):
    """
    order the domain of a variable by the rule of least constraining value
    :param var:
    :param assignment:
    :param csp:
    :return:
    """
    domain_copy = var.domain.copy()
    # for value in csp.get_values():
    #     print("Num: " + str(get_affected_value_num(var, value, csp)))
    # TODO have runtimecsp encapsulate this
    domain_copy.sort(key=lambda x: get_affected_value_num(var, x, csp), reverse=True)

    return domain_copy


def ordered_domain_runtime(var, assignment, csp, is_rtcost):
    """
    order the domain of a variable by the rule of least constraining value, breaking ties using RunTime
    :param var:
    :param assignment:
    :param csp:
    :return:
    """
    domain_copy = var.domain.copy()
    return domain_copy.sort()

    affected_value_dic = {}  # keep a dictionary of affected_value that's also used by RunTime tie breaking
    for value in domain_copy:
        affected_value_dic[value] = get_affected_value_num(var, value, csp)

    # for value in csp.get_values():
    #     print("Num: " + str(get_affected_value_num(var, value, csp)))
    # TODO have runtimecsp encapsulate this
    domain_copy.sort(key=lambda x: affected_value_dic[x], reverse=False)

    # breaking ties
    # group values that has the same 'affected_value_num'
    nums = set(map(lambda x: affected_value_dic[x], affected_value_dic))  # all the affect_nums that are present
    grouped_values = [[y[0] for y in affected_value_dic.keys() if affected_value_dic[y] == x] for x in nums]
    # sort each group by run time
    rtn = []

    for group in grouped_values:

        # for value in group:
        #     print("Runtime for " + value + " is " + str(csp.get_run_time(value, assignment)))
        # print()

        #  if rtcost is true, we multiple the runtime by its cost for a processor
        if is_rtcost:
            group.sort(key=lambda x: csp.get_run_time(x, assignment) * csp.get_rtcost_for_value(x),
                       reverse=False)  # x is a processor (value)
        else:
            group.sort(key=lambda x: csp.get_run_time(x, assignment), reverse=False)  # x is a processor (value)
        rtn = rtn + group

    return rtn


def naive_select_unassigned_var(assignment, csp):
    '''
    naive select_unassigned_var
    :param Constraint csp
    '''
    for var in csp.get_all_variables():
        if assignment[var] is None:
            return var


def select_unassigned_var(assignment, csp):
    '''
    clever select_unassigned_var
    implementing minimum remaining-values (MRV) / most constrained variable / fail-first
    :param csp Constraint
    :param assignment Dictionary
    '''
    # make a list to order all the variables
    var_list = []
    min_domain_len = math.inf
    for var in csp.get_all_variables():
        if assignment[var] is None:
            var_list.append(var)
            if len(var.domain) < min_domain_len:  # update the min domain length
                min_domain_len = len(var.domain)

    min_var_list = []  # the list that keeps the most constrained variables
    for var in var_list:
        if len(var.domain) == min_domain_len:
            min_var_list.append(var)

    if len(min_var_list) == 1:  # just return the variable if there's one most constrained variable
        return min_var_list[0]
    elif len(min_var_list) > 1:  # break tie using left-most columns first
        # min_var_list.sort(key=lambda x: (len(csp.get_connecting_unassigned_vars(x, assignment))), reverse=True)
        min_var_list.sort(key=lambda x: x.name)
        return min_var_list[0]
    else:
        print("Solver: select_unassigned_var: bad var list")
        sys.exit()


def is_assignment_complete(assignment):
    rtn = True
    for key, value in assignment.items():
        if value is None:
            rtn = rtn and False
        else:
            rtn = rtn and True
    return rtn


def initialize_assignment(assignment, csp):
    for var in csp.get_all_variables():
        assignment[var] = None


def check_value_consistency(var, value, assignment, csp):
    uex = csp.get_uex(var)
    uin = csp.get_uin(var)

    if uex:  # if the uex exists for this variable
        if value in uex:
            return False
    if uin:  # if the uex exists for this variable
        if value not in uin:
            return False

    connecting_var = csp.get_connecting_vars(var)

    # TODO the following part checks the binary constraints,
    # TODO it is very similar to what happended in revise function use in ac3
    if connecting_var is not None:  # if the variable has connections
        i = csp.get_index_of_value(value)  # get the index of the value being checked

        for c in connecting_var:
            const_matrix = csp.get_biconst(var, c)  # note that by doing this, var is the y axis, c is the x axis

            if assignment[c] is not None:
                if const_matrix[i, csp.get_index_of_value(assignment[c])] == 0:
                    return False
            # else:
            #     for j in range(csp.get_values_len()):
            #         if csp.get_value_by_index(j) in c.domain:
            #             if const_matrix[i, j] == 0:
            #                 return False

    # The following are domain-specific code for the task-processor problem
    # process_time = 0
    # for v in csp.get_all_variables():
    #     if assignment[v] is not None:
    #         if assignment[v] == value:
    #             process_time = process_time + v.tag
    # if process_time + var.tag >

    return True


def check_budget(assignment, csp):
    if not csp.is_budget_met(assignment):
        return False
    else:
        return True
