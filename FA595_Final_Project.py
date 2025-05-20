# Programmed by Isabella Valentino
# I pledge my honor that I have abided by the Stevens Honor System


# Importing Libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

cities = ['NY', 'LA', 'Chicago', 'Houston']

def createDataFile(city):
    # NYSE Stock File
    stockData = pd.read_csv("NYSE.csv", usecols=['Date', 'Open', 'Close'])
    # InitialOpen stores the opening value of the NYSE for the first line of the file
    initialOpen = stockData['Open'][0]
    # 4 City Weather Files
    weatherData = pd.read_csv(f"weather_{city}.csv", usecols=['datetime', 'conditions'])
    lineCountStockData = len(stockData)  # Holds number of lines in NYSE.csv file
    lineCountWeatherData = len(weatherData)  # Holds number of lines in weather.csv file
    # Writing to New CSV File newFile_(City).csv
    # Column Names
    columns = ['Date', 'Up or Down', 'Weather']
    # Name of CSV File
    writeFile = f"newFile_{city}.csv"
    # The weather files contains weekends while the NYSE.csv does not contain weekends because the stock
    # market is closed. I therefore loop through the NYSE.csv file and compare to the weather files the
    # date in each row and only write a line to newFile_(City).csv if the dates match.

    # Open newFile_(City).csv for writing
    with open(writeFile, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the columns to newFile.csv
        csvwriter.writerow(columns)

        s = 0  # s is index for line number in stockData
        for w in range(lineCountWeatherData):  # w is index for line number in weatherData
            if s < lineCountStockData:
                stockDataDate = stockData['Date'][s]
                # Since the date in the weather file is in a different format than the date in the stockData file
                # I split the values into individual variables for testing later
                stockDataYear, stockDataMonth, stockDataDay = stockDataDate.split('-')
                weatherYear, weatherMonth, weatherDay = weatherData['datetime'][w].split('-')
                # Only write to newFile_(City).csv if the two dates actually match from the
                # weather file weather.csv file and the stockData file NYSE.csv
                if int(stockDataDay) == int(weatherDay) and int(stockDataMonth) == int(weatherMonth) and int(
                        stockDataYear) == int(weatherYear):
                    weather = weatherData['conditions'][w]
                    # upOrDown contains the total points gained or lost for that day on the NYSE from open to close
                    upOrDown = round(stockData['Close'][s] - stockData['Open'][s], 2)
                    # Data Rows of newFile_(City).csv file
                    rows = [stockDataDate, upOrDown, weather]
                    # writing the data rows to newFile.csv
                    csvwriter.writerow(rows)
                    # if the two dates match move to the next line of stockData by increasing its index
                    s += 1
        csvfile.close()
    return initialOpen


def readNewDataFile(city, totalPointsGoodWeather, totalPointsBadWeather):
    numDaysGoodWeather = 0
    numDaysBadWeather = 0
    outlier = 0
    # Now read in the newFile_(City).csv into
    newFileData = pd.read_csv(f"newFile_{city}.csv", usecols=['Date', 'Up or Down', 'Weather'])
    lineCountnewFileData = len(newFileData)  # Holds number of lines in newFile.csv file
    # Loop through the data in newFile_(City).csv - Make calculations necessary for graphing
    for a in range(lineCountnewFileData):
        newFileDataDate = newFileData['Date'][a]
        newFileDataYear, newFileDataMonth, newFileDataDay = newFileDataDate.split('-')
        weather = newFileData['Weather'][a]
        upOrDown = newFileData['Up or Down'][a]
        # This if statement finds how many days there is good weather AND the market is up
        if upOrDown > 0 and weather == "Clear":
            numDaysGoodWeather += 1
        # This elif statement finds how many days there is bad weather AND the market is down
        elif upOrDown < 0 and weather != "Clear":
            numDaysBadWeather += 1
        # This else statement represents data that proves the anomaly wrong, how many days
        # there is good weather AND the market is down and how many days there is bad weather
        # AND the market is up.
        else:
            outlier += 1
        # When weather is Clear tally the points for totalPointsGoodWeather and store in the list using month as an index
        if weather == "Clear":
            totalPointsGoodWeather[int(newFileDataMonth) - 1] = round(
                totalPointsGoodWeather[int(newFileDataMonth) - 1] + upOrDown, 2)
        # If the weather is not Clear tally the points for totalPointsBadWeather and store in the list using month as an index
        elif weather != "Clear":
            totalPointsBadWeather[int(newFileDataMonth) - 1] = round(
                totalPointsBadWeather[int(newFileDataMonth) - 1] + upOrDown, 2)

    return numDaysGoodWeather, numDaysBadWeather, outlier


def calculateResults(initialOpen, totalPointsGoodWeather, totalPointsBadWeather, percentIncreaseGoodWeather,
                     percentIncreaseBadWeather):
    # Calculating Percent Increase for Good Weather and Bad Weather for each month in the list and store in new list
    for i in range(12):
        percentIncreaseGoodWeather[i] = round(totalPointsGoodWeather[i] / initialOpen * 100, 2)
        percentIncreaseBadWeather[i] = round(totalPointsBadWeather[i] / initialOpen * 100, 2)


def outputToConsole(city, numDaysGoodWeather, numDaysBadWeather, outlier, totalPointsGoodWeather, totalPointsBadWeather,
                    percentIncreaseGoodWeather, percentIncreaseBadWeather, monthList):
    # Output to screen number of days Good and Bad weather and Outlier
    print("\nAccuracy of the Sunshine Anomaly for ", city, "\n")
    print("Number of days for Good Weather and market Up:", numDaysGoodWeather)
    print("Number of days for Bad Weather and market Down:", numDaysBadWeather)
    print("Number of days where we have an Outlier:", outlier, "\n")

    # Output to screen percent increase for Good and Bad weather by month same data is used by matPlotLib for graph
    for i in range(12):
        print("Total Points Up or Down for", monthList[i], "Clear Weather:", totalPointsGoodWeather[i], )
        print("Percent Increase for", monthList[i], "Clear Weather:", percentIncreaseGoodWeather[i])
        print("Total Points Up or Down for", monthList[i], "Bad Weather:", totalPointsBadWeather[i])
        print("Percent Increase for", monthList[i], "Bad Weather:", percentIncreaseBadWeather[i])
        print()


def plotGraph(city, monthList, percentIncreaseGoodWeather, percentIncreaseBadWeather):
    # Set up parameters for the matPlotLib for Graph
    X_axis = np.arange(len(monthList))
    plt.bar(X_axis, percentIncreaseGoodWeather, 0.3, label='Percent Increase Good Weather', color="orange")
    plt.bar(X_axis + .35, percentIncreaseBadWeather, 0.3, label='Percent Increase Bad Weather', color="blue")
    plt.xticks(X_axis + .35 / 2, monthList)
    plt.xlabel("Month")
    plt.ylabel("Percentage")
    plt.title("Sunshine Anomaly - % Increase of NYSE by Month {}".format(city))
    plt.legend()
    plt.show()


def main():
    # initialize variables
    totalPointsGoodWeather = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalPointsBadWeather = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    percentIncreaseGoodWeather = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    percentIncreaseBadWeather = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for city in cities:
        initialOpen = createDataFile(city)
        numDaysGoodWeather, numDaysBadWeather, outlier = readNewDataFile(city, totalPointsGoodWeather,
                                                                         totalPointsBadWeather)
        calculateResults(initialOpen, totalPointsGoodWeather, totalPointsBadWeather, percentIncreaseGoodWeather,
                     percentIncreaseBadWeather)
        outputToConsole(city, numDaysGoodWeather, numDaysBadWeather, outlier, totalPointsGoodWeather,
                        totalPointsBadWeather, percentIncreaseGoodWeather, percentIncreaseBadWeather, monthList)
        plotGraph(city, monthList, percentIncreaseGoodWeather, percentIncreaseBadWeather)

main()