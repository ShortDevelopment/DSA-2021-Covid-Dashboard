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
covid_data_vaccination = getVaccinationData()

print("Loaded Data")

# %%
print(covid_data_rki[["GEN", "BL", "cases7_per_100k"]].to_string())
print(covid_data_intensiv[["bundesland", "bettenBelegtToBettenGesamtPercent",
      "intensivBettenBelegt", "intensivBettenGesamt"]].to_string())
print(
    covid_data_vaccination[covid_data_vaccination["location"] == "Germany"].to_string())
# %%
