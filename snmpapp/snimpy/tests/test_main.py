import sys
import os
import tempfile
import code  # noqa: F401
import mock
import platform
from snimpy.main import interact
from multiprocessing import Process
import agent
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestMain(unittest.TestCase):

    """Test the main shell"""

    @classmethod
    def setUpClass(cls):
        cls.agent = agent.TestAgent()

    @classmethod
    def tearDownClass(cls):
        cls.agent.terminate()

    @unittest.skipIf(platform.python_implementation() == "PyPy",
                     "setupterm seems unreliable with Pypy")
    def test_loadfile(self):
        script = tempfile.NamedTemporaryFile(delete=False)
        try:
            script.write("""
load("IF-MIB")
m = M(host="127.0.0.1:{0}",
      community="public",
      version=2)
assert(m.ifDescr[1] == "lo")
""".format(self.agent.port).encode("ascii"))
            script.close()
            with mock.patch("code.InteractiveInterpreter.write"):
                p = Process(target=interact, args=((script.name,),))
                p.start()
                p.join()
                self.assertEqual(p.exitcode, 0)
        finally:
            os.unlink(script.name)
