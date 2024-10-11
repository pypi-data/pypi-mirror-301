import random
from typing import List, Dict
from bs4 import BeautifulSoup, NavigableString
import json
import time

def get_random_user_agent() -> str:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    ]
    return random.choice(user_agents)

def convert_html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    markdown = []

    for element in soup.find_all():
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            markdown.append(f"{'#' * int(element.name[1])} {element.get_text().strip()}\n")
        elif element.name == 'p':
            markdown.append(f"{element.get_text().strip()}\n\n")
        elif element.name == 'a':
            markdown.append(f"[{element.get_text().strip()}]({element.get('href', '')})")
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li', recursive=False):
                prefix = '* ' if element.name == 'ul' else f"{li.find_previous_siblings('li').__len__() + 1}. "
                markdown.append(f"{prefix}{li.get_text().strip()}\n")
            markdown.append('\n')
        elif element.name == 'img':
            markdown.append(f"![{element.get('alt', 'Image')}]({element.get('src', '')})\n")
        elif element.name == 'div':
            text = element.get_text().strip()
            if text:
                markdown.append(f"{text}\n\n")

    return ''.join(markdown)

def get_metadata(html: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, 'lxml')
    metadata = {}
    
    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.string.strip()
    
    # Extract meta tags
    for meta in soup.find_all('meta'):
        name = meta.get('name', '').lower()
        property = meta.get('property', '').lower()
        content = meta.get('content', '')
        
        if name:
            metadata[name] = content
        elif property:
            metadata[property] = content
    
    # Extract Open Graph tags
    for og in soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')}):
        metadata[og['property']] = og.get('content', '')
    
    # Extract Twitter Card tags
    for twitter in soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')}):
        metadata[twitter['name']] = twitter.get('content', '')
    
    # Extract canonical URL
    canonical = soup.find('link', rel='canonical')
    if canonical:
        metadata['canonical_url'] = canonical['href']
    
    # Extract favicon
    favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
    if favicon:
        metadata['favicon'] = favicon['href']
    
    return metadata

def get_clean_html(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    
    # Remove unwanted elements
    for element in soup(['script', 'style', 'meta', 'link', 'noscript']):
        element.decompose()
    
    # Remove all attributes from remaining tags
    for tag in soup.find_all(True):
        tag.attrs = {}
    
    # Get the cleaned HTML as a string
    clean_html = str(soup.body) if soup.body else str(soup)
    
    return clean_html

def html_to_json(html: str, include_unique_selectors: bool = False) -> Dict:
    soup = BeautifulSoup(html, 'lxml')
    
    # Remove elements that can't be scraped
    for element in soup(['script', 'style', 'head', 'meta', 'link', 'noscript', 'title', 'iframe']):
        element.decompose()
    
    def element_to_dict(element, include_selector=False):
        result = {}
        if element.name:
            result['tag'] = element.name
            
            if element.attrs:
                result['attributes'] = element.attrs
            
            if include_selector:
                result['unique_selector'] = get_unique_selector(element)
            
            if element.string and element.string.strip():
                result['text'] = element.string.strip()
            elif element.contents:
                result['children'] = [element_to_dict(child, include_selector) for child in element.contents if child.name is not None]
            
            return result
        elif isinstance(element, NavigableString) and element.strip():
            return element.strip()
    
    json_data = element_to_dict(soup.body, include_unique_selectors)
    json_data['timestamp'] = int(time.time())
    
    return json_data

def get_unique_selector(element) -> str:
    if element.get('id'):
        return f'#{element["id"]}'
    
    if element.get('class'):
        classes = '.'.join(element['class'])
        return f'{element.name}.{classes}'
    
    siblings = element.find_previous_siblings(element.name)
    index = len(siblings) + 1
    return f'{element.name}:nth-of-type({index})'

def most_similar_algorithm(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    ignore_elements = {'link', 'noscript', 'head', 'title', 'html', 'body', 'footer', 'header', 'nav'}
    
    for elem in soup(['script', 'style', 'iframe', 'br', 'hr', 'input', 'button', 'meta']):
        elem.decompose()
    
    def score_element(elem):
        score = 0
        
        # Prefer elements with more children (but not too many)
        child_count = len(elem.find_all())
        score += min(child_count, 20) * 2
        
        # Prefer elements closer to the body
        score -= len(list(elem.parents)) * 2
        
        # Strongly prefer elements with product-related class names or IDs
        class_str = ' '.join(elem.get('class', []))
        id_str = elem.get('id', '')
        if any(keyword in (class_str + ' ' + id_str).lower() for keyword in ['product', 'item', 'result', 'listing']):
            score += 100
        
        # Prefer elements with price-like content
        if any(char.isdigit() for char in elem.text):
            score += 50 
        
        # Prefer elements with image children
        score += len(elem.find_all('img')) * 10
        
        # Prefer elements with a grid-like structure
        if 'grid' in class_str or 'flex' in class_str:
            score += 30
        
        return score

    elements = soup.find_all(lambda tag: tag.name not in ignore_elements and not tag.has_attr('hidden'))
    scored_elements = [(elem, score_element(elem)) for elem in elements]
    sorted_elements = sorted(scored_elements, key=lambda x: x[1], reverse=True)

    if sorted_elements:
        best_element = sorted_elements[0][0]
        return convert_html_to_markdown(str(best_element))
    else:
        return convert_html_to_markdown(str(soup))