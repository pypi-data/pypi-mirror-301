class Template:
	def __init__(self,name:str) -> None:
		self.__name:str = name

		self.__html_file:str
		self.__css_file:str
		self.__js_pre_file:str
		self.__js_aft_file:str
	
	@property
	def Name(self) -> str:
		return self.__name
	@Name.setter
	def Name(self,new_value:str) -> None:
		self.__name = new_value

	@property
	def HTML_File(self) -> str:
		return self.__html_file
	@HTML_File.setter
	def HTML_File(self,new_value:str) -> None:
		self.__html_file = new_value

	@property
	def CSS_File(self) -> str:
		return self.__css_file
	@CSS_File.setter
	def CSS_File(self,new_value:str) -> None:
		self.__css_file = new_value
	
	@property
	def JS_PreRender_File(self) -> str:
		return self.__js_pre_file
	@JS_PreRender_File.setter
	def JS_PreRender_File(self,new_value:str) -> None:
		self.__js_pre_file = new_value
	
	@property
	def JS_After_File(self) -> str:
		return self.__js_aft_file
	@JS_After_File.setter
	def JS_After_File(self,new_value:str) -> None:
		self.__js_aft_file = new_value
