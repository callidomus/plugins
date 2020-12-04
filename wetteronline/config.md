{{

form.guiInput('location', label='Ort', required=True, value='Berlin', help="""Ortsname wie er für das HTML-Widget von WetterOnline funktioniert (https://www.wetteronline.de/wetter-widget)""")

select_cycle = oDict([('60', '1 Minute'), ('300', '5 Minuten'), ('900', '15 Minuten'), ('1800', '30 Minuten'), ('3600', '1 Stunde')])
form.guiSelect('cycle', label='Abfrageintervall', named=select_cycle)

}}

