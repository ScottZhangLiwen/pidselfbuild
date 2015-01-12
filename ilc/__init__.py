import numpy as np
from matplotlib.pyplot import plot,show
from numpy import sum

class ilc:
    def __init__(self, beta, alpha):
        self.beta = np.array(beta)
        self.alpha = alpha
        
        self.error_sum = 0
        self.last_error = 0
        self.u_last =[]
        self.u = []
        self.error_list = []
        self.step = 0        
        self.result = []
        
        self.sum_list = []
        self.ilc_error_list = []
        self.ilc_sum_list = []
        
        self.sum_p = []
        self.sum_i = []
        self.sum_d =[]
        
    def clear(self):
        self.error_sum = 0
        self.last_error = 0
        self.u_last =[]
        self.u = []
        self.error_list = []
        self.step = 0
        self.result = []

    def _calculate_w(self, error):
#         print(error)
#         print(self.error_sum)
        self.error_sum += error
        derror = error-self.last_error
        return np.array([error, self.error_sum, derror])
    
    def calculate_u(self, error, step):
        return self.alpha*self.u_last[step] + np.sum(self.beta*self._calculate_w(error))
    
    def system(self, u):
        return u*np.sinc(1/(u+1))
    
    def ilc_run(self, step, setpoint, iteration):
        
        self.last_error = 0
        self.u_last = np.zeros(step)
        
        for iteration_count in range(0, iteration):
#             print("iteration_count", iteration_count)
            u = 0
            result = []
            self.error_list = []
            self.error_sum =0
            temp_sum = []
            
            for item in range(0, step):
#                 print('step',item)
                output = self.system(u)
                error = setpoint[item] - output
#                 print(error)
                w_new = self._calculate_w(error)
                
                self.last_error = error
                self.error_list.append(error)
                u = self.calculate_u(error, item)
                self.u_last[item] = u
                
                temp_sum.append(self.error_sum)
                result.append(output)
                
            self.sum_list.append(self.error_sum*self.error_sum)
            self.ilc_error_list.append(self.error_list)
            self.ilc_sum_list.append(temp_sum)
            
            self.result.append(result)
        
    def result_plot(self):
        for item in self.result:
            plot(item)
        show()

    def last_plot(self):
        plot(self.result[-1])
        show()
            
    def error_plot(self):
        plot(self.sum_list)
        show()
                
    def gen_PIDpar(self, step, iteration):
        '''Kp'''
        kp = []
        ki = []
        temp_ki = 0
        kd = []
        temp_kp = 0
        for item in range(0, step):
            for iterative_count in range(0, iteration):
                temp_kp += self.ilc_error_list[iterative_count][item]
                temp_ki += self.ilc_sum_list[iterative_count][item]
            if self.ilc_error_list[-1][item] == 0:
                kp.append(0)
            else:
                kp.append(self.beta[0] * temp_kp / self.ilc_error_list[-1][item])
                
            ki.append(self.beta[1] * temp_ki / self.ilc_sum_list[-1][item])
                
                
        plot(np.array(ki))
        show()
        plot(np.array(kp))
        show()
        
        return [np.array(kp), np.array(ki)]
    
    def PIDSimulation(self, k, step, setpoint):
        pid_error_sum = 0
        pid_error = 0
        kp = 0.3333
        ki = 0.6667
        
        u = 0
        result = []
        for i in range(0, step):
            output = self.system(u)
            
            pid_error = setpoint[i] - output
            pid_error_sum += pid_error
            
            if pid_error_sum>400: pid_error_sum=400
            if pid_error_sum<-400: pid_error_sum=-400
            
            
            u = kp*pid_error + ki*pid_error_sum
            result.append(output)
            
        print(output)
        plot(result)
        show()
    
    def getinfo(self, iteration):
        return self.ilc_error_list[iteration], self.u_last
        