from PID import pid
from matplotlib.pyplot import plot,show
from math import exp, sqrt
from numpy import abs
from selfbuild import selfbuild


def transfer_fun(x):
    return sqrt(abs(x))

setpoint = 0
u = 0
output = transfer_fun(u) 
result = []
PIDparameter = [1.0, 1.0, 1.0]

a = pid(0.0, 0.0, 0.00)
builder = selfbuild(PIDparameter, 20)
error = 0
for i in range(0,100):
    u = a.pid(error)
    output = transfer_fun(u)
    error = setpoint - output
    PIDparameter = builder.updateK(error, i)
    a.SetParameter(PIDparameter)
    result.append(output)
    
setpoint = 20

for i in range(100,200):
    u = a.pid(setpoint - output)
    output = transfer_fun(u)
    result.append(output)
    
plot(result)
show()
