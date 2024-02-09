import requests
from bs4 import BeautifulSoup
import os
def get_random_wikipedia_article(language="en", save_to_file=False, extract_image=True):
    try:
        with requests.get(f"https://{language}.wikipedia.org/wiki/Special:Random") as response:
            soup = BeautifulSoup(response.content, "html.parser")

        arcticle = {
            "title": soup.find("h1").text.strip(),
            "description": soup.find("p").text.strip(),
            "link": response.url,
            "image": ("https:" + soup.find("img")["src"]) if extract_image and soup.find("img") else "No image"
        }
        if extract_image:
            arcticle["image"] = save_image(soup.find("img"), arcticle["title"]) if soup.find("img") else "No image"
        if save_to_file:
            save_article(arcticle)

        return arcticle
    except requests.RequestException as e:
        print(f"Error: {e}")

def save_article(arcticle):
    with open("saved_articles.txt", "a", encoding="utf-8") as file:
        for key, value in arcticle.items():
            file.write(f"{key.capitalize()}: {value}\n")
       
        file.write(f"\n{'-' * 36}\n")

def save_image(image_tag, title):
    image_url = "https:" + image_tag["src"]
    image_name = title.replace(" ", "_") + ".jpg"
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_name, "wb") as file:
                file.write(response.content)
            return image_url

    except requests.RequestException as e:
        print(f"Error: {e}")
        return "Error"
if __name__ == "__main__":
    random_article = get_random_wikipedia_article(language="ru", extract_image=True, save_to_file=True)
    if random_article:
        for key, value in random_article.items():
            print(f"{key.capitalize()}: {value}")



