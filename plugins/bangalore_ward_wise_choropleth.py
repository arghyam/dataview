from models import * 
from plugins import template_plugin

class BangaloreWardWiseChoropleth(template_plugin.TemplatePlugin):

    plugin_key = "bangalore_ward_wise_choropleth.py" 
    version = 1 
    plugin_type = 1 
    description = """The choropleth map provides an easy way to visualize how a measurement varies across a geographic area or it shows the level of variability within a region. """ 
    image_url = "http://localhost:5000/static/img/bangalore-ward.jpg" 
    name = "Bangalore Ward Wise Choropleth"
    author = "Thejesh GN"
    url = "https://github.com/thejeshgn/bangalore-heatmap"

    def __init__(self):
        template_plugin.__init__(self)

    def initialize(self):
        pass

    def install():
        plugin = Plugin.query.filter_by(plugin_key=plugin_key).first()
        if plugin:
            return False
        else:
            new_plugin = Plugin(plugin_key=plugin_key,version=version,plugin_type=plugin_type,description=description,image_url=image_url,name=name,author=author,url=url,status=1,class_name=BangaloreWardWiseChoropleth.__name__)
            models.db.session.add(new_plugin)
            models.db.session.commit()
            return True

    #checks all the dependency, if no dependency then allows to uninstall    
    def uninstall():
        pass
     #checks health or upgrades
    def check():
        pass

    #match the data_table_id columns to visualize colums and generate matched_colums    
    def match():
        pass

    #Given a data_table_id , check if it satisfies all the conditions that is required for this plugin to work. 
    #If sucessful insert into visualize table for future reference. it will also store matched_colums)    
    def validate():
        pass

     #for visualize type - takes data_table_id and matched_colums dict
    def visualize():
        pass
    