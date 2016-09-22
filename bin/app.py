import web
from web import form
import scraper_0
import parser_0

urls = (
  '/', 'Index',	#mapping between urls and classes, you can add more of them
  '/fill_form', 'Filling'
)


app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")
		
def form_autogen(field_list):
	autogen = DynamicForm()
	for i in field_list:
		autogen.add_input(form.Textbox(i))
	return autogen

class DynamicForm(web.form.Form):

    def add_input(self, new_input):
        self.inputs += (new_input, )


class Index(object):
    def GET(self):
    	return render.index()

    def POST(self):
        template_info = web.input(movie_url=None, article={}, news={})
        #retrieve info from filmup
        if template_info.movie_url != "":
            field_dict = scraper_0.get_info_from_filmup(template_info.movie_url)      
        else:
            field_dict = {"null" : "null"}  
        #fill templates
        html_template_filled_article = parser_0.fill_fields_from_dict(field_dict, template_info['article'].value)
        html_template_filled_news = parser_0.fill_fields_from_dict(field_dict, template_info['news'].value)
        #get missing fields
        field_list = parser_0.get_field_list(html_template_filled_article)
        field_list += parser_0.get_field_list(html_template_filled_news)
        field_list = list(set(field_list))
        myform = form_autogen(field_list)
        f = myform()
        return render.show_filled_html(html_template_filled_article, html_template_filled_news,f)
        
class Filling(object):
	def GET(self):
		return 'Get'

	def POST(self):
		values = web.input()
		html_template_article = values['partial_fill_article']
		html_template_news = values['partial_fill_news']
		html_template_filled_article = parser_0.fill_fields_from_dict(values, html_template_article)
		html_template_filled_news = parser_0.fill_fields_from_dict(values, html_template_news)
		f = form.Form()
		return render.show_filled_html(html_template_filled_article, html_template_filled_news, f)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()