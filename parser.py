import requests
from bs4 import BeautifulSoup

def get_random_wikipedia_article(language="en", save_to_file=False, extract_image=True):
    url = f"https://{language}.wikipedia.org/wiki/Special:Random"
    #Получаем html код
    response = requests.get(url)
    html = response.content
    #Парсим html код
    soup = BeautifulSoup(response.text, "html.parser")
    #Находимаем заголвок страницы
    title = soup.find("h1").text.strip()
    #Находим первый параграф
    descriprtion = soup.find("p").text.strip()

    #Формируем ссылку на статью
    full_article_url = response.url

    arcticle = {
        "title": title,
        "description": descriprtion,
        "link": full_article_url
    }

    if extract_image:
        image = soup.find("img")["src"]
        if image:
            arcticle["image"] = "https:" + image
        else:
            arcticle["image"] = "No image"

    if save_to_file:
        save_article(arcticle)

    return arcticle

def save_article(arcticle):
    with open("saved_articles.txt", "a", encoding="utf-8") as file:
        file.write(f"Title: {arcticle['title']}\n")
        file.write(f"Description: {arcticle['description']}\n")
        file.write(f"Link: {arcticle['link']}\n")
        if "image" in arcticle:
            file.write(f"Image: {arcticle['image']}\n")
        file.write("\n-------------------------------------------------\n")

random_article = get_random_wikipedia_article(language="ru", extract_image=True, save_to_file=True)
print(f"Title: {random_article['title']}")
print(f"Description: {random_article['description']}")
print(f"Link: {random_article['link']}")
if "image" in random_article:
    print(f"Image: {random_article['image']}")


