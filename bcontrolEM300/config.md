{{
form.guiInput('host', label='Host', required=None, help="""IP Adresse der EM300 LR""")
select_data = oDict([('10', '10 Sekunden'), ('60', '1 Minute'), ('300', '5 Minuten'), ('900', '15 Minuten'), ('1800', '30 Minuten')])
form.guiSelect('cycle', label='Abfrageintervall', named=select_data)
}}
