{{                                                                                                                                                                               select_data = oDict([
    ('', ''),
    ('_0', '== Heute =='),                               
    ('0__title', 'Wetterlage'),
    ('0__img', 'Icon'),
    ('0__temp_now', 'Temperatur aktuell (°C)'),
    ('0__temp_min', 'Temperatur min. (°C)'),
    ('0__temp_max', 'Temperatur max. (°C)'),
    ('0__sunhours', 'Sonnenstunden (h)'),
    ('0__rain_probability', 'Regenwahrscheinlichkeit (%)'),

    ('_1', '== Morgen =='),
    ('1__title', 'Wetterlage'),
    ('1__img', 'Icon'),                               
    ('1__temp_min', 'Temperatur min. (°C)'),
    ('1__temp_max', 'Temperatur max. (°C)'),
    ('1__sunhours', 'Sonnenstunden (h)'),
    ('1__rain_probability', 'Regenwahrscheinlichkeit (%)'),

    ('_2', '== Übermorgen =='),                               
    ('2__title', 'Wetterlage'),
    ('2__img', 'Icon'),
    ('2__temp_min', 'Temperatur min. (°C)'),
    ('2__temp_max', 'Temperatur max. (°C)'),
    ('2__sunhours', 'Sonnenstunden (h)'),
    ('2__rain_probability', 'Regenwahrscheinlichkeit (%)'),
])
form.guiSelect('wetteronline', label='Wert', named=select_data)
}}