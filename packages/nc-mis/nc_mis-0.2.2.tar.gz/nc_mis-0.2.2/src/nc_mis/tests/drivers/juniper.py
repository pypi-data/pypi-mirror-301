import unittest

from drivers.aruba.aos.AOS import AOS
from drivers.juniper.JUNOS import JUNOS
from helpers.logger import logger


class TestJuniper(unittest.TestCase):
    device = JUNOS(ip="0.0.0.0",
                    username="user",
                    password="password"
                    )

    def setUp(self):
        logger()

    def test_JUNOS_deploy_config(self):
        test_config = ''

    def tearDown(self):
        with self.device as connected_device:
            connected_device.rollback()

if __name__ == '__main__':
    unittest.main()
