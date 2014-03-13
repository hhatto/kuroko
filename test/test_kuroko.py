import unittest
from kuroko import Bot, timer


class TestDecorator(unittest.TestCase):

    def test_timer_arg(self):
        class TestBot(Bot):
            @timer(5)
            def _tt(self):
                pass
        b = TestBot()
        self.assertEqual(True, callable(b.funcs[0]['options']['callback']))

    def test_timer_noarg(self):
        class TestTimerNoargBot(Bot):
            @timer
            def _test_timer_noarg(self):
                pass
        bb = TestTimerNoargBot()
        self.assertEqual(True, callable(bb.funcs[0]['options']['callback']))


if __name__ == '__main__':
    unittest.main()
