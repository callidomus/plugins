{{
form.guiInput('serialport', required=None, label='Device of the Reader', help="""Devicename of the Reader the e.g. /dev/ir.schake.12345""")

select_baud = oDict([('auto', 'Auto'), ('300', '300 Baud'), ('600', '600 Baud'), ('1200', '1200 Baud'), ('2400', '2400 Baud'), ('4800', '4800 Baud'), ('9600', '9600 Baud')])
form.guiSelect('baudrate', label='Baudrate', named=select_baud, help="""sets the baudrate used for reading from the meter - can be used to force specific baudrate (300,600,1200,2400,4800,9600,auto - default: 'auto')""")

select_data = oDict([('30', '30 Sekunden'), ('60', '1 Minute'), ('120', '2 Minuten'), ('300', '5 Minuten'), ('600', '10 Minuten')])
form.guiSelect('update_cycle', label='Abfrageintervall', named=select_data, help="""interval in seconds how often the data is read from the meter - be careful not to set a shorter interval than a read operation takes (default: 60)""")

select_yesno = oDict([('1', 'yes'), ('0', 'no')])
form.guiSelect('use_checksum', label='Use Checksum', named=select_yesno, help="""controls the checksum check of the received data - disable if you get continuous checksum errors/timeouts (yes/no - default: yes)""")

select_yesno = oDict([('1', 'yes'), ('0', 'no')])
form.guiSelect('reset_baudrate', label='Reset Baudrate', named=select_yesno, help=""" determines if the baudrate is reset to 300 baud in every read cycle or left at full speed - disable to improve performance if your meter allows it (yes/no - default: yes)""")

select_yesno = oDict([('1', 'yes'), ('0', 'no')])
form.guiSelect('no_waiting', label='No Waiting', named=select_yesno, help="""omit additional waiting times required for some meters - enable to improve performance if your meter allows it (yes/no - default: no)""")

}}
