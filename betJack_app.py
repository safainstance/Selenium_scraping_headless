import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Headless mode
options = Options()  # Initialize an instance of the Options class
options.headless = True  # True -> Headless mode activated
options.add_argument('window-size=1920x1080')  # Set a big window size, so all the data will be displayed

web = "https://betjack.com/en/sports/basketball/ncaab"
path = 'C:\\upwork\\python_scrapping\\Selenium\\driver\\chromedriver.exe'
service = Service(path)
driver = webdriver.Chrome(service=service,options=options)
driver.get(web)
driver.implicitly_wait(5)
container = driver.find_element(By.XPATH, "//*/div[contains(@class,'SkeletonContainer__AnimateContainerCss')]")

parent_next_div = container.find_element(By.TAG_NAME,'div')

# date = parent_next_div.find_element(By.XPATH, ".//*/div[contains(@class,'EventGroup__HeaderCss']")
date = parent_next_div.find_element(By.XPATH, "//div[contains(@class,'EventGroup__HeaderCss')]")
print("date ",date.text)
events = parent_next_div.find_elements(By.XPATH, "//*[contains(@class,'BoardContent__BoardContentCss')]")
commence_date = []
commence_time = []
home_team = []
away_team = []
outcome_team = []
Point_Spread = []
Spread_Price = []
Money_Line = []
Total_Points = []
Total_Price = []
for event in events:
    parents = event.find_elements(By.XPATH, "./div[contains(@class,'Event__EventCss-sc-1v7np2h-0 jMljNN')]")
    print("Lenght =", str(len(parents)))

    for parent in parents:
        teams = parent.find_elements(By.XPATH, ".//*/span[contains(@class,'PlayerInfo__PlayerInfoNameCss')]")
        time_match = parent.find_element(By.XPATH, "//div[contains(@class,'InfoGroup__ExtraInfoCss')]/div")
        time_match = time_match.text
        home = teams[0].text
        away = teams[1].text
        print("Home : ",home)
        print("Away : ",away)
        commence_date.append(date.text)
        home_team.append(home)
        away_team.append(away)
        outcome_team.append(home)
        commence_time.append(time_match)

        commence_date.append(date.text)
        home_team.append(home)
        away_team.append(away)
        outcome_team.append(away)
        commence_time.append(time_match)

        threeColumns = parent.find_element(By.XPATH, ".//*[contains(@class, 'ThreeColumns__ThreeColumnsCss')]")
        outComeList = threeColumns.find_elements(By.XPATH, ".//*[contains(@class, 'OutcomeList__OutcomeListCss')]")
        count = int(len(outComeList))
        list = []
        for column in outComeList:
            title = column.find_element(By.XPATH, ".//*/span[contains(@class,'OutcomeList__OutcomeListTitleCss')]")
            title = title.text
            list.append(title)
            points = column.find_elements(By.XPATH,".//li[contains(@class,'OutcomeList__OutcomeListCollectionItemCss')]")

            if title == "Point Spread":
                points1 = points[0].text.split("\n")
                Point_Spread.append(points1[0])
                Spread_Price.append(points1[1])
                points2 = points[1].text.split("\n")
                Point_Spread.append(points2[0])
                Spread_Price.append(points2[1])
            elif title == "Moneyline":
                Money_Line.append(points[0].text)
                Money_Line.append(points[1].text)
            elif title == "Total Points":
                points1 = points[0].text.split("\n")
                Total_Points.append(points1[0])
                Total_Price.append(points1[1])
                points2 = points[1].text.split("\n")
                Total_Points.append(points2[0])
                Total_Price.append(points2[1])
        if "Moneyline" not in list:
            Money_Line.append("No value")
            Money_Line.append("No value")
        if "Point Spread" not in list:
            Point_Spread.append("No value")
            Spread_Price.append("No value")
        if "Total Points" not in list:
            Total_Points.append("No value")
            Total_Price.append("No value")
        print("________________________")
    break
driver.quit()
df_books = pd.DataFrame({'commence_date': commence_date, 'commence_time': commence_time, 'home_team': home_team,
                         'away_team': away_team, 'outcome_team': outcome_team, 'Point Spread': Point_Spread,
                         'Spread-Price': Spread_Price, 'Money Line': Money_Line, 'Total Points': Total_Points,
                                                'Total Price': Total_Price})
df_books.to_csv('betJack_basketball_ncaab.csv', index=False)


