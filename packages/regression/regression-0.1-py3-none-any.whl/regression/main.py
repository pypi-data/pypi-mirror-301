import matplotlib.pyplot as mlt
import numpy as np
class linearRegression:
    lowest=[0,0,1000]
    def train(self, x:list, y:list) -> None:
        """x: list -> features. y list -> labels. Train the model."""
        self.x, self.y=self.sepXY(self.sortByX(x,y))
        self.main()
    
    def sortByX(self,x:list, y:list):
        xyCombine = []
        for index, item in enumerate(x):
            xyCombine.append((item, y[index]))
        xyCombine.sort(key=lambda x :x[0] )
        return xyCombine
    def sepXY(self,xyCombine : list):
        x=[]
        y=[]
        for item in xyCombine:
            x.append(item[0])
            y.append(item[1])
        return x, y

    def func(self, x1,y1,x2,y2):
        """give linear equation which has solution x1, y1 and x2, y2"""
        # y1 = m.x1 + c
        # y2 = m.x2 + c
        
        m= (y1-y2)/(x1-x2)
        c= y1-m*x1
        return (m,c)
    def plotDataPoints(self):
        mlt.scatter(self.x,self.y)
    def plotFunc(self):
        """plot the regression function."""
        m=self.lowest[0]
        c=self.lowest[1]
        x1=self.x[0]
        x2=self.x[-1]+5
        y1 = m*x1 + c
        y2 = m*x2 + c
        mlt.plot([x1,x2],[y1,y2],color="green")
    def up(self,m,c)-> int:
        """give numbers of data point above the function"""
        noOfUpperY=0
        for index, item in enumerate(self.x):
            thatY = m*item + c # what the linear func give at that x in list
            difY=self.y[index] - thatY # give difference of actual y and predicted y
            if difY>0: # if difference is +ve
                
                noOfUpperY+=1
            
        return noOfUpperY
    def down(self,m,c)->int: 
        """ give number of data point below the function."""
        noOfDownY=0
        for index, item in enumerate(self.x):
            thatY = m*item + c # what the linear func give at that x in list
            difY=self.y[index] - thatY # give difference of actual y and predicted y
            if difY<0: # if difference is -ve
                noOfDownY+=1
        return noOfDownY
    
    def error(self,up,down):
        """return the total error. """
        dif = up-down
        if (dif<0): 
            dif = -1*dif
        return dif
    def predict(self,x):
        """predict the y"""
        m=self.lowest[0]
        c=self.lowest[1]

        result=m*x+c
        return result
    def graphDirectionUp(self)-> bool:
        """tell if graph is inclined or declined"""
        y=self.y
        tenPercent = int(len(y)*0.1)
        firstgroup = y[0:tenPercent]
        lastgroup = y[-tenPercent:-1]
        firstlen = len(firstgroup)
        npfirst = np.array(list(firstgroup))
        firstmean = npfirst.sum()/firstlen
        lastlen = len(lastgroup)
        nplast = np.array(list(lastgroup))
        lastmean = nplast.sum()/lastlen
        if lastmean>firstmean:
            return True
        else:
            return False

    def main(self):
        """find best suited function for the given data"""
        lowest =[0,0,100000000]
        for item in np.linspace(0,max(self.y),1000):
            if self.graphDirectionUp():
                m,c=self.func(self.x[0],self.y[0],self.x[-1],item)
                err = self.error(self.up(m,c),self.down(m,c))
    

                if(lowest[2]>err):
                    lowest[0]=m
                    lowest[1]=c
                    lowest[2]=err
            else:
                m,c=self.func(self.x[-1],self.y[-1],self.x[0],item)
                err = self.error(self.up(m,c),self.down(m,c))
            
                if(lowest[2]>err):
                    lowest[0]=m
                    lowest[1]=c
                    lowest[2]=err
        self.lowest[0] = lowest[0]
        self.lowest[1]=lowest[1]
        self.lowest[2] = lowest[2]
    def regressionFunc(self)-> tuple:
        """return the function which bwst suited the data"""
        return (self.lowest[0],self.lowest[1])
    

