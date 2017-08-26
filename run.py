import json, importlib, pkgutil
from endrebot0 import EndreBot, log

log.info('endrebot0 v0.4.0')

with open('config.json') as f:
	cfg = json.load(f)
	bot = EndreBot(cfg)

for _, name, _ in pkgutil.iter_modules(['endrebot0/commands']):
	log.debug('Loading module %s', name)
	module = importlib.import_module('endrebot0.commands.' + name)
	bot.add_module(module)

bot.run()

log.shutdown()
