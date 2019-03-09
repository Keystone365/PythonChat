
class Messagebase:

	hasError = false

	def __init__(self):
		Exception = new Exception()


class ResponseMessageBase(Messagebase):

	hasError = false

	def __init__(self):
		Exception = new Exception()

class ResquestMessageBase(Messagebase):

	hasError = false

	def __init__(self):
		Exception = new Exception()

class ValidationRequest(ResquestMessageBase):
	Email = ""