# Sets for problem
set PROD;  # products
set STAGE; # stages

# parameters
param rate {PROD,STAGE} >  0; # lambda
param ovail {STAGE} >= 0;     # t
param profit {PROD};           # profit per ton
param commit {PROD} >= 0;     # lower limit
param market {PROD} >= 0;     # upper limit

var Make {p in PROD} >= commit[p], <=market[p];  # tons produced
maximize Total_Profit: sum {p in PROD} profit[p] * Make[p];
# Objective: total profits from all products
subject to Time {s in STAGE}:
sum {p in PROD} (1/rate[p,s]) * Make[p] <= avail[s];
# In each stage: total of hours used by all
# products may not exceed hours available