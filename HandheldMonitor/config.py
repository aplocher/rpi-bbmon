class Config:
    voice_output_enabled = True

    remote_temperature_enabled = True
    # Thresholds are in Celsius
    remote_temperature_threshold_high = 31.0
    remote_temperature_threshold_low = 18.0
    # If voice is enabled, say these outloud when a threshold limit is crossed
    remote_temperature_threshold_high_say = 'Warning, high temperature, {fahr} degrees fahrenheit'
    remote_temperature_threshold_low_say = 'Warning, low temperature, {fahr} degrees fahrenheit'
    # Or, celsius
    #remote_temperature_threshold_low_say = 'Warning, low temperature, {cels} degrees celsius'
    #remote_temperature_threshold_high_say = 'Warning, high temperature, {cels} degrees celsius'
    remote_temperature_line1_format = 'Nursery Temp.'
    remote_temperature_line2_format = '{fahr:0.1f}-f / {cels:0.1f}-c'
    # Or, celius only
    #remote_temperature_line2_format = '{cel:0.1f}-c'
    # Or, f only
    #remote_temperature_line2_format = '{far:0.1f}-f'

    remote_audio_sensor_enabled = True
    # Lower number means it will trigger more often (likely more false positives)
    remote_audio_sensor_sensitivity = 730
    # If voice_output_enabled, this will be said when a sound is detected
    remote_audio_sensor_say = 'Warning, sound detected'
    remote_audio_sensor_line1 = '!! WARNING !!'
    remote_audio_sensor_line2 = '*Sound detected*'

    front_leds_enabled = True