from spiderMaterialsProject import spider,config,dataManager
import getopt
import sys

def printHelp():
	print('''usage: python main.py -m <module> [ -s <search query> | -g <material id> ] -i <time:microsecond>

Actions:
  -m                use module request or spider
  -s                use search functions (only for spider)
  -g                get materials detials by materials id like mp-12907

 Options:
  -i                set interval time 
  -p                set save path     default from config
''')

def main():
	shortopts = 'm:s:g:i:h'
	logopts = ["help"]
	action = None
	method = "spider"
	root_path = config.savepath["root"]
	try:
		optlist, args = getopt.getopt(sys.argv[1:], shortopts, logopts)
		for key, value in optlist:
			if key == "-g":
				action = 1
				material_id = value
			elif key == "-s":
				action = 2
				search_query = value
			elif key == "-m":
				if value in ["request","spider"]:
					method = value
				else:
					printHelp()
					sys.exit(0)
			elif key == "-p":
				root_path = value
			elif key in ("-h","--help"):
				printHelp()
				sys.exit(0)
		if len(optlist) == 0:
			printHelp()
			sys.exit(0)
	except getopt.GetoptError as e:
		print(e)
		sys.exit(2)
	with dataManager.metaDir(root_path):
		if action == 2:
			print(search_query)
			browser = spider.spider()
			for inform in browser.search(search_query):
				print(inform)
		elif action == 1:
			print(material_id)
			with dataManager.metaDir(material_id) as loadData:
				if method == "request":
					browser = spider.requestsDownload()
					browser.getBandImage(config.url["band_src"] % material_id)
					browser.getDosImage(config.url["dos_src"] % material_id)
					browser.getVaspZip(material_id)
				elif method == "spider":
					browser = spider.spider()
					browser.innerPage(material_id)



if __name__ == "__main__":
	main()
