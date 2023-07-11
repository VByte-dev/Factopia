from flask import Flask, render_template, request
import requests

app = Flask(__name__)

#-----------------------------------------------------------------------------------------#

def get_wikipedia_acontenrticle(article_title):
    # Define the base URL for the Wikipedia API
    base_url = "https://en.wikipedia.org/w/api.php"

    # Define the parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
        "titles": article_title
    }

    try:
        # Send a GET request to the Wikipedia API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for any request errors

        data = response.json()

        # Check if the API response contains an error
        if 'error' in data:
            error_message = data['error']['info']
            raise Exception(f"Wikipedia API error: {error_message}")

        # Extract the page content from the API response
        page_id = next(iter(data['query']['pages']))  # Get the first page ID
        page_content = data['query']['pages'][page_id]['extract']

        return page_content

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the Wikipedia API: {e}")
        return None
    except Exception as e:
        print(f"Error retrieving Wikipedia content: {e}")
        return None

def suggest_related_articles(query):
    # Define the base URL for the Wikipedia API
    base_url = "https://en.wikipedia.org/w/api.php"

    # Define the parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srprop": "title",
        "srlimit": 5  # Limit the number of suggested articles
    }

    try:
        # Send a GET request to the Wikipedia API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for any request errors

        data = response.json()

        # Extract the suggested article titles from the API response
        suggested_articles = [result["title"] for result in data["query"]["search"]]

        return suggested_articles

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the Wikipedia API: {e}")
        return []
    except Exception as e:
        print(f"Error retrieving suggested articles: {e}")
        return []


#-----------------------------------------------------------------------------------------#

@app.route('/', methods = ['GET'])
def homePage():
    try:
        query = request.args.get('query')
        if query == '':
            c = ''' '''
            r = suggest_related_articles(query)

        else:
            c =  get_wikipedia_acontenrticle(query)
            r = suggest_related_articles(query)
        print(c)
        
    except:
        c = 'Oops! Something Went Wrong'
    
    return render_template('mainPage.html', content = c, related = r, query = f'{query}:', we = '''Factopia, a comprehensive online resource where you can uncover a world of fascinating facts and explore a wide range of informative articles. As you step into Factopia, prepare to embark on a journey of discovery and immerse yourself in a wealth of knowledge. Our site harnesses the power of the Wikipedia API, connecting you to a vast collection of articles and information covering diverse topics. Whether you're seeking answers to burning questions, conducting research, or simply indulging your curiosity, Factopia is your go-to destination. With our user-friendly interface and carefully curated content, we strive to make learning engaging, enjoyable, and accessible to all. Join us at Factopia and unlock a world of enlightenment.''')
    print(suggest_related_articles('query'))

#-----------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')