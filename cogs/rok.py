import discord
from discord.ext import commands

class RoKBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Birlik rol ID'lerin
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
        
        class RoleToggleSelect(discord.ui.Select):
            def __init__(self, role_ids):
                options = [discord.SelectOption(label=name, value=str(rid)) for name, rid in role_ids.items()]
                # min_values=0 ve max_values=len ile çoklu seçime izin veriyoruz
                super().__init__(placeholder="Birliklerinizi seçin/kaldırın...", 
                                 min_values=0, max_values=len(role_ids), options=options)
            
            async def callback(self, i: discord.Interaction):
                selected_role_ids = [int(v) for v in self.values]
                all_role_ids = list(self.role_ids.values())
                
                # Kullanıcının mevcut rollerini temizle (sadece bizim birlik rollerinden)
                roles_to_remove = [r for r in i.user.roles if r.id in all_role_ids]
                await i.user.remove_roles(*roles_to_remove)
                
                # Seçilenleri ekle
                roles_to_add = [i.guild.get_role(rid) for rid in selected_role_ids if i.guild.get_role(rid)]
                if roles_to_add:
                    await i.user.add_roles(*roles_to_add)
                
                msg = f"✅ Güncellendi: {', '.join([r.name for r in roles_to_add]) if roles_to_add else 'Hiçbir birlik seçilmedi.'}"
                await i.response.send_message(msg, ephemeral=True)

        class NicknameModal(discord.ui.Modal, title='RoK Kayıt'):
            isim = discord.ui.TextInput(label='Oyun isminiz?', required=True)
            def __init__(self, role_ids): super().__init__(); self.role_ids = role_ids
            async def on_submit(self, i: discord.Interaction):
                await i.user.edit(nick=str(self.isim))
                view = discord.ui.View().add_item(RoleToggleSelect(self.role_ids))
                await i.response.send_message("İsim güncellendi! Birlikleri seçin/kaldırın:", view=view, ephemeral=True)

        btn = discord.ui.Button(label="Kaydı Başlat", style=discord.ButtonStyle.primary)
        btn.callback = lambda i: i.response.send_modal(NicknameModal(self.ROLE_IDS))
        view = discord.ui.View(timeout=None).add_item(btn)
        await ctx.send("Kayıt için tıklayın:", view=view)

async def setup(bot):
    await bot.add_cog(RoKBot(bot))
