from ilc import ilc
import numpy as np

alpha = 0.97
beta = np.array([0.01, 0.01, 0.01])

handle = ilc(beta, alpha)

setpoint = 50
iteration = 1000
step = 255
setpoint = [10 for item in range(0,50)] + [setpoint for item in range(0,50)] \
                    + [10 for item in range(0,100) ] + [0 for item in range(0,55)]
# print(setpoint)
handle.ilc_run(step, setpoint, iteration)
handle.result_plot()
handle.last_plot()
handle.error_plot()
handle.PIDSimulation([1,1], step, setpoint)
# info_error, info_u = handle.getinfo(999)

# file = open('error.data','w')
# for item in info_error:
#     file.write(str(item))
#     file.write('\n')
# 
# file.close()
# file=open('u.data','w')
# for item in info_u:
#     file.write(str(item))
#     file.write('\n')
# file.close()

# handle.gen_PIDpar(step, iteration)
# handle.PIDSimulation(handle.gen_PIDpar(step, iteration), step, setpoint)