{{

form.guiInput('ip', label='IP Wechselrichter', pattern='ip', required=True)

select_right = oDict([('istl', 'Installateur'), ('usr', 'Benutzer')])
form.guiSelect('username', label='Benutzername', named=select_right)

form.guiInput('password', label='Passwort')

select_cycle = oDict([('10', '10 Sekunden'), ('60', '1 Minute'), ('300', '5 Minuten'), ('900', '15 Minuten'), ('1800', '30 Minuten')])
form.guiSelect('cycle', label='Abfrageintervall', named=select_cycle)

}}
