import discord
from discord.ext import commands

class RoKBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ROLE_IDS = {
            "Infantry": 1526342009596547142,
            "Cavalry": 1526341870899298426,
            "Archery": 1526342056430141440,
            "Siege": 1526342109983014942
        }

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kayit(self, ctx):
        await ctx.message.delete()
        
        # Seçim menüsü
        class RoleToggleSelect(discord.ui.Select):
            def __init__(self, role_dict):
                self.role_dict = role_dict
                options = [discord.SelectOption(label=name, value=str(rid)) for name, rid in role_dict.items()]
                super().__init__(placeholder="Birlikleri seçin...", min_values=0, max_values=len(role_dict), options=options)
            
            async def callback(self, i: discord.Interaction):
                selected_ids = [int(v) for v in self.values]
                all_role_ids = list(self.role_dict.values())
                
                # Önce tüm eski birlik rollerini al
                remove_roles = [r for r in i.user.roles if r.id in all_role_ids]
                await i.user.remove_roles(*remove_roles)
                
                # Seçilenleri ekle
                add_roles = [i.guild.get_role(rid) for rid in selected_ids if i.guild.get_role(rid)]
                if add_roles:
                    await i.user.add_roles(*add_roles)
                
                msg = f"✅ Güncellendi: {', '.join([r.name for r in add_roles]) if add_roles else 'Hiçbir birlik seçilmedi.'}"
                await i.response.send_message(msg, ephemeral=True)

        # Modal
        class NicknameModal(discord.ui.Modal, title='RoK Kayıt'):
            isim = discord.ui.TextInput(label='Oyun isminiz?', required=True)
            def __init__(self, role_dict):
                super().__init__()
                self.role_dict = role_dict
            
            async def on_submit(self, i: discord.Interaction):
                await i.user.edit(nick=str(self.isim))
                view = discord.ui.View().add_item(RoleToggleSelect(self.role_dict))
                await i.response.send_message("İsim güncellendi! Birlikleri seçin:", view=view, ephemeral=True)

        # Buton
        btn = discord.ui.Button(label="Kaydı Başlat", style=discord.ButtonStyle.primary)
        btn.callback = lambda i: i.response.send_modal(NicknameModal(self.ROLE_IDS))
        view = discord.ui.View(timeout=None).add_item(btn)
        await ctx.send("Kayıt olmak için tıklayın:", view=view)

async def setup(bot):
    await bot.add_cog(RoKBot(bot))
