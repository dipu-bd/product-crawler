# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FormatPipeline(object):
    """
    All crawled items are passed through this pipeline
    """
    def process_item(self, item, spider):
        """
        Process an item produced by the spider
        """
        item["link"] = item["link"].strip()
        item["category"] = [x.strip() for x in item["category"]]
        item["title"] = item["title"].strip()
        item["warranty"] = (item["warranty"] or "Not Specified").strip()
        item["rating"] = to_float(item["rating"].replace(',', '.'))
        item["features"] = [to_ascii(x) for x in item["features"]]
        item["features"] = list(set(item["features"]))
        item["price"]["value"] = to_float(str(item["price"]["value"]))
        if "old_price" in item:
            item["old_price"]["value"] = to_float(str(item["old_price"]["value"]))
            item["discount_rate"] = to_int((item["discount_rate"] or "0%").strip()[:-1])
        # end if
        return item
    # end def
# end class

def to_ascii(x):
    return x.encode('ascii', 'ignore').decode('utf8').strip()
#end def

def parse(func, arg):
    """Tries to parse the value"""
    try:
        return func(arg)
    except ValueError:
        return 0
# end def

def to_float(x):
    return parse(float, (x or "0"))
# end def

def to_int(x):
    return parse(int, (x or "0"))
# end def
