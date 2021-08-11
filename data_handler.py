# %%
import requests
import json
import pandas


def getRKIData() -> pandas.DataFrame:
    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=cases7_per_100k%20desc&resultOffset=0&resultRecordCount=500&resultType=standard&cacheHint=true"
    data = json.loads(requests.get(url).text)
    return pandas.DataFrame([x["attributes"] for x in data["features"]])


def getIntensivData() -> pandas.DataFrame:
    url = "https://www.intensivregister.de/api/public/reporting/laendertabelle?format=json&onlyErwachsenenBetten=true&onlyHaupversorgerCovid19=false"
    data = json.loads(requests.get(url).text)
    return pandas.DataFrame(data["data"])


def getVaccinationData() -> pandas.DataFrame:
    url = "https://covid.ourworldindata.org/data/internal/megafile--vaccinations-bydose.json"
    data = json.loads(requests.get(url).text)
    return pandas.DataFrame(data)


covid_data_rki = getRKIData()
covid_data_intensiv = getIntensivData()
covid_data_vaccination = getVaccinationData() # Blöde Idee von [vorname != "Simon" && vorname == Elias && nachname == Atmani]...

print("Loaded Data")

# %%
print(covid_data_rki[["GEN", "BL", "cases7_per_100k"]].to_string())
print(covid_data_intensiv[["bundesland", "bettenBelegtToBettenGesamtPercent",
      "intensivBettenBelegt", "intensivBettenGesamt"]].to_string())
print(
    covid_data_vaccination[covid_data_vaccination["location"] == "Germany"].to_string())
    
# %%
def getSelectPageData():
    def ich_hasse_Python(x):
        y = list(x)
        y.sort()
        return y
    return covid_data_rki.groupby('BL').agg({'GEN':ich_hasse_Python})["GEN"].to_dict()

# %%
def getMainPageData(Kreis: str):
    output_data = dict()
    covid_kreis = covid_data_rki[covid_data_rki["GEN"] == Kreis]
    covid_kreis_inzidenz = covid_kreis["cases7_per_100k"].index[0]
    #covid_kreis_betten = covid_data_intensiv[["BettenFrei"] == Kreis]
    inz = 0
    if covid_kreis_inzidenz < 10:
        inz = 1
    if 10 <= covid_kreis_inzidenz < 35:
        inz = 2
    if 35 <= covid_kreis_inzidenz < 50:
        inz = 3
    if covid_kreis_inzidenz > 50:
        inz = 4
    output_data["covid_kreis_inzidenz"] = covid_kreis_inzidenz
    output_data["inz"] = inz

getMainPageData("Aichach-Friedberg")

#hi

# %%


