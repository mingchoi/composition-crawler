# Composition Crawler

This module allow you to use composition to crawler & download resource from web.

For example:
```
SeekTask(
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
```