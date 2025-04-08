from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def filtering(media_name):
    element_name = ""
    class_name = ""

    if media_name == "kompas":
        element_name = "h1"
        class_name = "hlTitle"
    elif media_name == "tribun":
        element_name = "div"
        class_name = "hltitle"
    elif media_name == "detik":
        element_name = "h2"
        class_name = "media__title"
    elif media_name == "cnn":
        element_name = "h1"
        class_name = "text-2xl inline group-hover:text-cnn_red"
    elif media_name == "tempo":
        element_name = "p"
        class_name = "text-[26px] lg:text-[32px] leading-[122%] font-bold"

    return [element_name, class_name]

def scrape_blog_titles(media_name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    filter = filtering(media_name)
    element_name, class_name = filter[0], filter[1]

    titles = soup.find(element_name, class_=class_name)

    return titles.text if titles else "No title found"

@app.route('/', methods=['GET', 'POST'])
def index():
    titles = []
    data = None  # Initialize data to avoid NameError
    media_name = None  # Initialize media_name to avoid NameError
    url = None  # Initialize url to avoid NameError

    if request.method == 'POST':
        media_name = request.form.get('media_name')
        try:
            if media_name == 'kompas':
                url = 'https://www.kompas.com/'
            elif media_name == 'tribun':
                url = 'https://www.tribunnews.com/'
            elif media_name == 'detik':
                url = 'https://www.detik.com/'
            elif media_name == 'cnn':
                url = 'https://www.cnnindonesia.com/'
            elif media_name == 'tempo':
                url = 'https://www.tempo.co/'
            else:
                url = None

            if url:
                titles = scrape_blog_titles(media_name, url)
            else:
                titles = "Invalid media name"
        finally:
            data = titles

    return render_template('index.html', data=data, media_name=media_name, url=url)

if __name__ == '__main__':
    app.run(debug=True)
