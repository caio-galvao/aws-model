from unittest import main, TestCase

from new_aws_model import otimizaModelo

#Tests for the model
#Checking only the total cost

class TestNewAWSModel(TestCase):

#    def test1(self):
#        t = 5
#        demand = [10, 10, 10, 10, 10]
#        p_od = 5
#        p_re = 1
#        u = 2
#        y = 2
#
#        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y), 120)

    def testOnDemand(self):
        t = 5
        demand = [10, 10, 10, 10, 10]
        p_od = 5
        p_re = 100
        u = 100
        y = 2

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 250)

    def testReservedPar(self): #Nas reservas, deve impedir tempos negativos
        t = 4
        demand = [10, 10, 10, 10]
        p_od = 100
        p_re = 1
        u = 2
        y = 2

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 80)

    def testReservedImpar(self): #Deve considerar que está reservando no futuro
        t = 5
        demand = [10, 10, 10, 10, 10]
        p_od = 100
        p_re = 1
        u = 2
        y = 2

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 120)

    def testReservedAllUp(self):
        t = 4
        demand = [10, 10, 10, 10]
        p_od = 100
        p_re = 0
        u = 4
        y = 2

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 80)
    
    def testReservedNoUp(self):
        t = 4
        demand = [10, 10, 10, 10]
        p_od = 100
        p_re = 2
        u = 0
        y = 2

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 80)

    def testAmbos(self):
        t = 5
        demand = [10, 10, 10, 10, 10]
        p_od = 3
        p_re = 1
        u = 2
        y = 2

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 110)
    
    def testc42xlarge(self):
        t = 8
        demand =  [10, 10, 109, 20, 30, 40, 50 , 75]
        p_od = 0.398
        p_re = 0.242 #effective hourly rate
        u = 0
        y = 8760 #1 year
        result = otimizaModelo(t, demand, p_od, p_re, u, y)

        self.assertEqual(otimizaModelo(t, demand, p_od, p_re, u, y)[0], 110)

if __name__ == '__main__':
    main()