from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import sys
import requests
from requests.exceptions import HTTPError
from urllib.request import urlretrieve

ui, _ = loadUiType('main.ui')
countries_url = 'https://restcountries.eu/rest/v2/all'
res = []


class MainWin(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.HandleEvents()

    def HandleEvents(self):
        self.CountriesCombo.currentIndexChanged.connect(
            self.HandleComboBoxChange)
        self.GetCountries.clicked.connect(self.HandleCountriesGet)

    def HandleCountriesGet(self):
        global res
        try:
            res = requests.get(countries_url)
        except HTTPError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f'Error: {e}')
        else:
            res = res.json()
            country_name = []
            for country in res:
                country_name.append(country['name'])

            self.CountriesCombo.addItems(country_name)

    def HandleComboBoxChange(self):
        country_index = self.CountriesCombo.currentIndex()

        self.CountryCode.setText(res[country_index]['alpha3Code'])

        phone_codes = []
        for phone_code in res[country_index]['callingCodes']:
            self.CallingCodes.clear()
            phone_codes.append(phone_code)
        self.CallingCodes.addItems(phone_codes)

        self.SubRegion.setText(res[country_index]['subregion'])

        self.Population.setText(f"{res[country_index]['population']}")

        timezones = []
        for timezone in res[country_index]['timezones']:
            self.Timezones.clear()
            timezones.append(timezone)
        self.Timezones.addItems(timezones)

        borderingCountries = []
        for borderingCountry in res[country_index]['borders']:
            self.BorderingCountries.clear()
            borderingCountries.append(borderingCountry)
        self.BorderingCountries.addItems(borderingCountries)

        currencies = []
        for currency in res[country_index]['currencies']:
            self.Currencies.clear()
            currency_info = [(k, currency[k]) for k in currency]
            currencies.append(
                f"{currency_info[0][1]} | {currency_info[1][1]} | {currency_info[2][1]}"
            )
        self.Currencies.addItems(currencies)

        urlretrieve(res[country_index]['flag'], "flag.svg")
        pixmap = QPixmap('flag.svg')
        self.Flag.setPixmap(pixmap)
        self.Flag.setScaledContents(True)


def main():
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
