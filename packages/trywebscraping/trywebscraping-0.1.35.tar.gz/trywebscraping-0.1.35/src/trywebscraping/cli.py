import os
import click

@click.group()
def cli():
    """TryWebScraping CLI"""
    pass

@cli.command()
def help():
    """Display help message"""
    commands = {
        "init": "Initialize a new scraping project",
        "help": "Display this help message"
    }
    click.echo("TryWebScraping CLI Help:")
    for cmd, desc in commands.items():
        click.echo(f"  {cmd:<4} - {desc}")

@cli.command()
@click.argument('project_name', required=False)
@click.option('--example', type=click.Choice(['amazon', 'news', 'custom']), help='Choose an example template')
def init(project_name, example):
    """Initialize a new scraping project"""
    if not project_name:
        project_name = click.prompt("Enter project name (use '.' for current directory)", default=".", show_default=True)
    
    if project_name == ".":
        click.echo("Using current directory for the project.")
    else:
        os.makedirs(project_name, exist_ok=True)
    
    # Create app.py file
    app_path = os.path.join(project_name, "app.py")
    
    examples = {
        'amazon': """from trywebscraping import Fetch

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
""",
        'news': """from trywebscraping import Fetch

hn = Fetch("https://news.ycombinator.com/")
articles = hn.query("tr.athing", key="articles").extract({
    "rank": "td span.rank",
    "title": "td.title a",
    "link": "td.title a@href"
}).query("tr.athing + tr", key="articles").extract({
    "score": "span.score",
    "user": "a.hnuser",
})
print(articles)
""",
        'custom': """from trywebscraping import Fetch

# Here's a quick template to get you started.
example = Fetch("https://example.com")
content = example.query("div").extract({
    "title": "h1",
    "link": "p a@href",
    "link_text": "p a"
})
print(content)
"""
    }
    
    if not example:
        example = click.prompt(
            "Choose an example template",
            type=click.Choice(list(examples.keys())),
            default="custom"
        )
    
    with open(app_path, "w") as f:
        f.write(examples[example])
    
    click.echo(f"Initialized new scraping project: {project_name}")
    click.echo(f"Created {app_path} with {example} example")

def main():
    cli()

if __name__ == "__main__": 
    main()