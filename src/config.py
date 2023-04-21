# config.py
import configparser
ConfigPraser = configparser.ConfigParser()
ConfigPraser.read('config.ini')

Config = {
    'SCREEN_SIZE': [int(x) for x in ConfigPraser['general']['SCREEN_SIZE'].split(', ')],
    'BACKGROUND_COLOR': [int(x) for x in ConfigPraser['general']['BACKGROUND_COLOR'].split(', ')],
    'FPS': int(ConfigPraser['general']['FPS']),

    'CELLS': int(ConfigPraser['grid']['CELL_SIZE']),
    'DECAY_RATE': int(ConfigPraser['grid']['DECAY_RATE']),
}
