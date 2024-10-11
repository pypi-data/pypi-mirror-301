from nc_mis.drivers.aruba.aos.AOS import AOS

device = AOS(ip='10.0.0.1', user='AdminUser', password='VeryUniquePassword')

# Return raw running config
device_config = device.get_config()

# Save config to file
device.backup_config(path='/opt/ncubed/backup/')

# Push command with rollback on failure
device.send_config(commands=['configure terminal', 'interface1/1/1', 'shutdown'])

