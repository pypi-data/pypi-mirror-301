from ..Uni_cfg import aiohttp, asyncio, Namespace


# Respone DataType
class Response(Namespace):
	async def update(self):
		
		path = getattr(Rest, self.type)
		return await path(url=self.url, headers=self.headers, data=self.data, json=self.json_data)


# Rest requests
class Rest():

	async def __init__(self, response, text, json):
		self.response = response
		self.text = text
		self.json = json


	async def get(url: str, headers: dict = None, data: dict = None, json: dict = None):

		response_status = None
		response_text = None
		response_json = None

		async with aiohttp.ClientSession(headers=headers) as session:
			response = await session.get(url=url, json=json, data=data)

			response_status = response.status

			try:
				response_text = await response.text(encoding='UTF-8')
				response_json = await response.json()
			except Exception as e:
				#traceback.print_exc()
				pass

		return Response(type='get', url=url, headers=headers, json_data=json, data=data, status=response_status, text=response_text, json=response_json)


	async def post(url: str, headers: dict = None, data: dict = None, json: dict = None, form_data: Namespace = None):

		response_status = None
		response_text = None
		response_json = None

		async with aiohttp.ClientSession(headers=headers) as session:

			if form_data != None:
				response = await session.post(url=url, data=form_data)
			else:
				response = await session.post(url=url, json=json, data=data)

			response_status = response.status

			try:
				response_text = await response.text(encoding='UTF-8')
				response_json = await response.json()
			except Exception as e:
				#traceback.print_exc()
				pass

		return Response(type='post', url=url, headers=headers, json_data=json, data=data, status=response_status, text=response_text, json=response_json)


	async def download(url, dest):
	    async with aiohttp.ClientSession() as session:
	        async with session.get(url) as response:
	            if response.status == 200:
	                with open(dest, 'wb') as f:
	                    while True:
	                        chunk = await response.content.read(1024)
	                        if not chunk:
	                            break
	                        f.write(chunk)
	                print(f"File downloaded: {dest}")
	                return True
	            else:
	                print(f"Failed to download file. Status code: {response.status}")
	                return False