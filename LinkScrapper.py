from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json
import re


def end_of_records():
    if len(driver.find_elements(By.XPATH, '//*[@id="recipeListing"]/div[last()]/ul/li')) == 0:
        return False
    return driver.find_element_by_xpath('//*[@id="recipeListing"]/div[last()]/ul/li').text == 'No Record Found'


options = Options()
options.Headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(
    options=options, executable_path="/Users/bluetomato/Projects/experiments/chromedriver")

website_list = ['https://food.ndtv.com/recipes/breads-recipes', 'https://food.ndtv.com/recipes/snacks-recipes',
                'https://food.ndtv.com/recipes/vegetarian-recipes', 'https://food.ndtv.com/recipes/chicken-recipes',
                'https://food.ndtv.com/recipes/rice-recipes', 'https://food.ndtv.com/recipes/desserts-recipes',
                'https://food.ndtv.com/recipes/breakfast-recipes', 'https://food.ndtv.com/recipes/healthy-recipes',
                'https://food.ndtv.com/recipes/meat-recipes', 'https://food.ndtv.com/recipes/dinner-party-recipes'
                ]

# to get list of recipe names and links

for x in website_list:
    driver.get(x)

    show_link = driver.find_elements_by_xpath('//*[@id="pagination"]/a')

    while show_link[0].is_displayed() and not end_of_records():
        driver.execute_script("arguments[0].click();", show_link[0])
        show_link = driver.find_elements_by_xpath('//*[@id="pagination"]/a')

    content = driver.page_source
    Soup = BeautifulSoup(content, features="html.parser")
    links = []  # list to get the links of the recipes
    recipeNames = []  # list to get the names of the recipes

    recipe_div = Soup.find("div", {"id": "recipeListing"})

    # listing=recipe_div.ul.findAll('li',class_="main_image")
    # for x in listing:
    #     name=x.find('h2',attrs={'class':'recipe-image-header'})
    #     recipeNames.append(name.text)
    listing = recipe_div.findAll('div', class_="desc")
    for x in listing:
        name = x.find('h2', attrs={'class': 'recipe-image-header'})
        recipeNames.append(name.text)

    linklist = recipe_div.findAll('a', attrs={'itemprop': 'url'})
    for x in linklist:
        links.append(x.get('href'))
    df = pd.DataFrame({'RecipeName': recipeNames, 'Links': links})
    df.to_csv('Recipe.csv', mode='a', index=False, encoding='utf-8')

# making data unique
df = pd.read_csv('Recipe.csv')
df.drop_duplicates(inplace=True)
df.to_csv('StructuredRecipes.csv', index=False)
