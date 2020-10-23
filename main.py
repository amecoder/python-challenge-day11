import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

"""
final result @see https://royaloddballmicrocode.serranoarevalo.repl.co/
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

base_url = 'https://reddit.com'

results = []
def extract_reddit_monthly_top(subject=""):
  url = f"{base_url}/r/{subject}/top/?t=month"
  #url = f"{base_url}/{subject}"
  html = requests.get(url, headers=headers)
  
  html_soup = BeautifulSoup(html.text, "html.parser")
  posts = html_soup.find('div', {'class':'rpBJOHq2PR60pnwJlUyP0'})
  divs = posts.find_all('div')
  for div in divs:
    post = {}
    title = div.find('h3', {'class':'_eYtD2XCVieq6emjKBH3m'})    
    upvotes = div.find('div', {'class':'_1rZYMD_4xY3gRcSS3p8ODO _25IkBM0rRUqWX5ZojEMAFQ'})
    link = div.find('a', {'class':'SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE'})
    if title and upvotes and link and title :
      post['subreddit'] = subject
      post['title']  = title.text
      try:
        post['upvotes'] = int(upvotes.get_text())
      except:
        k_m = upvotes.get_text()[-1]
        number = upvotes.get_text()[0:-1]
        if k_m == 'k':
          post['upvotes'] = int(float(number)*1000)
        elif k_m == 'm':
          post['upvotes'] = int(float(number)*10000)
      post['link'] = base_url + link['href']
      post['upvotes_tag'] = upvotes.get_text()
      results.append(post)
      del post

app = Flask("DayEleven")

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/read')
def read():
  selectedSubjects = []
  for subject in subreddits:
    param_value = request.args.get(subject)
    if (param_value == 'on'):
      selectedSubjects.append(subject)
      extract_reddit_monthly_top(subject)
      
  unique_results = list({result['title']: result for result in results}.values())
  final_results = sorted(unique_results, key=lambda result: (result['upvotes']), reverse=True)
  #print(final_results)
  return render_template('read.html', readResults=final_results, selectedSubjects=selectedSubjects)  

app.run(host="0.0.0.0")