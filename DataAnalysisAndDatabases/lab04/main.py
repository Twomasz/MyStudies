import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
from sqlalchemy import create_engine

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020')


def film_in_category(category: Union[int, str]) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli category jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tytule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)
    dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    if not isinstance(category, Union[int, str]):
        return None

    elif isinstance(category, str):
        df = pd.read_sql("""
                            SELECT
                                f.title,
                                l.name "languge",
                                c.name "category"
                            FROM film f
                            INNER JOIN film_category fc on f.film_id = fc.film_id
                            INNER JOIN category c on c.category_id = fc.category_id
                            INNER JOIN language l on l.language_id = f.language_id
                            WHERE c.name LIKE %(category)s
                            ORDER BY f.title, l.name
                         """, con=connection_sqlalchemy, params={"category": category})
        return df
    elif isinstance(category, int):
        df = pd.read_sql("""
                            SELECT
                                f.title,
                                l.name "languge",
                                c.name "category"
                            FROM film f
                            INNER JOIN film_category fc on f.film_id = fc.film_id
                            INNER JOIN category c on c.category_id = fc.category_id
                            INNER JOIN language l on l.language_id = f.language_id
                            WHERE c.category_id = %(category)s
                            ORDER BY f.title, l.name
                         """, con=connection_sqlalchemy, params={"category": category})
        return df


def film_in_category_case_insensitive(category: Union[int, str]) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tytule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)
    dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    if not isinstance(category, Union[int, str]):
        return None

    elif isinstance(category, str):
        df = pd.read_sql("""
                            SELECT
                                f.title,
                                l.name "languge",
                                c.name "category"
                            FROM film f
                            INNER JOIN film_category fc on f.film_id = fc.film_id
                            INNER JOIN category c on c.category_id = fc.category_id
                            INNER JOIN language l on l.language_id = f.language_id
                            WHERE c.name ILIKE %(category)s
                            ORDER BY f.title, l.name
                         """, con=connection_sqlalchemy, params={"category": category})
        return df
    elif isinstance(category, int):
        df = pd.read_sql("""
                            SELECT
                                f.title,
                                l.name "languge",
                                c.name "category"
                            FROM film f
                            INNER JOIN film_category fc on f.film_id = fc.film_id
                            INNER JOIN category c on c.category_id = fc.category_id
                            INNER JOIN language l on l.language_id = f.language_id
                            WHERE c.category_id = %(category)s
                            ORDER BY f.title, l.name
                         """, con=connection_sqlalchemy, params={"category": category})
        return df


def film_cast(title: str) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
        
    Parameters:
    title (int): wartość id kategorii, dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(title, str):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            a.first_name,
                            a.last_name
                        FROM film f
                        INNER JOIN film_category fc on f.film_id = fc.film_id
                        INNER JOIN film_actor fa on f.film_id = fa.film_id
                        INNER JOIN actor a on a.actor_id = fa.actor_id
                        WHERE f.title LIKE %(title)s
                        ORDER BY a.last_name, a.first_name
                     """, con=connection_sqlalchemy, params={"title": title})
    return df
    

def film_title_case_insensitive(words: list):
    """ Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających co najmniej jedno
     z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
        
    Parameters:
    words(list): wartość minimalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(words, list):
        return None

    regex_pattern = f'('
    for word in words[:-1]:
        regex_pattern += word + '|'

    regex_pattern += words[-1] + ')'

    a = '^' + regex_pattern + ' '
    b = ' ' + regex_pattern + '$'
    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            title
                        FROM film
                        WHERE title ~*%(a)s
                        OR title ~*%(b)s
                     """, con=connection_sqlalchemy, params={"a": a, "b": b})
    return df
