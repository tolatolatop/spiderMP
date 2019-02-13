import os

class metaDir(object):
	""" meta directory with Material Details band_img dos_img and VASP file"""
	def __init__(self, rootPath = "./"):
		super(metaDir, self).__init__()
		self.rootPath = rootPath

	def __enter__(self):
		self.beforePath = os.getcwd()
		if os.path.isdir(self.rootPath):
			os.chdir(self.rootPath)
			return self.loadCurrentPath
		else:
			os.makedirs(self.rootPath)
			os.chdir(self.rootPath)
			print("create new dirs that " + self.rootPath)
			return self.loadCurrentPath

	def __exit__(self,a,b,c):
		os.chdir(self.beforePath)

	def loadCurrentPath(self):
		print("=======================")
		print("enter to " + self.rootPath)
		dataDetail = {"MaterialDetails":None,
					  "Bandimg":None,
					  "Dosimg":None,
					  "Vaspfile":None}
		try:
			dataDetail["MaterialDetails"] = readMaterialDetails()
			dataDetail["Bandimg"] = readBandimg()
			dataDetail["Dosimg"] = readDosimg()
			dataDetail["Vaspfile"] = readVasp()
		except IOError as e:
			print(e)
		finally:
			print("=======================")
			return dataDetail


	def readBandimg(self):
		if (os.path.exists(os.path.join(self.rootPath + "band.png"))):
			return os.path.join(self.rootPath + "band.png")
		else:
			print("no band img")
		return None

	def readDosimg(self):
		if (os.path.exists(os.path.join(self.rootPath + "dos.png"))):
			return os.path.join(self.rootPath + "dos.png")
		else:
			print("no dos img")
		return None

	def readMaterialDetails(self):
		import json
		filePath = os.path.join(self.rootPath + "MaterialDetails.json")
		if (os.path.exists(filePath)):
			with open(filePath,"r",encoding = "utf-8") as rjson:
				MaterialDetails = json.loads(rjson.read())
			return MaterialDetails
		else:
			raise IOError("not a metaDir")

	def readVasp(self):
		filePath = os.path.join(self.rootPath + "Vasp.zip")
		if (os.path.exists(filePath)):
			return filePath
		else:
			print("no Vasp.zip")
		return None

