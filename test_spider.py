from spiderMaterialsProject import spider as SMP

try:
    spider = SMP.spider() # open spider
    spider.innerPage("mp-1027692") # catch Data but no save
finally:
    spider.quit()
