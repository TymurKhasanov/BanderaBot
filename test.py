from pprint import pprint

from app.services.wiki_skills import get_skills

skills = get_skills("2-gladiator")

pprint(skills["Physical"][0])