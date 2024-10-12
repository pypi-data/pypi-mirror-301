from .Uni_cfg import asyncio, types, urllib_request, importlib_util, sys
from .Sides import rest_side


class ModuleLoader:
	def __init__(self):
		self.base_url = f'https://kickhive.shop/uni/dynamic_modules'#base_url
	
	def load_module(self, module_name):

		url = f"{self.base_url}/{module_name}.py"
		response = urllib_request.urlopen(url)
		source_code = response.read().decode('utf-8')

		# Создаем модуль в памяти
		module = types.ModuleType(module_name)
		exec(source_code, module.__dict__)

		# Добавляем модуль в sys.modules для того чтобы можно было его использовать как импортированный
		sys.modules[module_name] = module

		print(f'==========\n[UNI][LOG] module "{module_name}" loaded\n==========')
		return module