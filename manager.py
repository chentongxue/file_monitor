# coding=utf-8
from config_parser import ConfigParser
from monitor import FileMonitorHandler
from observer import observer


config = ConfigParser('config.cfg')

for task in config['TASKS']:
    file_monitor = FileMonitorHandler(
        directory=task['directory'],
        keywords=task['keywords'],
        bot_api=config.get('BOT_API'),
        alert_cd=config['ALERT_CD'],
        suffix=task['suffix'],
        name=task['name'],
    )
    file_monitor.run()

observer.start()
observer.join()
