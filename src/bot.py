import os
import discord
from discord.ext.commands import Bot
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    @discord.ui.button(label="Verify",custom_id = "Verify",style = discord.ButtonStyle.success)
    async def verify(self, button, interaction):
        # Put your verified role id below
        role = 1174195647973441567
        user = interaction.user
        if role not in [y.id for y in user.roles]:
            await user.add_roles(user.guild.get_role(role))
            await user.send("You have been verified!")
            return
        return

class Buy(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Buy", custom_id="Buy", style=discord.ButtonStyle.green)
    async def buy(self, button: discord.Button, interaction: discord.Interaction):
        channel_name = f"{interaction.user.name}-order"
        category = discord.utils.get(interaction.guild.categories, name="Orders")
        channel = await interaction.guild.create_text_channel(name=channel_name, category=category)
        embed = discord.Embed(title="Buy Order",
                      description="This is a buy order for one of ComboGang's Services\n\nStart of by answering these questions:\n1. What type of service are you ordering(Minecraft, Website, Desktop, Active Chatter).",
                      colour=0x00b0f4,
                      timestamp=datetime.now())

        embed.set_footer(text="Made by combogang")
        await channel.set_permissions(interaction.guild.get_role(interaction.guild.id), send_messages=False, read_messages=False)
        # Put your owner, or ticket support id below
        await channel.set_permissions(interaction.guild.get_role(1174195359925411860), send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        await channel.set_permissions(interaction.message.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        await channel.send(embed=embed)
        # Put your owner or ticket support id below
        combo = discord.utils.get(interaction.guild.roles, id=1174195359925411860)
        await channel.send(f"{combo.mention}")



class Combo(Bot):
    """Main class for the bot
    
    Args:
        Token (str): The token for the bot so it can start
    
    
    """
    def __init__(self, token: str, **options) -> None:
        super().__init__(command_prefix="!", options=options)
        self.token = token

            
    async def start(self) -> None:
        """Starts the bot with the given token"""
        return await super().start(self.token, reconnect=True)

    
    async def on_ready(self):
        """Hook for when the bot is ready"""
        logger.debug("Bot ready")
        # Put your verify channel id below
        await self.get_channel(1174196732662382602).purge(limit=500)
        # Put your buy order channel id below
        await self.get_channel(1174197503852290058).purge(limit=500)
        # Put your verify channel id below
        embed = discord.Embed(title = "Verification", description = "Click below to verify.")
        await self.get_channel(1174196732662382602).send(embed = embed, view = Verification())
        embed2 = discord.Embed(title="Buy Order", description="Click below to create a buy order")
        # Put your buy order channel id below
        await self.get_channel(1174197503852290058).send(embed=embed2, view = Buy())

load_dotenv()
bot = Combo(token=os.environ["TOKEN"])