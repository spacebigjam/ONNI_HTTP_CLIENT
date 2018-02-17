import sys
import logging
import urllib.error
import gzip


from urllib.request import Request
from urllib.request import urlopen

class HttpMngmt:

	def __init__(self, end_point):
		self.request = Request(end_point)

	def run_request(self):

		response = self._get_response()

		if response != None:
			self.status = response.status
			self.headers = response.getheaders()
			if(response.getheader("Content-Encoding") == "gzip"):
				self.content = gzip.decompress(response.read())
			else:
				self.content = response.read()
		else:
			self.status = None
			self.headers = None 
			self.content = None

	def _get_response(self):
		try:
			response = urlopen(self.request)
		except urllib.error.HTTPError as http_err:
			logging.error("HTTP Error       ["+str(http_err.code)+"]")
			logging.error("HTTP Description ["+str(http_err.reason)+"]")
			logging.debug("HTTP status ["+str(response.status)+"]")
			response = None
		except urllib.error.URLError as url_err:
			logging.error(str(url_err.reason))
			response = None

		return response


if __name__ == "__main__":
	http_obj = HttpMngmt("http://debian")
	http_obj.run_request()

	if http_obj.content != None:
		print (http_obj.content)
