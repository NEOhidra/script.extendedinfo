import xbmcaddon
import os
import xbmc
from Utils import *
import urllib

moviedb_key = '34142515d9d23817496eeb4ff1d223d0'
__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString
Addon_Data_Path = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % __addonid__).decode("utf-8"))
base_url = ""
poster_size = ""
fanart_size = ""


def HandleTMDBMovieResult(results):
    movies = []
    log("starting HandleTMDBMovieResult")
    for movie in results:
        if ("backdrop_path" in movie) and (movie["backdrop_path"]):
            backdrop_path = base_url + fanart_size + movie['backdrop_path']
        else:
            backdrop_path = ""
        if ("poster_path" in movie) and (movie["poster_path"]):
            poster_path = base_url + poster_size + movie['poster_path']
        else:
            poster_path = ""
        year = movie.get('release_date', "")
        if year:
            year = year[:4]
        trailer = "plugin://script.extendedinfo/?info=playtrailer&&id=" + str(movie.get('id', ""))
        if False:
            path = 'plugin://script.extendedinfo/?info=extendedinfo&&id=%s' % str(movie.get('id', ""))
        else:
            path = trailer
        newmovie = {'Art(fanart)': backdrop_path,
                    'Art(poster)': poster_path,
                    'Thumb': poster_path,
                    'Poster': poster_path,
                    'fanart': backdrop_path,
                    'Title': movie.get('title', ""),
                    'Label': movie.get('title', ""),
                    'OriginalTitle': movie.get('original_title', ""),
                    'ID': movie.get('id', ""),
                    'Path': path,
                    'Trailer': trailer,
                    'Play': "",
                    'DBID': "",
                    'Rating': movie.get('vote_average', ""),
                    'Votes': movie.get('vote_count', ""),
                    'Year': year,
                    'Premiered': movie.get('release_date', "")}
        if not str(movie['id']) in str(movies):  # too dirty
            movies.append(newmovie)
    movies = CompareWithLibrary(movies)
    return movies

def HandleTMDBActorMovieResult(results):
    movies = []
    log("starting HandleTMDBActorMovieResult")
    for movie in results:
        try:
            if ("backdrop_path" in movie) and (movie["backdrop_path"]):
                backdrop_path = base_url + fanart_size + movie['backdrop_path']
            else:
                backdrop_path = ""
            if ("poster_path" in movie) and (movie["poster_path"]):
                poster_path = base_url + poster_size + movie['poster_path']
            else:
                poster_path = ""
            newmovie = {'Art(fanart)': backdrop_path,
                        'Art(poster)': poster_path,
                        'Thumb': poster_path,
                        'Poster': poster_path,
                        'fanart': backdrop_path,
                        'Title': movie.get('title', ""),
                        'OriginalTitle': movie.get('original_title', ""),
                        'ID': movie.get('id', ""),
                        'Path': "plugin://script.extendedinfo/?info=playtrailer&&id=" + str(movie.get('id', "")),
                        'Play': "",
                        'DBID': "",
                        'Rating': movie.get('vote_average', ""),
                        'Votes': movie.get('vote_count', ""),
                        'Year': movie.get('release_date', "")[:4],
                        'Premiered': movie.get('release_date', "")}
            if not str(movie['id']) in str(movies):  # too dirty
                movies.append(newmovie)
        except Exception as e:
            log("Exception:")
            log(e)
            prettyprint(movie)
    movies = CompareWithLibrary(movies)
    return movies


def HandleTMDBTVShowResult(results):
    tvshows = []
    log("starting HandleTMDBTVShowResult")
    for tv in results:
        if ("backdrop_path" in tv) and (tv["backdrop_path"]):
            backdrop_path = base_url + fanart_size + tv['backdrop_path']
        else:
            backdrop_path = ""
        if ("poster_path" in tv) and (tv["poster_path"]):
            poster_path = base_url + poster_size + tv['poster_path']
        else:
            poster_path = ""
        newtv = {'Art(fanart)': backdrop_path,
                 'Art(poster)': poster_path,
                 'Thumb': poster_path,
                 'Poster': poster_path,
                 'fanart': backdrop_path,
                 'Title': tv.get('name', ""),
                 'OriginalTitle': tv.get('original_name', ""),
                 'ID': tv.get('id', ""),
                 'Path': "",
                 'Play': "",
                 'DBID': "",
                 'Rating': tv.get('vote_average', ""),
                 'Votes': tv.get('vote_count', ""),
                 'Premiered': tv.get('first_air_date', "")}
        if not str(tv['id']) in str(tvshows):  # too dirty
            tvshows.append(newtv)
    tvshows = CompareWithLibrary(tvshows)
    return tvshows


def HandleTMDBListResult(results):
    lists = []
    for movielist in results["lists"]["results"]:
        newlist = {'Art(poster)': base_url + poster_size + str(movielist.get('poster_path', "")),
                   'Title': movielist['name'],
                   'ID': movielist['id'],
                   'Description': movielist['description']}
        lists.append(newlist)
    return lists


def HandleTMDBPeopleResult(results):
    people = []
    for person in results:
        description = "[B]Known for[/B]:[CR][CR]"
        if "known_for" in results:
            for movie in results["known_for"]:
                description = description + movie["title"] + " (%s)" % (movie["release_date"]) + "[CR]"
        builtin = 'RunScript(script.metadata.actors,"%s")' % (unicode(person.get('name', "")))
        if "profile_path" in person and person["profile_path"] is not None:
            image = base_url + poster_size + person["profile_path"]
        else:
            image = ""
        alsoknownas = " / ".join(person.get('also_known_as', ""))
        newperson = {'adult': str(person.get('adult', "")),
                     'name': person['name'],
                     'title': person['name'],
                     'also_known_as': alsoknownas,
                     'alsoknownas': alsoknownas,
                     'biography': person.get('biography', ""),
                     'birthday': person.get('birthday', ""),
                     'description': description,
                     'plot': description,
                     'id': str(person['id']),
                     'path': "plugin://script.extendedinfo/?info=action&&id=" + builtin,
                     'deathday': person.get('deathday', ""),
                     'place_of_birth': person.get('place_of_birth', ""),
                     'placeofbirth': person.get('place_of_birth', ""),
                     'homepage': person.get('homepage', ""),
                     'thumb': image,
                     'icon': image,
                     'poster': image}
        people.append(newperson)
    return people

def HandleTMDBPeopleImagesResult(results):
    images = []
    for item in results["images"]["profiles"]:
        image_path = base_url + poster_size + item['file_path']
        image = {'aspectratio': item['aspect_ratio'],
                 'thumb': image_path,
                 'poster': image_path}
        images.append(image)
    return images



def HandleTMDBCompanyResult(results):
    companies = []
    log("starting HandleLastFMCompanyResult")
    for company in results:
        newcompany = {'parent_company': company['parent_company'],
                      'name': company['name'],
                      'description': company['description'],
                      'headquarters': company['headquarters'],
                      'homepage': company['homepage'],
                      'id': company['id'],
                      'logo_path': company['logo_path']}
        companies.append(newcompany)
    return companies


def SearchforCompany(Company):
  #  Companies = Company.split(" / ")
   # Company = Companies[0]
    import re
    regex = re.compile('\(.+?\)')
    Company = regex.sub('', Company)
    log(Company)
    response = GetMovieDBData("search/company?query=%s&" % urllib.quote_plus(Company), 30)
    try:
        return response["results"][0]["id"]
    except:
        log("could not find Company ID")
        return ""


def GetPersonID(person):
    persons = person.split(" / ")
    # if len(persons) > 1:
    #     personlist = []
    #     for item in persons:
    #         personlist.append(item["name"])
    #     dialog = xbmcgui.Dialog()
    #     selection = dialog.select("Select Actor", personlist)
    # else:
    person = persons[0]
    response = GetMovieDBData("search/person?query=%s&include_adult=true&" % urllib.quote_plus(person), 30)
    try:
        return response["results"][0]["id"]
    except:
        log("could not find Person ID")
        return ""


def SearchForSet(setname):
    setname = setname.replace("[", "").replace("]", "").replace("Kollektion", "Collection")
    response = GetMovieDBData("search/collection?query=%s&language=%s&" % (urllib.quote_plus(setname.encode("utf-8")), __addon__.getSetting("LanguageID")), 14)
    try:
        return response["results"][0]["id"]
    except:
        return ""


def GetMovieDBData(url="", cache_days=14):
    url = "http://api.themoviedb.org/3/%sapi_key=%s" % (url, moviedb_key)
    global base_url
    global poster_size
    global fanart_size
    if not base_url:
        log("fetching base_url and size (MovieDB config)")
        base_url = True
        base_url, poster_size, fanart_size = GetMovieDBConfig()
    results = Get_JSON_response(url, cache_days)
    return results


def GetMovieDBConfig():
    response = GetMovieDBData("configuration?", 60)
    if response:
        return (response["images"]["base_url"], response["images"]["poster_sizes"][-2], response["images"]["backdrop_sizes"][-2])
    else:
        return ("", "", "")


def GetCompanyInfo(Id):
    response = GetMovieDBData("company/%s/movies?append_to_response=movies&" % (Id), 30)
    if response and "results" in response:
        return HandleTMDBMovieResult(response["results"])
    else:
        return []


def millify(n):
    import math
    millnames = ['', 'Thousand', 'Million', 'Billion', 'Trillion']
    # millnames = ['', 'k', 'm', 'b', 't']
    millidx = max(0, min(len(millnames) - 1, int(math.floor(math.log10(abs(n)) / 3.0))))
    return '%.0f %s' % (n / 10 ** (3 * millidx), millnames[millidx])


def GetSeasonInfo(tvshowname, seasonnumber):
    response = GetMovieDBData("search/tv?query=%s&language=%s&" % (urllib.quote_plus(tvshowname), __addon__.getSetting("LanguageID")), 30)
    tvshowid = str(response['results'][0]['id'])
    response = GetMovieDBData("tv/%s/season/%s?append_to_response=videos&language=%s&" % (tvshowid, seasonnumber, __addon__.getSetting("LanguageID")), 30)
    season = {'SeasonDescription': response["overview"],
              'AirDate': response["air_date"]}
    videos = []
    for item in response["videos"]["results"]:
        video = {'key': item["key"],
                 'name': item["name"],
                 'type': item["type"]}
        videos.append(video)
    return season, videos


def GetMovieDBID(imdbid):
    response = GetMovieDBData("find/tt%s?external_source=imdb_id&language=%s&" % (imdbid, __addon__.getSetting("LanguageID")), 30)
    return response["movie_results"][0]["id"]


def GetExtendedMovieInfo(movieid):
    response = GetMovieDBData("movie/%s?append_to_response=trailers,casts,releases,keywords,similar_movies,lists&language=%s&" % (movieid, __addon__.getSetting("LanguageID")), 30)
    authors = []
    directors = []
    genres = []
    if not response:
        Notify("Could not get movie information")
        return {}, []
    for item in response['genres']:
        genres.append(item["name"])
    for item in response['casts']['crew']:
        if item["job"] == "Author":
            authors.append(item["name"])
        if item["job"] == "Director":
            directors.append(item["name"])
    Writer = " / ".join(authors)
    Director = " / ".join(directors)
    Genre = " / ".join(genres)
    if len(response['trailers']['youtube']) > 0:
        Trailer = response['trailers']['youtube'][0]['source']
    else:
        Trailer = ""
    if len(response['releases']['countries']) > 0:
        mpaa = response['releases']['countries'][0]['certification']
    else:
        mpaa = ""
    if len(response['production_countries']) > 0:
        Country = response['production_countries'][0]["name"]
    else:
        Country = ""
    if len(response['production_companies']) > 0:
        Studio = response['production_companies'][0]["name"]
    else:
        Studio = ""
    Set = response.get("belongs_to_collection", "")
    if Set:
        SetName = Set.get("name", "")
        SetID = Set.get("id", "")
    else:
        SetName = ""
        SetID = ""
    if 'release_date' in response and response.get('release_date') is not None:
        year = response.get('release_date', "")[:4]
    else:
        year = ""
    BudgetValue = response.get('budget', "")
    if not BudgetValue in [0, ""]:
        Budget = millify(float(BudgetValue))
    else:
        Budget = ""
    if ("backdrop_path" in response) and (response["backdrop_path"]):
        backdrop_path = base_url + fanart_size + response['backdrop_path']
    else:
        backdrop_path = ""
    if ("poster_path" in response) and (response["poster_path"]):
        poster_path = base_url + poster_size + response['poster_path']
    else:
        poster_path = ""
    if False:
        path = 'plugin://script.extendedinfo/?info=extendedinfo&&id=%s' % str(response.get('id', ""))
    else:
        path = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % Trailer
    movie = {'Art(fanart)': backdrop_path,
             'Art(poster)': poster_path,
             'Thumb': poster_path,
             'Poster': poster_path,
             'fanart': backdrop_path,
             'Title': response.get('title', ""),
             'Label': response.get('title', ""),
             'Tagline': response.get('tagline', ""),
             'RunningTime': response.get('runtime', ""),
             'Duration': response.get('runtime', ""),
             'mpaa': mpaa,
             'Director': Director,
             'Writer': Writer,
             'Budget': Budget,
             'Homepage': response.get('homepage', ""),
             'Set': SetName,
             'SetId': SetID,
             'ID': response.get('id', ""),
             'Plot': response.get('overview', ""),
             'OriginalTitle': response.get('original_title', ""),
             'Genre': Genre,
             'Rating': response.get('vote_average', ""),
             'Play': '',
             'Trailer': 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % Trailer,
             'Path': path,
             'ReleaseDate': response.get('release_date', ""),
             'Premiered': response.get('release_date', ""),
             'Country': Country,
             'Studio': Studio,
             'DiscArt': "",
             'VideoResolution': "",
             'AudioChannels': "",
             'VideoCodec': "",
             'VideoAspect': "",
             'Logo': "",
             'DBID': "",
             'Studio': Studio,
             'Year': year}
    movie = CompareWithLibrary([movie])[0]
    actors = HandleTMDBPeopleResult(response["casts"]["cast"])
    return movie, actors


def GetExtendedActorInfo(actorid):
    response = GetMovieDBData("person/%s?append_to_response=tv_credits,movie_credits,images,tagged_images&" % (actorid), 1)
    person = HandleTMDBPeopleResult([response])
    images = HandleTMDBPeopleImagesResult(response)
    movie_roles = HandleTMDBMovieResult(response["movie_credits"]["cast"])
    tvshow_roles = HandleTMDBMovieResult(response["tv_credits"]["cast"])
    return person[0], movie_roles, tvshow_roles, images


def GetMovieLists(Id):
    response = GetMovieDBData("movie/%s?append_to_response=trailers,casts,releases,keywords,similar_movies,lists&language=%s&" % (Id, __addon__.getSetting("LanguageID")), 30)
    return HandleTMDBListResult(response)


def GetPopularActorList():
    response = GetMovieDBData("person/popular?", 1)
    return HandleTMDBPeopleResult(response["results"])


def GetActorMovieCredits(actorid):
    response = GetMovieDBData("person/%s/movie_credits?" % (actorid), 1)
    return HandleTMDBMovieResult(response["cast"])


def GetActorTVShowCredits(actorid):
    response = GetMovieDBData("person/%s/tv_credits?" % (actorid), 1)
    return HandleTMDBMovieResult(response["cast"])


def GetMovieKeywords(Id):
    response = GetMovieDBData("movie/%s?append_to_response=trailers,casts,releases,keywords,similar_movies,lists&language=%s&" % (Id, __addon__.getSetting("LanguageID")), 30)
    keywords = []
    if "keywords" in response:
        for keyword in response["keywords"]["keywords"]:
            newkeyword = {'id': keyword.get('id', ""),
                          'name': keyword['name']}
            keywords.append(newkeyword)
        return keywords
    else:
        log("No Keywords in JSON answer")
        return []


def GetSimilarMovies(Id):
    response = GetMovieDBData("movie/%s?append_to_response=trailers,casts,releases,keywords,similar_movies,lists&language=%s&" % (Id, __addon__.getSetting("LanguageID")), 30)
    if "similar_movies" in response:
        return HandleTMDBMovieResult(response["similar_movies"]["results"])
    else:
        log("No JSON Data available")


def GetMovieDBTVShows(tvshowtype):
    response = GetMovieDBData("tv/%s?language=%s&" % (tvshowtype, __addon__.getSetting("LanguageID")), 2)
    if "results" in response:
        return HandleTMDBTVShowResult(response["results"])
    else:
        log("No JSON Data available for GetMovieDBMovies(%s)" % tvshowtype)
        log(response)


def GetMovieDBMovies(movietype):
    response = GetMovieDBData("movie/%s?language=%s&" % (movietype, __addon__.getSetting("LanguageID")), 2)
    if "results" in response:
        return HandleTMDBMovieResult(response["results"])
    else:
        log("No JSON Data available for GetMovieDBMovies(%s)" % movietype)
        log(response)


def GetSetMovies(Id):
    response = GetMovieDBData("collection/%s?language=%s&" % (Id, __addon__.getSetting("LanguageID")), 14)
    if "parts" in response:
        return HandleTMDBMovieResult(response["parts"])
    else:
        log("No JSON Data available")


def GetDirectorMovies(Id):
    response = GetMovieDBData("person/%s/credits?language=%s&" % (Id, __addon__.getSetting("LanguageID")), 14)
    # return HandleTMDBMovieResult(response["crew"]) + HandleTMDBMovieResult(response["cast"])
    if "crew" in response:
        return HandleTMDBMovieResult(response["crew"])
    else:
        log("No JSON Data available")


def search_movie(medianame, year=''):
    log('TMDB API search criteria: Title[''%s''] | Year[''%s'']' % (medianame, year))
    medianame = urllib.quote_plus(medianame.encode('utf8', 'ignore'))
    response = GetMovieDBData("search/movie?query=%s+%s&language=%s&" % (medianame, year, __addon__.getSetting("LanguageID")), 1)
    tmdb_id = ''
    try:
        if response == "Empty":
            tmdb_id = ''
        else:
            for item in response['results']:
                if item['id']:
                    tmdb_id = item['id']
                    log(tmdb_id)
                    break
    except Exception as e:
        log(e)
    if tmdb_id == '':
        log('TMDB API search found no ID')
    else:
        log('TMDB API search found ID: %s' % tmdb_id)
    return tmdb_id