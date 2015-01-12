from numpy import abs

class pid:
    
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_sum = 0.0
        self.last_error = 0.0
        self.error_sum_max = 500
        self.error_sum_min = -500
        
     
    pass

    def Selfbuild_init(self, k_init, n):
        '''
        PID自建立
        '''        
        self.step = 0
        self.ISEresult = []
        self.parameters = [k_init]
        
        self.k_initial = k_init
        self.factor = 1.0/n
        self.n = n
        
        self.lamdap = 0;
        self.lamdai = 1;
        self.lamdad = 0;
        
    def ISE(self):
        sum = 0
        if self.step<self.n:
            for item in self.error:
                sum +=item*item
        else:
            for item in self.error[self.step-self.n:self.step]:
                sum += item*item
        return sum*self.factor
        
    def gamma(self):
        if self.step ==0:
            fenzi = [0.0, 0.0, 0.0]
            fenmu = 1.0;
        else:
            fenzi =[self.parameters[self.step][0]-self.parameters[self.step-1][0],
                     self.parameters[self.step][1]-self.parameters[self.step-1][1],
                     self.parameters[self.step][2]-self.parameters[self.step-1][2]]
            fenmu = self.ISEresult[self.step]-self.ISEresult[self.step-1]
            
        temp = abs(fenzi/fenmu)
        gamma = [self.lamdap*temp, self.lamdai*temp, self.lamdad*temp]
        return gamma
    
    def updateK(self, error, step):
             self.error.append(error)
             self.step = step
             
             result_ISE = self.ISE()
             result_gamma = self.gamma()
             
               
    def SetParameter(self, k):
        self.kp = k[0]
        self.ki = k[1]
        self.kd = k[2]
    
    def getSum(self):
        return self.error_sum
    
    def pid(self, e):
        self.error_sum += e
        if self.error_sum>self.error_sum_max: 
            self.error_sum = self.error_sum_max
        if self.error_sum<self.error_sum_min: 
            self.error_sum = self.error_sum_min

        det = e - self.last_error
        u = self.kp*e + self.ki*self.error_sum +self.kd*det
        self.last_error = e
        
        return u
    
    
        
