import gurobipy as gp
from gurobipy import GRB
import pandas as pd

def uniPrint(to_print):
    try:
        display(to_print)
    except Exception as ex:
        print(to_print)
    return


# Used to generate lists of variables for the model
# buy value in 1k for month m such that bm = the amount to buy in month m
def generate_n_vars(model, count, vtype=GRB.CONTINUOUS, base_name="x", lb=None):
    """
        Generate list of count variables of given vtype each named base_name<Index>
        model:= gurobi generated model
        count:= the number of variables you want to generate
        vtype: the types of the variables generated which should be an GRB.vtype object
        base_name:= string used to name the variables of the form base_name<index>
        lb:= lower bound for variables
    """
    if lb is None:
        return [model.addVar(vtype=vtype, name=base_name + str(i + 1)) for i in range(count)]
    return [model.addVar(vtype=vtype, name=base_name + str(i + 1), lb=lb) for i in range(count)]


# used to generate the objective function by generating an expression that is the sum
# of the profits and costs for each month
def sum_vars(buyM, sellM, df, cost="C", profit="P"):
    """
        Generate an expression of the form:
            sum from m = 1 to M (sell(month)*proffit(month) - buy(month)*cost(month)) for all months to calculate
            the profit at the end of M months
        arguments:
        bs:= list of variables already added to the model representing the amount to buy in month s
        ss:= list of variables already added to the model representing the amount to sell in month s
        df:= dataframe containing cost and profit information where the row corresponding to
             index i contains data for month i+1 such that the indices are zero indexed
        cost:= column name for the passed data frame df that contains the cost of buying at month/index m
        profit:= column name for the passed data frame df that contains the profit of selling at month/index m
        returns: an expression of the form described above that can be passed to the model
    """
    cnt = 0
    expr = None
    for idx in df.index:
        if cnt == 0:
            expr = sellM[int(idx)] * df.loc[idx, profit] - buyM[int(idx)] * df.loc[idx, cost]
            cnt += 1
        else:
            expr += sellM[int(idx)] * df.loc[idx, profit] - buyM[int(idx)] * df.loc[idx, cost]
    return expr

    # used to generate the step based constraints described in the problem description


def add_sequential_constraints(model, bs, ss, xs, initial_stock, capacity):
    """
        creates constraints that mimic the process described as follows:
        1) check the amount on hand for month m held in variable xs[m] this
           represents the amount of stock in the warehouse at the beginning of month m.
           This is determined by the amount on hand during the previous month, the amount sold the previous month
           and the amount bought during the previous month:
                                           xs[m] = xs[m-1] - ss[m-1] + bs[m-1]
        2) during month m a you can only sell what was available in the ware house in month m:
                                                      ss[m] <= xs[m]
        3) At the end of the the month the total amount of stock in the warehouse meaning the amount bought
           plus the amount on hand, minus the amount sold for month m can not exceed the capacity for the ware house
                                       bs[m] + xs[m] - ss[m] <= capacity/limit_value
    """

    for i in range(len(bs)):
        # check the amount on hand in the warehouse for this month
        # given information that the initial month of analysis
        # contains initial amount of stock
        if i == 0:
            model.addConstr(xs[i] == initial_stock)
        else:
            model.addConstr(xs[i] == bs[i - 1] + xs[i - 1] - ss[i - 1])

        # add sell quantity constraint
        model.addConstr(ss[i] <= xs[i])

        # add capacity at end of month constraint
        model.addConstr(bs[i] + xs[i] - ss[i] <= capacity)
    return

# print out all decision variables
# if the variables have some sentinel value that signifies the last
# as defined with the end_sentinel an new line will  be printed to separate them
def displayDecisionVars(m, end_sentinel="10"):
    # display results/solution
    cnt = 0
    for v in m.getVars():
        try:
            print('{} {:.5f}'.format(v.VarName, v.X))
        except Exception as e:
            print(e, " There is some issue with your model/optimization")
            print('{},'.format(v.VarName))
        if end_sentinel in v.VarName:
            print()
        cnt += 1
    print("-------------------------------------\n\n")


# display the solution with the amount on hand, sold, and bought each month
# along with the current expected profit
def display_timestep_decisions(m, data_df, sell="Sell", buy="Buy", onhand="OnHand"):
    month_events = {}
    monthly_numbers = {}
    profits = 0
    for v in m.getVars():
        if "0" in v.Varname:
            mnth = int(v.VarName[-2:])
        else:
            mnth = int(v.VarName[-1])

        if mnth not in month_events:
            month_events[mnth] = {}
            monthly_numbers[mnth] = 0
        if sell in v.VarName:
            month_events[mnth][sell] = "Sell: " + str(v.X) + " at " + str(data_df.loc[mnth - 1, "P"])
            p = data_df.loc[mnth - 1, "P"]
            amnt = float(v.X)
            monthly_numbers[mnth] += amnt * p
        elif buy in v.VarName:
            month_events[mnth][buy] = "Buy: " + str(v.X) + " at " + str(data_df.loc[mnth - 1, "C"])
            p = data_df.loc[mnth - 1, "C"]
            amnt = float(v.X)
            monthly_numbers[mnth] += amnt * p * (-1)
        elif onhand in v.VarName:
            month_events[mnth][onhand] = "In Stock: " + str(v.X) + ","

    for month in month_events:
        profits += monthly_numbers[month]
        display_string = "Month: {}\n\t".format(month) + month_events[month][onhand] + " " + month_events[month][
            sell] + ", " + month_events[month][buy]
        print(display_string + ", Profits: {}".format(profits))