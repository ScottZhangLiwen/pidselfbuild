from numpy import abs


class selfbuild():
    
    def __init__(self, k, n):
        self.ISEresult = []
        self.error_laststep = 0
        
        self.k_initial = k
        self.factor = 1.0/n
        self.error = []
        
        self.k = [k]
        self.k_last = []
        
        self.n_scale = n
        self.step = 0
        self.lamda = 0.5;
        self.scaleP = 1;
        self.scaleI = 1;
        self.scaleD = 1;
        
    def ISE(self):
        sum = 0
        if self.step<self.n_scale:
            for item in self.error:
                sum += item*item
        else:
            for item in self.error[self.step-self.n:self.setp]:
                sum += item*item
        return sum*self.factor
    
    def gamma(self,):
        if self.step==0:
            fenziP = 0
            fenmuP = 1
            fenziI = 0
            fenmuI = 1
            fenziD = 0
            fenmuD = 1
        elif self.step==1:
            fenziP = self.k_last[0][0]
            fenmuP = self.ISEresult[0]
            fenziI = self.k_last[0][1]
            fenmuI = self.ISEresult[0]
            fenziD = self.k_last[0][2]
            fenmuD = self.ISEresult[0]
        else:
            fenziP = abs(self.k_last[self.step-1][0]-self.k_last[self.step-2][0])
            fenmuP = abs(self.ISEresult[self.step-1]-self.ISEresult[self.step-2])
            fenziI = abs(self.k_last[self.step-1][1]-self.k_last[self.step-2][1])
            fenmuI = abs(self.ISEresult[self.step-1]-self.ISEresult[self.step-2])
            fenziD = abs(self.k_last[self.step-1][2]-self.k_last[self.step-2][2])
            fenmuD = abs(self.ISEresult[self.step-1]-self.ISEresult[self.step-2])
            
        return [self.lamda*fenziP/fenmuP, self.lamda*fenziI/fenmuI, self.lamda*fenziD/fenmuD]
    
    def updateK(self, error, step): 
        self.error.append(error)
        self.step = step
        
        result_ISE = self.ISE()
        result_gamma = self.gamma()
        
        if result_ISE>self.error_laststep:
            self.scaleD = -self.scaleD
            self.scaleP = -self.scaleP
            self.scaleI = -self.scaleI
        
        result_kP = self.k[self.step-1][0] + result_gamma[0]*self.scaleP*result_ISE
        result_kI = self.k[self.step-1][1] + result_gamma[1]*self.scaleI*result_ISE
        result_kD = self.k[self.step-1][2] + result_gamma[2]*self.scaleD*result_ISE
        
        self.k.append([result_kP, result_kI, result_kD])
        self.ISEresult.append(result_ISE)
        return [result_kP, result_kI, result_kD]
    
    
    
    