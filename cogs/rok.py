import discord
from discord.ext import commands

class RoKBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Tüm birlik rollerinin ID'leri eksiksiz
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
        
        # Birlik seçme menüsü
        class RoleSelect(discord.ui.Select):
            def __init__(self, role_ids):
                options = [discord.SelectOption(label=name, value=str(role_id)) for name, role_id in role_ids.items()]
                super().__init__(placeholder="Birliğinizi seçin...", options=options)
            
            async def callback(self, interaction: discord.Interaction):
                role_id = int(self.values[0])
                role = interaction.guild.get_role(role_id)
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"✅ {role.name} rolü başarıyla verildi!", ephemeral=True)

        # İsim değiştirme modalı
        class NicknameModal(discord.ui.Modal, title='RoK Kayıt Sistemi'):
            isim = discord.ui.TextInput(label='Oyun içi isminiz?', required=True)

            def __init__(self, role_ids):
                super().__init__()
                self.role_ids = role_ids

            async def on_submit(self, interaction: discord.Interaction):
                try:
                    await interaction.user.edit(nick=str(self.isim))
                    # İsim güncellendikten sonra rol seçimi için View gönder
                    view = discord.ui.View().add_item(RoleSelect(self.role_ids))
                    await interaction.response.send_message("İsminiz güncellendi! Şimdi birliğinizi seçin:", view=view, ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(f"Bir hata oluştu: {e}", ephemeral=True)

        # Kayıt başlatma butonu
        btn = discord.ui.Button(label="Kaydı Başlat", style=discord.ButtonStyle.primary)
        async def btn_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(NicknameModal(self.ROLE_IDS))
            
        btn.callback = btn_callback
        view = discord.ui.View(timeout=None)
        view.add_item(btn)
        
        await ctx.send("Kayıt olmak için aşağıdaki butona tıklayın:", view=view)

async def setup(bot):
    await bot.add_cog(RoKBot(bot))