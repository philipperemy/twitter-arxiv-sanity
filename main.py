from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from slugify import slugify

from bot import Bot
from thumbnail import pdf_to_thumbnail


def main():
    twitter_bot = Bot()
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(5)
    driver.get('http://www.arxiv-sanity.com/toptwtr')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    raw_papers_list = soup.find_all('span', {'class', 'ts'})
    papers_list = []
    for raw_paper in raw_papers_list:
        link = raw_paper.contents[0].attrs['href']
        pdf = link.replace('/abs/', '/pdf/') + '.pdf'
        title = str(raw_paper.contents[0].contents[0])
        papers_list.append({'link': link, 'pdf': pdf, 'title': title})

    for paper in papers_list:
        message = paper['title'] + ' ' + paper['link']
        output_filename = slugify(paper['pdf']) + '.png'
        output_path = pdf_to_thumbnail(paper['pdf'], output_image_filename=output_filename)
        twitter_bot.send_tweet_with_image(message, output_path)
        print(message)
        sleep(5)


if __name__ == '__main__':
    main()
