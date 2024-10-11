<img src="https://www.trywebscraping.com/_next/image?url=%2Fassets%2Flogo.png&w=128&q=75" alt="Try Web Scraping Logo">

# Try Web Scraping

To get started, run: `pip install trywebscraping`

Here's some example code to help you begin:

```python
from trywebscraping import Fetch

hn = Fetch("https://news.ycombinator.com")
articles = hn.query("tr.athing").extract({
    "rank": "span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
}).limit(10)
print(articles)
```

Or for a more complex example:

```python
from trywebscraping import Fetch

amazon = Fetch("https://www.amazon.com/s?k=cracking+the+coding+interview")
product_listings = amazon.query("div.s-card-container").extract({
    "title": "h2 a span.a-text-normal",
    "price": "span.a-price-whole",
    "rating": "span.a-icon-alt",
    "num_reviews": "a-size-base",
    "product_link": "h2 a.a-link-normal@href",
    "product_image": "img.s-image@src"
})

print(product_listings)
```

If you're interested in this project, please connect with me:

- Schedule a call: https://cal.com/lukelucas/30min
- Email: luke.lucas@trywebscraping.com

For issues, feedback, or general discussion about the library, you can use our GitHub repository: https://github.com/webscrape/trywebscraping-python

I appreciate any communications, regardless of how you choose to reach out!
