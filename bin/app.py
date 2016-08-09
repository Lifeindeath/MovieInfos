import web
import scraper_0

urls = (
  '/hello', 'Index'	#mapping between urls and classes, you can add more of them
)


app = web.application(urls, globals())

render = web.template.render('templates/', base="layout")

class Index(object):
    def GET(self):
    	return render.url_form()

    def POST(self):
        form = web.input(movie_url=None)
        #greeting =  "%s, %s" % (form.greet, form.name)
        field_dict = scraper_0.get_info_from_filmup(form.movie_url)
        print field_dict
        return render.index(title = field_dict.get('Titolo originale:'), \
        					genre = field_dict.get('Genere:'), \
        					year = field_dict.get('Anno:'),    \
        					cast = field_dict.get('Cast:'))

if __name__ == "__main__":
    app.run()