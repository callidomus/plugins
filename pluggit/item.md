{{
select_data = oDict([('', ''), ('prmRamIdxUnitMode', 'Unit Mode'), ('prmNumOfWeekProgram', 'Week program'), ('prmRomIdxSpeedLevel', 'Fan speed'),('prmFilterRemainingTime', 'Filter time remaning'), ('prmRamIdxT1', 'Outdor temperature T1'), ('prmRamIdxT2', 'Supply temperature T2'), ('prmRamIdxT3', 'Extract temperature T3'), ('prmRamIdxT4' , 'Exhaust temperature T4')])
form.guiSelect('pluggit_listen', label='Listen', named=select_data)

select_data = oDict([('', ''), ('activatePowerBoost', 'Power Boost Aktivieren'), ('setFanSpeed', 'Set Fan Speed 0-4'), ('2', 'Zwei')])
form.guiSelect('pluggit_send', label='Send', named=select_data)
}}