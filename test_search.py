from spiderMaterialsProject import spider as SMP
try:
    spider = SMP.spider()
    results = spider.search("H")
    for res in results:
        print(res)
finally:
    spider.quit()

