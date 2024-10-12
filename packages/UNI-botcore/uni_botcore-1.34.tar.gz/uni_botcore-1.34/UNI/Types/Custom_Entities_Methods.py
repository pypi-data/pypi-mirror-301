from ..Uni_cfg import asyncio, Namespace, Bot_Object
from ..Datas import Data
from ..Types.Keyboards_ import InlineKeyboardMarkup
from ..Bot_Under_Methods.Rest_Core import download


class Chat_Methods():

	async def send_message(
		self,
		text: str,
		business_connection_id: str = '',
		message_thread_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: dict = {},
		disable_notification: bool = False,
		protect_content: bool = False,
		message_effect_id: str = '',
		reply_parameters: dict = {},
		reply_markup: InlineKeyboardMarkup = {}
	):

		return await self.bot_object.send_message(
			chat_id=self.id,
			text=text,
			business_connection_id=business_connection_id,
			message_thread_id=message_thread_id,
			parse_mode=parse_mode,
			entities=entities,
			link_preview_options=link_preview_options,
			disable_notification=disable_notification,
			protect_content=protect_content,
			message_effect_id=message_effect_id,
			reply_parameters=reply_parameters,
			reply_markup=reply_markup
		)


class Photo_Methods():

	async def download(
		self,
		path: str,
		size: str = 'large' #['min', 'small', 'medium', 'large']
	):

		photo_size_index = getattr(self, size)
		file_data = await self.bot_object.get_file(file_id=photo_size_index['file_id'])
		download_url = f'https://api.telegram.org/file/bot{self.bot_object.cur_bot_token}/{file_data.file_path}'

		return await download(url=download_url, path=path)