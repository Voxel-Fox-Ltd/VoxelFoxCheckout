import enum

import discord
from discord.ext import commands
import vfcheckout


__all__ = (
    'VFCCheckFailure',
    'CheckType',
    'guild_is_active',
    'user_is_active',
)


class VFCCheckFailure(commands.CheckFailure):
    pass


class CheckType(enum.Enum):
    USER = enum.auto()
    GUILD = enum.auto()


def guild_is_active(product_name: str):
    async def predicate(ctx: commands.Context | discord.Member | discord.Guild):
        if isinstance(ctx, discord.Guild):
            guild = ctx
        else:
            guild = ctx.guild
        if guild is None:
            raise commands.NoPrivateMessage()
        v = await vfcheckout.async_.check(
            product_name=product_name,
            guild_id=guild.id,
        )
        if v:
            return True
        raise VFCCheckFailure("No active purchase for this guild.")
    return commands.check(predicate)


def user_is_active(product_name: str):
    async def predicate(ctx: commands.Context | discord.Member):
        if isinstance(ctx, discord.Member):
            member = ctx
        else:
            member = ctx.author
        v = await vfcheckout.async_.check(
            product_name=product_name,
            user_id=member.id,
        )
        if v:
            return True
        raise VFCCheckFailure("No active purchase for this user.")
    return commands.check(predicate)
