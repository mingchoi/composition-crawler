from dataclasses import dataclass
from typing import Callable, List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver


@dataclass()
class DownloadTask:
    folder: str
    filename: str
    url: str


@dataclass()
class SubGroupTask:
    groupname: str
    url: str


@dataclass()
class Context:
    driver: WebDriver
    path: str
    url: str


@dataclass()
class Selector:
    select_rule: Callable[[], List[WebElement]]

    def seek(self, ctx: Context) -> [DownloadTask]:
        return None


@dataclass()
class Group(Selector):
    select_rule: Callable[[], List[WebElement]]
    convert_rule: Callable[[], SubGroupTask]
    nextpage_rule: Callable[[Context], str]
    child: Selector

    def seek(self, ctx: Context) -> [DownloadTask]:
        nextpage = ctx.url
        tasks = []
        while nextpage != "":
            ctx.driver.get(nextpage)
            members = list(map(self.convert_rule(nextpage), self.select_rule(ctx)))
            print(members)
            for m in members:
                tasks += self.child.seek(Context(
                    driver=ctx.driver,
                    path=m.groupname,
                    url=m.url
                ))
            nextpage = self.nextpage_rule(ctx)
        return tasks


@dataclass()
class URLSeekTask(Selector):
    select_rule: Callable[[Context], List[WebElement]]
    export_rule: Callable[[Context], DownloadTask]
    nextpage_rule: Callable[[Context], str]

    def seek(self, ctx: Context) -> [DownloadTask]:
        nextpage = ctx.url
        tasks = []
        while nextpage != "":
            ctx.driver.get(nextpage)
            print(nextpage)
            tasks += list(map(self.export_rule(ctx), self.select_rule(ctx)))
            nextpage = self.nextpage_rule(ctx)
        return tasks


@dataclass()
class SeekTask:
    url: str
    child: Selector

    def start(self, driver: WebDriver):
        ctx = Context(driver=driver, path="/", url=self.url)
        tasks = self.child.seek(ctx)
        return tasks
