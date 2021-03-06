import asyncio, discord
from ..command import *

@command
async def ping(ctx):
	await ctx.message.edit(content='pong')
	return ctx.message.edited_at - ctx.message.created_at

@command
async def delete(ctx, qty=0):
	await ctx.message.delete()
	for _ in range(qty):
		m = await ctx.bot.wait_for('message', check=lambda m: (m.channel, m.author) == (ctx.channel, ctx.author))
		await m.delete()

@command
async def game(ctx, game, status=None):
	status = discord.Status[status] if status else discord.Status.online
	await ctx.bot.change_presence(status=status, game=discord.Game(name=game))
	await ctx.message.delete()

afk_targets = None

async def afk_send(ctx, message_key, *args, **kwargs):
	global afk_targets
	if afk_targets is None:
		afk_targets = {channel.id: channel for channel in ctx.bot.get_all_channels() if isinstance(channel, discord.TextChannel)}
		afk_targets.update({mem.id: mem for mem in ctx.bot.get_all_members() if mem.bot})
	
	for info in ctx.bot.config['afk_messages']:
		if message_key in info:
			trigger = await afk_targets[info['dest']].send(info[message_key].format(*args, **kwargs))
			try:
				response = await ctx.bot.wait_for('message', check=lambda m: m.channel == trigger.channel, timeout=10)
				await response.ack()
			except asyncio.TimeoutError:
				pass
	
	await ctx.message.delete()

@command
async def afk(ctx, *args, status=None, **kwargs):
	await afk_send(ctx, 'afk_message', *args, **kwargs)
	if status == 'offline':
		await ctx.bot.change_presence(status=discord.Status.invisible)
	elif status is not None:
		await ctx.bot.change_presence(status=discord.Status[status], game=discord.Game(name='AFK: ' + ', '.join(args)))

@command
async def unafk(ctx, *args, **kwargs):
	await afk_send(ctx, 'unafk_message', *args, **kwargs)

@command
async def purge(ctx, qty, self=True):
	check = (lambda m: m.author == ctx.author) if self else None
	await ctx.channel.purge(limit=qty+1, check=check)
