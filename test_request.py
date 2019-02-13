from spiderMaterialsProject import spider as SMP
from spiderMaterialsProject import dataManager 
import os
from spiderMaterialsProject import config
band_src = "https://www.materialsproject.org/electronic_structure/bandstructure/plot/mp-1027692"
dos_src = "https://www.materialsproject.org/electronic_structure/dos/plot/mp-1027692"
requests = SMP.requestsDownload()

with dataManager.metaDir(os.path.join(config.savepath["root"],"mp-1027692")) as loadFile:
	requests.getBandImage(band_src)
	requests.getDosImage(dos_src)
	requests.getVaspZip("mp-1027692")

