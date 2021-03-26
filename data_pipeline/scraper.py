import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path



def make_driver(driver_path:Path):
    options = Options()
    options.headless = True
    # options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    return driver


def scrape_metadata(
    assignee: str, year: int, lang: str, driver, save_path: Path,pages=10
):
    """Scrape patents metadata from Google Patents, querying for
    Assignee's name, Year and Language.


    Args:
        assignee (str): Assignee name
        year (list): Year
        lang (str): Language
        driver (object): selenium driver, obtained from `make_driver`
        save_path (Path): path of output csv file.
        pages (int, optional): number of result pages to scrape for each year.
    """
    metadata = {
        "Name": [],
        "Title": [],
        "Active_Countries": [],
        "Author": [],
        "Link": [],
        "Date_Priority": [],
        "Date_Filed": [],
        "Date_Published": [],
        "Date_Granted": [],
    }
    for month in range(1, 13):
        for page in range(pages):
            URL = (
                f"https://patents.google.com/"
                f"?assignee={assignee}"
                f"&before=priority:{year}{month:02d}31"
                f"&after=priority:{year}{month:02d}01"
                f"&language={lang}"
                f"&num=100"
                f"&page={page}"
            )

            driver.get(URL)

            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pdfLink"))
                )
            except:
                break

            patents_in_page = driver.find_elements_by_tag_name("search-result-item")

            for patent in patents_in_page:
                if len(patent.find_elements_by_class_name("pdfLink")) == 0:
                    continue
                # print(f"Patent number {len(metadata['Name'])}")
                metadata_element = patent.find_element_by_class_name("metadata")
                ###print("Getting Name")
                metadata["Name"].append(
                    patent.find_element_by_class_name("pdfLink")
                    .get_attribute("href")
                    .split("/")[-1]
                )
                ###print("Getting Title")
                metadata["Title"].append(
                    patent.find_element_by_class_name("result-title")
                    .find_element_by_tag_name("span")
                    .get_attribute("innerHTML")
                )
                # Note that we could save not-active and unknown countries aswell
                ###print("Getting Active_Countries")
                active_countries = [
                    x.get_attribute("innerHTML")
                    for x in metadata_element.find_elements_by_class_name("active")
                ]
                metadata["Active_Countries"].append(" ".join(active_countries))
                ###print("Getting Author")
                metadata["Author"].append(
                    metadata_element.find_element_by_css_selector(
                        "span:nth-last-child(2)"
                    )
                    .find_element_by_id("htmlContent")
                    .get_attribute("innerHTML")
                )
                ###print("Getting Link")
                metadata["Link"].append(
                    patent.find_element_by_class_name("pdfLink").get_attribute(
                        "href"
                    )
                )
                ###print("Getting Dates")
                metadata["Date_Priority"].append("")
                metadata["Date_Filed"].append("")
                metadata["Date_Published"].append("")
                metadata["Date_Granted"].append("")
                for date in (
                    patent.find_element_by_class_name("dates")
                    .get_attribute("innerHTML")
                    .split(" • ")
                ):
                    datetype, dateval = date.split(" ")
                    metadata["Date_" + datetype][-1] = dateval

        print(
            f"Scraped month {month}/{year} for a total of {len(metadata['Link'])} entries."
        )

    # Save data
    print(f"Saving year {year} data...")
    df_metadata = pd.DataFrame.from_dict(metadata)
    df_metadata.to_csv(save_path)