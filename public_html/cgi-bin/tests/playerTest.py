import unittest
from Player import *
class TestPlayer(unittest.TestCase):

    def test_constructor(self):
        #tests constructor sets id
        p = Player("foo_id")
        self.assertEqual(p.getID(), 'foo_id')

    def test_increaseScore(self):
        #tests increaseScore inceases score
        p = Player("")
        self.assertEqual(p.getScore(), 0)
        p.increaseScore(20)
        self.assertEqual(p.getScore(), 20)
        p.increaseScore(20)
        self.assertEqual(p.getScore(), 40)

    def test_createMeeples(self):
        #tests createMeeples creates 8 meeples
        p = Player("")
        p.createMeeples()
        self.assertEqual(len(p._inactiveMeeples), 8)
        self.assertEqual(p.meeplesAvailable(), 8)

    def test_getMeeple(self):
        #tests getMeeple
        p = Player("")
        p.createMeeples()
        p.getMeeple()
        self.assertEqual(p.meeplesAvailable(), 7)
        self.assertEqual(len(p._activeMeeples), 1)

    def test_takeBack(self):
        #tests takeBack
        p = Player("")
        p.createMeeples()
        m = p.getMeeple()
        p.takeBack(m)
        self.assertEqual(p.meeplesAvailable(), 8)
        self.assertEqual(len(p._activeMeeples), 0)
        
        
        

if __name__ == '__main__':
    unittest.main()
