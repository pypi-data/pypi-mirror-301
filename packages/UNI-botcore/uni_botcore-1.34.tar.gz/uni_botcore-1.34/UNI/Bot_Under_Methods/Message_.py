from ..Uni_cfg import asyncio, Namespace, aiohttp
from ..Sides import rest_side
from ..Datas import Data
from .Rest_Core import send_query

from ..Types.Keyboards_ import InlineKeyboardMarkup
from ..Types.Reply_ import ReplyParameters
from ..Types.Entities_ import LinkPreviewOptions



class Message_Methods():

	async def send_message(
		self,
		chat_id: int,
		text: str,
		business_connection_id: str = '',
		message_thread_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: LinkPreviewOptions = LinkPreviewOptions().json_obj,
		disable_notification: bool = False,
		protect_content: bool = False,
		message_effect_id: str = '',
		reply_parameters: ReplyParameters = {},
		reply_markup: InlineKeyboardMarkup = {}
		):

		json_ = await Data.rebuild_json(locals())

		if reply_markup != {}:
			json_['reply_markup'] = reply_markup.raw_keyboard
			
		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='sendMessage')


	async def delete_message(
		self,
		chat_id: int,
		message_id: int
		):

		json_ = await Data.rebuild_json(locals())

		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='deleteMessage')


	async def edit_message_text(
		self,
		text: str,
		chat_id: int,
		message_id: int,
		business_connection_id: str = '',
		inline_message_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: dict = {},
		reply_markup: InlineKeyboardMarkup = {}
		):


		json_ = await Data.rebuild_json(locals())

		if reply_markup != {}:
			json_['reply_markup'] = reply_markup.raw_keyboard

		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='editMessageText')


	async def forward_message(
		self,
		chat_id: int,
		message_id: int,
		from_chat_id: int,
		message_thread_id: int = 0,
		disable_notification: bool = False,
		protect_content: bool = None,
		):

		json_ = await Data.rebuild_json(locals())
		#print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='forwardMessage')


	async def set_message_reaction(
		self,
		chat_id: int,
		message_id: int,
		reaction: list,
		is_big: bool = False,
	):

		json_ = await Data.rebuild_json(locals())
		#print(f'BUILD MESSAGE: {json_}')

		json_['reaction'] = [{"type": "emoji", "emoji": i} for i in reaction]

		return await send_query(bot_object=self, data=json_, method='setMessageReaction')


	async def send_photo(
		self,
		chat_id: int,
		photo: str = None,
		business_connection_id: str = '',
		message_thread_id: int = 0,
		caption: str = '',
		parse_mode: str = 'HTML',
		caption_entities: dict = {},
		show_caption_above_media: bool = False,
		has_spoiler: bool = False,
		disable_notification: bool = False,
		protect_content: bool = False,
		message_effect_id: str = '',
		reply_parameters: ReplyParameters = {},
		reply_markup: InlineKeyboardMarkup = {}
		):

		json_ = await Data.rebuild_json(locals())
		form_ = False

		#del json_[files]

		if reply_markup != {}:
			json_['reply_markup'] = reply_markup.raw_keyboard


		if not isinstance(photo, str):
			form_ = True

			old_json = json_
			json_ = aiohttp.FormData()

			for key, value in old_json.items():

				if key != 'photo':
					json_.add_field(key, str(value) if isinstance(value, int) else value)
				else:
					json_.add_field('photo', photo, filename='receipt.png', content_type='image/png')  # Добавляем изображение


		print(f'BUILD MESSAGE: {json_}')

		if not form_:
			return await send_query(bot_object=self, data=json_, method='sendPhoto', form_data=files_)
		else:
			return await send_query(bot_object=self, method='sendPhoto', form_data=json_)