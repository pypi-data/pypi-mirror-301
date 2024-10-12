from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from ..Datas.Data import CustomNamespace


async def send_query(bot_object: Namespace, data: dict = {}, method: str = '', form_data: Namespace = None) -> dict:

	url = f'https://api.telegram.org/bot{bot_object.cur_bot_token}/{method}'

	if data:
		res = await rest_side.Rest.post(url=url, json=data, form_data=form_data)
	else:
		res = await rest_side.Rest.post(url=url, form_data=form_data)
	#return await Data.wrap_dict(res.json), res.json
	print(f'RES JSON: {res.json}')
	return CustomNamespace(res.json['result']) if 'result' in res.json.keys() else res.json




async def download(url: str, path: str) -> dict:

	res = await rest_side.Rest.download(url=url, dest=path)
	return CustomNamespace({'result': res})