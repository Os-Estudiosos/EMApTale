import unittest
import os
import sys
import math
sys.path.append(os.getcwd())
from utils import radians_to_degrees, reduce_angle, get_positive_angle


class RadiansToDegreesTest(unittest.TestCase):
    def test_zero(self):
        """Testa se está convertendo os valores corretamente"""
        self.assertAlmostEqual(radians_to_degrees(0), 0, places=6)
        self.assertAlmostEqual(radians_to_degrees(math.pi), 180, places=6)
        self.assertAlmostEqual(radians_to_degrees(math.pi / 2), 90, places=6)
        self.assertAlmostEqual(radians_to_degrees(2 * math.pi), 360, places=6)

    def test_negative_radian(self):
        """Testa se os valores negativos estão convertendo normalmente"""
        self.assertAlmostEqual(radians_to_degrees(-math.pi), -180, places=6)

    def test_errors(self):
        """Testa se estão levantando erros"""
        with self.assertRaises(TypeError):
            radians_to_degrees("")
            radians_to_degrees([121])
            radians_to_degrees(complex(1, 2))
            radians_to_degrees(())
            radians_to_degrees({})


class QuadrantReductionTest(unittest.TestCase):
    def test_reducing_correctly(self):
        """Testa se a função está reduzindo corretamente"""
        self.assertEqual(reduce_angle(0), 0)

        self.assertEqual(reduce_angle(45), 45)
        self.assertEqual(reduce_angle(360), 0)  # Verifica se 360 é reduzido a 0

        self.assertEqual(reduce_angle(450), 90)
        self.assertEqual(reduce_angle(720), 0)
        self.assertEqual(reduce_angle(1080), 0)

        self.assertEqual(reduce_angle(-45), 315)
        self.assertEqual(reduce_angle(-360), 0)

        self.assertEqual(reduce_angle(-450), 270)
        self.assertEqual(reduce_angle(-720), 0)
        self.assertEqual(reduce_angle(-1080), 0)
    
    def test_errors(self):
        """Testa se estão levantando erros"""
        with self.assertRaises(TypeError):
            reduce_angle("")
            reduce_angle([121])
            reduce_angle(complex(1, 2))
            reduce_angle(())
            reduce_angle({})



class PositiveAngleCorrectionTest(unittest.TestCase):
    def test_getting_positives_correctly(self):
        """Testa se estão retornando os valores corretamente"""
        self.assertEqual(get_positive_angle(0), 0)

        self.assertEqual(get_positive_angle(45), 45)
        self.assertEqual(get_positive_angle(360), 360)
        self.assertEqual(get_positive_angle(720), 720)

        self.assertEqual(get_positive_angle(-45), 315)
        self.assertEqual(get_positive_angle(-360), 0)
        self.assertEqual(get_positive_angle(-270), 90)

        self.assertEqual(get_positive_angle(-450), 270)
        self.assertEqual(get_positive_angle(-720), 0)
        self.assertEqual(get_positive_angle(-1080), 0)
    
    def test_errors(self):
        """Testa se estão levantando erros"""
        with self.assertRaises(TypeError):
            get_positive_angle("")
            get_positive_angle([121])
            get_positive_angle(complex(1, 2))
            get_positive_angle(())
            get_positive_angle({})
