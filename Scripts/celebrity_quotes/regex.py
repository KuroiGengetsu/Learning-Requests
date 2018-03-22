"""All regexs and short functions define here"""
import re

REMOVE = lambda x, y: x.replace(y, "")                                        
QUOTES_REGEX= re.compile(r'<p>(\d+、[^<]*)</p>')                              
SPECIAL_SYMBOL_REGEX = re.compile(r'&\w+;')
TOPIC_LINK_REGEX = re.compile(r'<a title="(.*?)".*?href="(show/\w+)">')

