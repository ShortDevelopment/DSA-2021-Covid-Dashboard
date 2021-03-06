# %%
import requests
import pandas


def get_rki_data() -> pandas.DataFrame:
    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=cases7_per_100k%20desc&resultOffset=0&resultRecordCount=500&resultType=standard&cacheHint=true"
    data = requests.get(url).json()
    return pandas.DataFrame([x["attributes"] for x in data["features"]])


def get_icu_data() -> pandas.DataFrame:
    url = "https://www.intensivregister.de/api/public/reporting/laendertabelle?format=json&onlyErwachsenenBetten=true&onlyHaupversorgerCovid19=false"
    data = requests.get(url).json()
    return pandas.DataFrame(data["data"])


def get_vaccination_data() -> pandas.DataFrame:
    url = "https://covid.ourworldindata.org/data/internal/megafile--vaccinations-bydose.json"
    data = requests.get(url).json()
    return pandas.DataFrame(data)


covid_data_rki = get_rki_data()
covid_data_icu = get_icu_data()
covid_data_vaccination = get_vaccination_data()

print("Loaded Data")


# %%


def get_select_page_data():
    return covid_data_rki.groupby('BL').agg({'GEN': lambda x: sorted(list(x))})["GEN"].to_dict()


# %%


def get_main_page_data(Kreis: str):
    output_data = dict()
    covid_kreis = covid_data_rki[covid_data_rki["GEN"] == Kreis].reset_index()

    bundesland = covid_kreis["BL"][0]
    output_data["bundesland"] = bundesland
    bundesland = bundesland.upper().replace(
        "-", "_").replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")

    covid_kreis_inzidenz = covid_kreis["cases7_per_100k"][0]
    output_data["covid_kreis_inzidenz"] = covid_kreis_inzidenz

    inz = 0
    if covid_kreis_inzidenz < 10:
        inz = 1
    if 10 <= covid_kreis_inzidenz < 35:
        inz = 2
    if 35 <= covid_kreis_inzidenz < 50:
        inz = 3
    if covid_kreis_inzidenz > 50:
        inz = 4

    output_data["inz"] = inz

    deutsche_impfis = pandas.DataFrame(
        covid_data_vaccination[covid_data_vaccination["location"] == "Germany"])
    neueste_deutsche_impfis = deutsche_impfis.tail(1).to_dict('r')
    output_data["neueste_deutsche_impfis"] = neueste_deutsche_impfis

    covid_intensiv_data = covid_data_icu[covid_data_icu["bundesland"] == bundesland].to_dict(
        'r')
    output_data["covid_intensiv_data"] = covid_intensiv_data

    return output_data


# %%
get_select_page_data()
# %%

# %%
