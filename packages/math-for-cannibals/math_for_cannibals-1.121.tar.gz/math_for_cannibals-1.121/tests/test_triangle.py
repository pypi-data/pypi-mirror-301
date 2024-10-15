import unittest
import program.RightTriangle as RightTriangle


class TestRightTriangle(unittest.TestCase):

    def testBSideBDegree(self):
        Rt = RightTriangle.RightTriangle(bSide=5, aDegree=20).get_triangle()
        anglesAndDegrees = {"bSide": 5, "cSide": 5.320, "aSide": 1.819, "aDegree": 20, "cDegree": 90, "bDegree": 70}

         # Compare the sides
        self.assertAlmostEqual(Rt['bSide'], anglesAndDegrees['bSide'], places=2)
        self.assertAlmostEqual(Rt['cSide'], anglesAndDegrees['cSide'], places=2)
        self.assertAlmostEqual(Rt['aSide'], anglesAndDegrees['aSide'], places=2)
        
        # Compare the angles
        self.assertAlmostEqual(Rt['aDegree'], anglesAndDegrees['aDegree'], places=1)
        self.assertAlmostEqual(Rt['bDegree'], anglesAndDegrees['bDegree'], places=1)
        self.assertEqual(Rt['cDegree'], anglesAndDegrees['cDegree'])  # Exact match since cDegree is always 90

        # assertAlmostEqual er god til floates fordi der ofte er "afrundingsfejl". For at fikse disse fejl sætter vi et tolerance niveau
        # Tolerence niveaut er hvor mange decimale pladser bliver tjekket.


    def testCalculateAnglesByAngles(self):
        Rt = RightTriangle.RightTriangle(aDegree=20).get_triangle()
        anglesAndDegrees = {"aDegree": 20,  "bDegree": 70, "cDegree": 90}

        self.assertEqual(Rt['aDegree'], anglesAndDegrees["aDegree"])
        self.assertEqual(Rt['bDegree'], anglesAndDegrees["bDegree"])
        self.assertEqual(Rt['cDegree'], anglesAndDegrees["cDegree"])


    def testPythagoreamTheroem(self):
        sides = RightTriangle.RightTriangle(aSide=2, bSide=3).get_sides()
        cSide = 3.60555

        self.assertAlmostEqual(sides['cSide'], cSide, places=3)


    def testCalculateDegreesWithSides(self):
        calculatedDegrees = RightTriangle.RightTriangle(aSide=2, bSide=3).get_degrees()
        degrees = {'aDegree': 33.690, "bDegree": 56.31, "cDegree": 90}

        self.assertAlmostEqual(calculatedDegrees["aDegree"], degrees["aDegree"], places=3)
        self.assertAlmostEqual(calculatedDegrees["bDegree"], degrees["bDegree"], places=3)
        self.assertEqual(calculatedDegrees["cDegree"], degrees["cDegree"])

    def testCalculateArea(self):
        caclulateArea = RightTriangle.RightTriangle(bSide=2, cSide=3).get_triangle()
        area = 2.2360

        self.assertAlmostEqual(caclulateArea["area"], area, places=3)




    
# python -m unittest tests/test_triangle.py