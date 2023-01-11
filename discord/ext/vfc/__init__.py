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

HasIDType = (
    discord.Member
    | discord.Object
    | discord.abc.Snowflake
)
ContextType = (
    commands.Context
    | HasIDType
    | int
)


class VFCCheckFailure(commands.CheckFailure):
    pass


class CheckType(enum.Enum):
    USER = enum.auto()
    GUILD = enum.auto()


def guild_is_active(product_name: str):
    async def predicate(ctx: ContextType | discord.Guild):
        if isinstance(ctx, commands.Context):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
            guild_id = ctx.guild.id
        elif isinstance(ctx, int):
            guild_id = ctx
        else:
            guild_id = ctx.id
        v = await vfcheckout.async_.check(
            product_name=product_name,
            guild_id=guild_id,
        )
        if v:
            return True
        raise VFCCheckFailure("No active purchase for this guild.")
    return commands.check(predicate)


def user_is_active(product_name: str):
    async def predicate(ctx: ContextType):
        if isinstance(ctx, commands.Context):
            user_id = ctx.author.id
        elif isinstance(ctx, int):
            user_id = ctx
        else:
            user_id = ctx.id
        v = await vfcheckout.async_.check(
            product_name=product_name,
            user_id=user_id,
        )
        if v:
            return True
        raise VFCCheckFailure("No active purchase for this user.")
    return commands.check(predicate)
