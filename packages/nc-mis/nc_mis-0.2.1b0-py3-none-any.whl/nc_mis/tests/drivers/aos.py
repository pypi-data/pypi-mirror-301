import unittest

from nc_mis.drivers.aruba.aos.AOS import AOS
from nc_mis.drivers.juniper.JUNOS import JUNOS
from nc_helpers.logger import logger


class TestAOS(unittest.TestCase):
    device = AOS(ip="0.0.0.0",
                    username=None,
                    password=None
                    )

    def setUp(self):
        self.device = AOS(ip="0.0.0.0",
            username=None,
            password=None
            )
    #     logger()

    def test_AOS_parse_hostname(self):
        test_config = '''
        Current configuration:
!
!Version ArubaOS-CX Virtual.10.09.1000
!export-password: default
hostname IT-CX2
user admin group administrators password ciphertext AQBapROYOrQuGvCcXioBboIhhnn3mQ35WuU1jpJVF1hLd4mSYgAAAGdGXVs4Spi8vleRSa5hzTltKWI5qksAVi8Q6i4n6mCsq1dRXC1osj/pOUsNZeH+v1FLlOZZ0TTYz+lZ9jXIPEwOfQdahSsDS0ob1Iea0mFAJGM4YyDOW3WxkQSUJyjaoOMs
user nc-admin group administrators password ciphertext AQBapbnycG8p/jh9jopz8cYG9xLUuHpOH9fZT9G5HYnPpPLlYgAAAKzSLSZJNkDvreaehpi0trWgfr5FPPJcNpIweI79qz1Jja3NaJSIpUSMXdyG7aoiZHeICCo4WRv0apuIoF6bVfN1vUgYcL9X42n3BT45zs3ISso4b7P5PNc/lwdFOQ1ZwD2P
led locator on
sflow
sflow collector 192.168.0.56
sflow sampling 1
sflow polling 10
ntp server pool.ntp.org minpoll 4 maxpoll 4 iburst
ntp enable
!
!
!
!
!
!
ssh server vrf mgmt
vlan 1
spanning-tree
spanning-tree instance 1 vlan 1-4094
interface mgmt
    no shutdown
    ip static 192.168.3.1/20
    default-gateway 192.168.0.1
interface lag 1
    no shutdown
    no routing
    vlan trunk native 1 tag
    vlan trunk allowed all
    lacp mode active
interface 1/1/1
    no shutdown
    ip address 10.3.0.3/31
interface 1/1/2
    no shutdown
interface 1/1/3
    no shutdown
    lag 1
interface 1/1/4
    no shutdown
    lag 1
snmp-server vrf mgmt
snmp-server community public
vsx
    inter-switch-link lag 1
    role secondary
    vsx-sync snmp ssh vsx-global
!
!
!
!
!
https-server vrf mgmt
        '''
        oc = self.device.parse_to_openconfig(config=test_config)
        print(oc)

    # def tearDown(self):
    #     with self.device as connected_device:
    #         connected_device.rollback()

if __name__ == '__main__':
    unittest.main()
