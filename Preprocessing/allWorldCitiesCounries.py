import pandas as pd
import pycountry_convert

def createCitiesPickleFile():

    worldCitiesfile = pd.read_excel('../Docs/worldcities.xlsx',encoding='utf-8')

    worldCitiesDict = {}
    worldIso2Dict = {}
    worldIso3Dict = {}
    worldCountriesDict = {}
    index = 0
    cpt=0
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe'
    }
    unsupportedCountries =[]
    for city in worldCitiesfile['city']:

        try:
            iso2CountryCode = pycountry_convert.country_alpha3_to_country_alpha2(worldCitiesfile['iso3'][index])
            continentCode = pycountry_convert.country_alpha2_to_continent_code(iso2CountryCode)
            country = worldCitiesfile['country'][index].lower()
            worldCountriesDict[country] = continents[continentCode]
            worldCitiesDict[city.lower()] = country
            worldIso2Dict[country] = iso2CountryCode
            worldIso3Dict[country] = worldCitiesfile['iso3'][index]
            worldIso2Dict[iso2CountryCode.lower()] = country # a problem when i try to transform the iso2 code to lower  case
            worldIso3Dict[worldCitiesfile['iso3'][index].lower()] =  country
        except:
            unsupportedCountries.append(worldCitiesfile['iso3'][index].lower())
            cpt+=1
            pass
        index += 1
    print(cpt)
    unsupportedCountries = set(unsupportedCountries)
    print("number of unsupported countries",unsupportedCountries)
    print("number of countries",worldCountriesDict.__len__())
    print("number of iso2",worldIso2Dict.__len__())
    print("number of iso3",worldIso3Dict.__len__())
    print("number of cities",worldCitiesDict.__len__())
    import pickle
    with open('../Docs/locations.pickle','wb') as file:
        pickle.dump(worldCitiesDict , file)
        pickle.dump(worldIso2Dict, file)
        pickle.dump(worldIso3Dict, file)
        pickle.dump(worldCountriesDict, file)
    print("succes !")

createCitiesPickleFile()
