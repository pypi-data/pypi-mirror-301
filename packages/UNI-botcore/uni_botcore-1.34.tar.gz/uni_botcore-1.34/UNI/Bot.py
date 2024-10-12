from .Uni_cfg import asyncio, Namespace, traceback, time, json, v_, time, os, UNI_Handlers, Observer, FileSystemEventHandler, importlib

from .Converters import primary_converter
from .Datas.Data import wrap_namespace

from .Bot_Under_Methods.Main_ import Main_Methods
from .Bot_Under_Methods.Message_ import Message_Methods
from .Bot_Under_Methods.Callback_ import Callback_Methods
from .Bot_Under_Methods.Inline_ import Inline_Methods
from .Bot_Under_Methods.Chat_ import Chat_Methods
from .Bot_Under_Methods.File_ import File_Methods

from .Sides import rest_side, ssh_side



class AsyncHandlerReloader(FileSystemEventHandler):
	def __init__(self, module, loop_, debounce_delay=1.0):
		self.module = module
		self.loop_ = loop_
		self.debounce_delay = debounce_delay
		self.last_modified = 0

	def on_modified(self, event):
		if event.src_path.endswith('.py'):
			current_time = time.time()
			if current_time - self.last_modified >= self.debounce_delay:
				self.last_modified = current_time
				#print(f"Изменен файл: {event.src_path}")

				# Выделяем тип хэндлера из имени файла
				handler_type = str(os.path.basename(event.src_path)).split('_handler.py')[0]
				#print(f'***{handler_type}***')

				# Запускаем асинхронную задачу перезагрузки хэндлеров
				asyncio.run_coroutine_threadsafe(self.reload_handlers(handler_type), self.loop_)


	async def reload_handlers(self, handler_type):
		await asyncio.sleep(0)  # Чтобы это был async метод
		
		# Перезагрузка модуля с хэндлерами
		handler_module = getattr(self.module, f'{handler_type}_handler', None)
		if handler_module:

			old_handlers = UNI_Handlers[handler_type]
			UNI_Handlers[handler_type] = []  # Очищаем хэндлеры


			importlib.reload(self.module)
			importlib.reload(handler_module)
			#print(f"Хэндлер {handler_type} перезагружен")

			# Перезагружаем хэндлеры в основной системе

			for i in old_handlers:
				commands = i.get('commands', [])
				chat_types = i.get('chat_types', [])
				func = i.get('func', None)

				if func:
					# Применяем декоратор
					decorated_func = uni_handler(**i['locals_'])(func)
					UNI_Handlers[handler_type].append({
						'func': decorated_func,
						'locals_': i['locals_']
					})

					print(f'[UNI][LOG] handler {handler_type} update and reloaded')



class Dispatcher(
	Message_Methods,
	Callback_Methods,
	Inline_Methods,
	Chat_Methods,
	File_Methods
	):

	def __init__(self, 
		bot_token: str,
		BAG: Namespace = None,
		test_bot_token: str = '', 
		testbot: bool = False, 
		allowed_updates: list = [
			"message", 
			"inline_query", 
			"callback_query",
			"chat_member",
			'message_reaction',
			'chat_join_request',
			'business_message',
			'business_connection',
			'edited_business_message',
			'deleted_business_messages'
		],
		tasks: list = []
		):

		self.bot_token = bot_token
		self.test_bot_token = test_bot_token
		self.testbot = testbot
		self.cur_bot_token = bot_token if testbot == False else test_bot_token

		self.allowed_updates = allowed_updates
		self.tasks = tasks


	def run(self):

		print(time.time())
		asyncio.run(self.pooling())


	async def watch_dog(self):

		loop_ = asyncio.get_running_loop()

		# Определяем путь к папке, где находятся ваши хэндлеры динамически
		handlers_dir = None

		for i in self.BAG.handlers:
			#handlers_dir = os.path.dirname(self.BAG.handlers_path.__file__)
			handlers_dir = os.path.dirname(i.__file__)
			#print(f'HDIR: {handlers_dir}')
			break

		# Настраиваем наблюдателя
		event_handler = AsyncHandlerReloader(self.BAG.handlers_path, loop_=loop_)
		observer = Observer()
		observer.schedule(event_handler, path=handlers_dir, recursive=True)

		# Запускаем наблюдение
		observer.start()

		try:
			while True:
				await asyncio.sleep(1)
		except KeyboardInterrupt:
			observer.stop()

		observer.join()



	async def pooling(self):

		#print(f'BAG: {self.BAG}')

		for task_ in self.tasks:
			asyncio.create_task(task_)

		asyncio.create_task(self.autoupdate())
		if hasattr(self.BAG, 'watch_dog'):
			if self.BAG.watch_dog == True:
				asyncio.create_task(self.watch_dog())


		offset = 1
		last_update_id = 0
		while True:
			try:

				updates_ = await Main_Methods.get_updates(
					bot_object= self, 
					offset=offset, 
					allowed_updates=self.allowed_updates
				)
				updates = updates_.result
				json_updates_ = await updates_.to_dict()
				json_updates = json_updates_['result']

				#print(updates)#дописать

				if len(updates) > 0:

					cur_update = updates[0]
					cur_json_update = json_updates[0]
					

					if cur_update.update_id != last_update_id:

						last_update_id = cur_update.update_id
						print(cur_update)
						#logging.debug(updates)
						print(json.dumps(cur_json_update, indent=4))

						result = await primary_converter.process_update(update=cur_update, bot_object=self)
						offset=cur_update.update_id+1

				await asyncio.sleep(.1)
				#print('---')

			except Exception as e:
				try:
					traceback.print_exc()

				except Exception as e:
					pass
				#traceback.print_exc()
				continue


	async def autoupdate(self):

		while True:
			try:
				print(f'ЧЕКАЕМ ОБНОВУ ПАКЕТА')
				last_version = await self.get_last_version()
				print(f'CUR V: {v_} | LAST V: {last_version}')

				if v_ != last_version:
					print(f'версии разные')

					await ssh_side.send_ssh_query(hostname=self.BAG.hostserver.name, username=self.BAG.hostserver.username, password=self.BAG.hostserver.password, command=f'pip install UNI-botcore=={last_version}')
					await asyncio.sleep(1)
					await ssh_side.send_ssh_query(hostname=self.BAG.hostserver.name, username=self.BAG.hostserver.username, password=self.BAG.hostserver.password, command=f'pip install UNI-botcore=={last_version}')
					await Message_Methods.send_message(self=self, chat_id=1939628022, text=f'Ядро обновлено до версии {last_version}')
					os.system(f'pm2 restart {self.BAG.bot_name}')
					

				await asyncio.sleep(120)
			except Exception as e:
				traceback.print_exc()
				pass


	async def get_last_version(self):

		last_v_query = await Main_Methods.get_last_uni_version()
		last_v = last_v_query.info.version
		return last_v