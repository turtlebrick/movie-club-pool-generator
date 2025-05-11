import requests
from dotenv import load_dotenv
import os
import random

load_dotenv()

TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"


def get_movie() -> dict:
    correct_title_and_year = False

    while not correct_title_and_year:
        movie_title = input("\nMovie Title: ")
        is_digit = False

        while not is_digit:
            is_digit = False

            movie_release_year = input("Movie Release Year: ")
            if not movie_release_year.isdigit() or len(movie_release_year) != 4:
                print("Error: Invalid format. Please enter release year as a 4 digit number.")
            else:
                movie_release_year = int(movie_release_year)
                is_digit = True
        
        is_yes_or_no = False

        while not is_yes_or_no:
            answer = input(f"\nIs this information correct? ['yes'/'no']\n\tMovie Title{'.' * (len("Movie Release Year") - len("Movie Title"))}: {movie_title}\n\tMovie Release Year: {movie_release_year}\n\n")

            if answer in ['yes', 'no']:
                is_yes_or_no = True
            else:
                print("Error: Invalid response. Answer must be \"yes\" or \"no\".")
        
        if answer == 'yes':
            correct_title_and_year = True

    movie = {
        'title': movie_title,
        'release_year': movie_release_year
    }
    
    return movie


def get_movie_json(title: str, year: int) -> dict:
    """
    Get Movie JSON

    Returns a dict from TMDB's API matching the given movie title and release year
    """

    url = f"{BASE_URL}/search/movie?query={title.replace(' ', '%20').lower()}&language=en-US&page=1&year={year}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YzI4MWM0MzAxNzJhMjM4YTU2NmVjYzM2MGE1YWU2NCIsIm5iZiI6MTc0NjgzODk0OS4wMzMsInN1YiI6IjY4MWVhNWE1MDQyMWQxNGVlMjJkMGVhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AREey9-TzMXouo02WXUcs8_TWQwXz6t66tDcnS2mO04"
    }

    response = requests.get(url, headers=headers)

    return response.json()


def get_movie_crew_json(id: int) -> dict:
    url = f"{BASE_URL}/movie/{id}/credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YzI4MWM0MzAxNzJhMjM4YTU2NmVjYzM2MGE1YWU2NCIsIm5iZiI6MTc0NjgzODk0OS4wMzMsInN1YiI6IjY4MWVhNWE1MDQyMWQxNGVlMjJkMGVhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AREey9-TzMXouo02WXUcs8_TWQwXz6t66tDcnS2mO04"
    }

    response = requests.get(url, headers=headers)

    return response.json()


def get_movie_details_json(id: int) -> dict:
    url = f"{BASE_URL}/movie/{id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YzI4MWM0MzAxNzJhMjM4YTU2NmVjYzM2MGE1YWU2NCIsIm5iZiI6MTc0NjgzODk0OS4wMzMsInN1YiI6IjY4MWVhNWE1MDQyMWQxNGVlMjJkMGVhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AREey9-TzMXouo02WXUcs8_TWQwXz6t66tDcnS2mO04"
    }

    response = requests.get(url, headers=headers)

    return response.json()


def get_movie_dict() -> dict:
    movie_dict = {}
    adding_more_movies = True

    while adding_more_movies:
        is_correct_movie = False

        movie = get_movie()
        print("\nSearching for movie...")
        
        movie_json = get_movie_json(
            title=movie.get('title'),
            year=movie.get('release_year')
        )

        while not is_correct_movie:
            for result in movie_json.get('results'):
                id = result.get('id')
                movie_crew_json = get_movie_crew_json(id=id)
                if "Director" not in [crew_member.get('job') for crew_member in movie_crew_json.get('crew')]:
                    continue

                director = next(
                    crew_member.get('name') 
                    for crew_member in movie_crew_json.get('crew') 
                    if crew_member.get('job') == "Director"
                )
                starring = [
                    crew_member.get('name') 
                    for crew_member in movie_crew_json.get('cast')
                ][:3]

                is_yes_or_no = False

                while not is_yes_or_no:
                    answer = input(f"\nIs this information correct? ['yes'/'no']\n\n\tDirected by: {director}\n\tStarring{'.' * (len("Directed by") - len("Starring"))}: {', '.join(starring)}\n\tOverview{'.' * (len("Directed by") - len("Overview"))}: {result.get('overview')}\n\n")

                    if answer in ['yes', 'no']:
                        is_yes_or_no = True
                    else:
                        print("Error: Invalid response. Answer must be \"yes\" or \"no\".")

                if answer == "yes":
                    details = get_movie_details_json(id=id)

                    movie_dict[details.get('title')] = {
                        'details': details, 
                        'credits': movie_crew_json
                    }

                    is_correct_movie = True
                    is_yes_or_no = False

                    while not is_yes_or_no:
                        answer = input("\nWould you like to add another movie? ['yes'/'no']\n\n")

                        if answer in ['yes', 'no']:
                            is_yes_or_no = True
                        else:
                            print("Error: Invalid response. Answer must be \"yes\" or \"no\".")
                    
                    if answer == "no":
                        adding_more_movies = False
                
                if is_correct_movie:
                    break
    
    return movie_dict


def get_decade_window(year: int) -> str:
    if year >= 1900 and year < 1960: return "40s - 50s"
    elif year >= 1960 and year < 1980: return "60s - 70s"
    elif year >= 1980 and year < 2000: return "80s - 90s"
    else: return "2000s"


def get_stripped_movie_dict(movie_dict: dict) -> dict:
    stripped_movie_dict = {}

    for title, movie in movie_dict.items():
        details = movie.get('details')
        year = details.get('release_date').split('-')[0]
        decade_window = get_decade_window(year=int(year))
        language = details.get('spoken_languages')[0].get('english_name')
        genres = [genre.get('name') for genre in details.get('genres')]

        stripped_movie_dict[title] = {
            'title': title,
            'year': year,
            'decade_window': decade_window,
            'language': language,
            'genres': genres
        }
    
    return stripped_movie_dict


def get_lowest_similarity(diverse_movie_quintuplet: list, movie_options: list):
    present_qualities = {
        'decade_windows': [movie.get('decade_window') for movie in diverse_movie_quintuplet],
        'languages': [movie.get('language') for movie in diverse_movie_quintuplet],
        'genres': [genre for movie in diverse_movie_quintuplet for genre in movie.get('genres')]
    }

    for title, movie in movie_options.items():
        similarity = 0

        if movie.get('language') in present_qualities.get('languages'): similarity += 10
        if movie.get('decade_window') in present_qualities.get('decade_windows'): similarity += 5
        similarity += len([genre for genre in movie.get('genres') if genre in present_qualities.get('genres')])
        similarity = int(float(similarity) / float(15 + len(present_qualities.get('genres'))) * 100)

        movie['similarity'] = similarity
    
    lowest_similarity = min([movie.get('similarity') for movie in movie_options])
    movies_with_lowest_similarity = [movie for movie in movie_options if movie.get('similarity') == lowest_similarity]

    if len(movies_with_lowest_similarity) == 1:
        return movies_with_lowest_similarity[0]
    else:
        return movies_with_lowest_similarity[random.randint(0, len(movies_with_lowest_similarity) - 1)]


def get_diverse_quintuplet(stripped_movie_dict: dict) -> list:
    diverse_movie_quintuplet = []
    english_movies = [movie for title, movie in stripped_movie_dict.items() if movie.get('language') == "English"]
    foreign_movies = [movie for title, movie in stripped_movie_dict.items() if movie.get('language') != "English"]

    print(len(english_movies))
    print(len(foreign_movies))

    while len(diverse_movie_quintuplet) < 4:
        if len([movie for movie in diverse_movie_quintuplet if movie.get('language') != "English"]) < 2:
            if len([movie for movie in diverse_movie_quintuplet if movie.get('language') != "English"]) == 0:
                if len(english_movies) > 1:
                    random_index = random.randint(0, len(english_movies) - 1)
                else:
                    random_index = 0
                diverse_movie_quintuplet.append(english_movies[random_index])
                english_movies.pop(random_index)
                continue
            else:
                if random.randint(0, 1) == 0:
                    movie_with_lowest_similarity = get_lowest_similarity(
                        diverse_movie_quintuplet=diverse_movie_quintuplet,
                        movie_options=english_movies
                    )
                    movie_index = english_movies.index(movie_with_lowest_similarity)
                    diverse_movie_quintuplet.append(english_movies[movie_index])
                    english_movies.pop(movie_index)
                    continue
        
        movie_with_lowest_similarity = get_lowest_similarity(
            diverse_movie_quintuplet=diverse_movie_quintuplet,
            movie_options=foreign_movies
        )
        movie_index = foreign_movies.index(movie_with_lowest_similarity)
        diverse_movie_quintuplet.append(foreign_movies[movie_index])
        continue
    
    assert len(diverse_movie_quintuplet) == 4

    return diverse_movie_quintuplet


def main():
    print("Welcome to Ian's Movie Club Pool Generator! Let's start with gathering a list of movies...")
    movie_dict = get_movie_dict()
    stripped_movie_dict = get_stripped_movie_dict(movie_dict=movie_dict)
    answer = ""

    print("Continue pressing ENTER to generate new lists. Type anything to stop.")

    while answer == "":
        diverse_movie_quintuplet = get_diverse_quintuplet(
            stripped_movie_dict=stripped_movie_dict
        )

        longest_title_len = max([len(movie.get('title')) for movie in diverse_movie_quintuplet])
        longest_language_len = max([len(movie.get('language')) for movie in diverse_movie_quintuplet])

        for movie in diverse_movie_quintuplet:
            print(f"{movie.get('title')} ({movie.get('year')}){'.' * (longest_title_len - len(movie.get('title')))}: {movie.get('language')}{'.' * (longest_language_len - len(movie.get('language')))} ({','.join(movie.get('genres'))})")

        answer = input("")



if __name__ == "__main__":
    main()