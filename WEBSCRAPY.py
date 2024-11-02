import hashlib
import io
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image


def get_content_from_url(url):
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Firefox()  # If you're using Chrome, uncomment the Chrome line below
    # driver = webdriver.Chrome(options=options)

    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    return page_content


def parse_image_urls(content, classes, location, source):
    soup = BeautifulSoup(content, "html.parser")
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name and name.get(source) not in results:
            results.append(name.get(source))
    return results


def save_urls_to_csv(image_urls):
    df = pd.DataFrame({"links": image_urls})
    df.to_csv("links.csv", index=False, encoding="utf-8")


def get_and_save_image_to_file(image_url, output_dir):
    try:
        image_content = requests.get(image_url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")

        filename = hashlib.sha1(image_content).hexdigest()[:10] + ".png"

        # Use Path class for consistent filepath handling
        file_path = Path(output_dir) / filename

        image.save(file_path, "PNG", quality=80)
        print(f"Saved image: {file_path}")
    except Exception as e:
        print(f"Error saving image {image_url}: {e}")


def main():
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptop&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=laptop"
    content = get_content_from_url(url)
    image_urls = parse_image_urls(
        content=content, classes="s-item__image-wrapper image-treatment", location="img", source="src"
    )
    save_urls_to_csv(image_urls)

    # Use the specified output directory on your machine
    output_dir = Path(r"C:\Users\gowth\Downloads\EBAY")  # Updated to the required path

    # Ensure the directory exists before saving the images
    output_dir.mkdir(parents=True, exist_ok=True)

    for image_url in image_urls:
        get_and_save_image_to_file(image_url, output_dir=output_dir)


if __name__ == "__main__":  # Fixed typo here
    main()
    print("Done!")
