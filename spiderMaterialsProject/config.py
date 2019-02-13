import os
fpath = os.path.dirname(os.path.abspath(__file__))
url = {"index":"https://www.materialsproject.org/",
        "innerpage":"https://www.materialsproject.org/materials/%s",
        "ZipUrl":"https://www.materialsproject.org/materials/download/",
        "band_src":"https://www.materialsproject.org/electronic_structure/bandstructure/plot/",
        "dos_src":"https://www.materialsproject.org/electronic_structure/dos/plot/"}

savepath = {"root":"./mpdata",
            "cookies":os.path.join(fpath,"sharedCookies.json"),
            "har":os.path.join(fpath,"www.materialsproject.org.har")}

headers = {"user-agent":None,"cookie":None,"origin":None,"upgrade-insecure-requests":None,"content-type":None}
postdata = {"material_id":None,"cifType":None,"output":None}
