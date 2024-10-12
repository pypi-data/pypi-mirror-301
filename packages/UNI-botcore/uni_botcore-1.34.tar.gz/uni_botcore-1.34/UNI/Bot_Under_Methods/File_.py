from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from .Rest_Core import send_query


class File_Methods():

	async def get_file(
		self,
		file_id: str
		):

		json_ = await Data.rebuild_json(locals())
			
		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='getFile')