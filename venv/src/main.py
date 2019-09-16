from selenium import webdriver
import os

from url_seeker import SeekTask, URLSeekTask, DownloadTask, Context, Group, SubGroupTask

count = 1


def gp_next_book_url(ctx: Context):
    global count
    if count >= 7:
        return ""
    count += 1
    nextpage = ctx.driver.find_elements_by_css_selector(".nav-previous > a")
    if len(nextpage) == 0:
        return ""
    return nextpage[0].get_attribute("href")


def get_next_page_url(ctx: Context) -> str:
    page_links = ctx.driver.find_elements_by_css_selector(".post-page-numbers")
    if len(page_links) == 0:
        return ""
    last_page_links = page_links[len(page_links) - 1]
    if last_page_links.text != "Next »":
        return ""
    return last_page_links.get_attribute("href")


def extract_filename(url: str) -> str:
    return os.path.basename(url).split("?")[0].replace("%20", " ")


def clean_url(url: str) -> str:
    return url.split("?")[0]


def clean_url_window_open(url: str) -> str:
    return url.replace("window.open('", "").replace("');", "")


def hk_ceo():
    return SeekTask(
        url="https://data.gov.hk/en-datasets/provider/hk-ceo?order=name&file-content=no",
        child=Group(
            select_rule=lambda ctx: ctx.driver.find_elements_by_css_selector("h3.dataset-heading > a"),
            convert_rule=lambda url: lambda e: SubGroupTask(groupname=e.text, url=e.get_attribute("href")),
            nextpage_rule=lambda ctx: "",
            child=URLSeekTask(
                select_rule=lambda ctx: ctx.driver.find_elements_by_css_selector(".mobile-view .p-download-btn"),
                export_rule=lambda ctx: lambda e: DownloadTask(
                    folder=ctx.path,
                    filename=extract_filename(clean_url_window_open(e.get_attribute("onclick"))),
                    url=clean_url_window_open(e.get_attribute("onclick"))
                ),
                nextpage_rule=lambda ctx: ""
            )
        )
    )


def main():
    b = webdriver.Chrome()

    task = hk_ceo()

    dlTasks = task.start(b)
    b.close()
    for dlTask in dlTasks:
        print(dlTask)


if __name__ == "__main__":
    main()
