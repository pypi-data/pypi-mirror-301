import discord, vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

class WebhookSender:
    """Данный класс предназначен для работы с Discord { WebHook's }..."""
    def __init__(self, url: str):
        self.webhook = discord.SyncWebhook.from_url(url)
    def send(self, message: str):
        """Данная функция может послужить вам для отправки текстовых сообщений!"""
        self.webhook.send(message)
    def send_embed(self, embed: discord.Embed):
        """Вы используете эту функцию для отправок эмбедов."""
        self.webhook.send(embed=embed)
    def file_send(self, directory: str):
        """Эта функция служит для отправки файла!"""
        self.webhook.send(file=discord.File(open(directory, 'rb')))
class VK:
    """Ну, а этот класс предназначен для работы с Vk_Api"""
    def __init__(self, token: str, id: int):
        self.vk = vk_api.VkApi(token=token)
        self.id = id
    def inspect_messages(self):
        """С помощью данной функции вы сможете на регулярной основе отслеживать приходящие сообщения в вашем сообществе VKонтакте..."""
        for event in VkLongPoll(self.vk).listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me == True:
                    print('Молодой человек, вам написал какой-то пользователь в личных сообщениях вашего сообщества во VK!')
                    
