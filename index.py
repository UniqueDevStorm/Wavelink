import discord
import wavelink
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(command_prefix=["!"])

        self.add_cog(Music(self))

    async def on_ready(self):
        print(f"Logged in as {self.user.name} | {self.user.id}")


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(
            host="127.0.0.1",
            port=2333,
            password="123456",
            region="eu",
            rest_uri="http://127.0.0.1:2333",
            identifier="FreeAI",
        )

    @commands.command(name="connect")
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            channel = ctx.author.voice.channel
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.is_connected:
            return

        if not channel.id:
            return await ctx.send("대충 이상한 채널")

        await ctx.send(f"Connecting to {channel.name}")
        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f"ytsearch:{query}")

        if not tracks:
            return await ctx.send("Could not find any songs with that query.")

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f"Added {str(tracks[0])} to the queue.")
        await player.play(tracks[0])

    @commands.command(name="eq")
    async def equalizer(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send("대충 노래 안틀음")

        await ctx.send("멋진 부스트 이퀄라이져")
        await player.set_eq(wavelink.Equalizer.boost()) @ commands.command(
            aliases=["ㅔㅣ묘", "재생"]
        )


Bot().run("NjkwMDUxODkxMzQxNjg4ODU3.XnLy5w.AeNomrXD0kkAZxYwjhUzyafl8XY")