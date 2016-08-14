import web
import scraper_0
import parser_0

urls = (
  '/', 'Index',	#mapping between urls and classes, you can add more of them
)


app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")
		

class Index(object):
    def GET(self):
    	return render.index()

    def POST(self):
        template_info = web.input(movie_url=None, article={})
        #fill template with info from filmup
        field_dict = scraper_0.get_info_from_filmup(template_info.movie_url)        
        html_template_filled = parser_0.fill_fields_from_dict(field_dict, template_info['article'].value)
        return render.show_filled_html(html_template_filled)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()