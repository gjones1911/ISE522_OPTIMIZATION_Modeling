
# declare decision variables
# xi = fraction for investment i s.t. i in {1,2,3,4,5}
var x1 >= 0; 
var x2 >= 0; 
var x3 >= 0; 
var x4 >= 0; 
var x5 >= 0; 


# set up the objective
maximize NPV: (x1)*(13) + (x2)*(16) + (x3)*(16) + (x4)*(14) + (x5)*(39);

# set up constraints based on the budget for the different years
subject to budget0: (x1)*(11) + (x2)*(53) + (x3)*(5) + (x4)*(5) + (x5)*(29) <= 40;
subject to budget1: (x1)*(3)  + (x2)*(6)  + (x3)*(5) + (x4)*(1) + (x5)*(34) <= 20;

# set up constraints to make sure that the fractional values for the different projects are confined to some 
# value between 0 and 1
subject to c1: x1 <=1;
subject to c2: x2 <=1;
subject to c3: x3 <=1;
subject to c4: x4 <=1;
subject to c5: x5 <=1;


