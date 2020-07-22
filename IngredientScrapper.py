from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import re


def keyingredient_div():
    if len(driver.find_elements_by_class_name('keyword_tag')) == 0:
        return False
    return True


options = Options()
options.Headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(
    options=options, executable_path="/Users/bluetomato/Projects/experiments/chromedriver")

# new file (ingredient scrapper)
df = pd.read_csv('StructuredRecipes.csv')

dictionary = {}
i = 0
keyingredient = []
for a in df["Links"]:
    try:
        driver.get(a)
        content = driver.page_source
        Soup = BeautifulSoup(content, features="html.parser")

        # fetching recipe names
        dictionary["RecipeName"] = df["RecipeName"][i]

        # fetching links
        dictionary["Links"] = df["Links"][i]

        # fetching ingredients with quantities
#         ingredient_div=Soup.find('div',attrs={'class':'ingredients'})
#         name=ingredient_div.find('ul')
#         for a in name.findAll('li'):
#             list_element=a.text
#             sub_ingredient.append(list_element)
#         ingredients.append(sub_ingredient)

        # fetching keyingredients
        if keyingredient_div():
            x = Soup.find('div', attrs={'class': 'keyword_tag'})
            if type(x.text) == str:
                word = re.sub('Key Ingredients: ', '', x.text)
                res = word.split(", ")
                keyingredient.append(res)
                dictionary["Ingredients"] = res
                # keyingredient.append(res)
                with open('Recipies.json', 'a') as fp:
                    json.dump(dictionary, fp)
        else:
            dictionary["Ingredients"] = None
            # keyingredient.append(None)

    except Exception as e:
        print(e)
        pass

    i += 1

#     for x in Soup.findAll('div',attrs={'class':'method stylNew'}):
#         procedure=x.find('ul')
#         detail.append(procedure.text)
#     for x in Soup.findAll('div',attrs={'class':'keyword_tag'}):
#         keyingredient.append(x.text)
