{{
select_data = oDict([('', ''),
    ('6400_00260100', 'Ertrag Gesamt'),
    ('6400_00262200', 'Ertrag Heute'),
    ('6200_40263F00', 'Aktuelle Leistung'),
    ('6180_08214800', 'Gerätestatus')])
form.guiSelect('sma_wr', label='Wert', named=select_data)
}}
