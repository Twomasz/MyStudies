import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
from sqlalchemy import create_engine

from typing import Union, List, Tuple


def film_in_category(category_id: int) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge   |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tytule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii, dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(category_id, int):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            f.title,
                            l.name "languge",
                            c.name "category"
                        FROM
                            category c
                        INNER JOIN film_category fc on c.category_id = fc.category_id
                        INNER JOIN film f on f.film_id = fc.film_id
                        INNER JOIN language l on l.language_id = f.language_id
                        WHERE c.category_id = %(category_id)s
                        ORDER BY f.title
                     """, con=connection_sqlalchemy, params={"category_id": category_id})
    return df


def number_films_in_category(category_id: int) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategorii przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii, dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(category_id, int):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            c.name "category",
                            COUNT(f.title)
                        FROM category c
                        INNER JOIN film_category fc on c.category_id = fc.category_id
                        INNER JOIN film f on f.film_id = fc.film_id
                        WHERE c.category_id = %(category_id)s
                        GROUP BY c.name
                     """, con=connection_sqlalchemy, params={"category_id": category_id})
    return df


def number_film_by_length(min_length: Union[int, float] = 0, max_length: Union[int, float] = 1e6):
    """ Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczególnych długości pomiędzy
    wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(min_length, Union[int, float]) or not isinstance(max_length, Union[int, float]) \
            or min_length < 0 or max_length < 0 or min_length > max_length:
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            length,
                            COUNT(title)
                        FROM film
                        WHERE length >= %(min_length)s AND length <= %(max_length)s
                        GROUP BY length
                     """, con=connection_sqlalchemy, params={"min_length": min_length, "max_length": max_length})
    return df


def client_from_city(city: str) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miasta, dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(city, str):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            c.city,
                            cust.first_name,
                            cust.last_name
                        FROM customer cust
                        INNER JOIN address a on a.address_id = cust.address_id
                        INNER JOIN city c on c.city_id = a.city_id
                        WHERE c.city = %(city)s
                     """, con=connection_sqlalchemy, params={"city": city})
    return df


def avg_amount_by_length(length: Union[int, float]) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla
    zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389


    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.

    Parameters:
    length (int,float): długość filmu, dla którego mamy pożyczyć średnią wartość wypożyczonych filmów

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(length, Union[int, float]):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            f.length,
                            AVG(p.amount)
                        FROM film f
                        INNER JOIN inventory i on f.film_id = i.film_id
                        INNER JOIN rental r on i.inventory_id = r.inventory_id
                        INNER JOIN payment p on r.rental_id = p.rental_id
                        WHERE f.length = %(length)s
                        GROUP BY f.length
                        ORDER BY f.length
                     """, con=connection_sqlalchemy, params={"length": length})
    return df


def client_by_sum_length(sum_min: Union[int, float]) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów
    przez klientów powyżej zadanej wartości.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265

    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.

    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów, którą musi spełniać klient

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(sum_min, Union[int, float]):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            c.first_name,
                            c.last_name,
                            SUM(f.length)
                        FROM customer c
                        INNER JOIN rental r on c.customer_id = r.customer_id
                        INNER JOIN inventory i on i.inventory_id = r.inventory_id
                        INNER JOIN film f on f.film_id = i.film_id
                        GROUP BY c.last_name, c.first_name
                        HAVING SUM(f.length) > %(sum_min)s
                        ORDER BY SUM(f.length), c.last_name
                     """, con=connection_sqlalchemy, params={"sum_min": sum_min})
    return df


def category_statistic_length(name: str) -> pd.DataFrame:
    """ Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185

    Jeżeli warunki wejściowe nie są spełnione, to funkcja powinna zwracać wartość None.

    Parameters:
    name (str): Nazwa kategorii, dla której ma zostać wypisana statystyka

    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    """
    if not isinstance(name, str):
        return None

    db = create_engine("postgresql://wbauer_adb:adb2020@pgsql-196447.vipserv.org:5432/wbauer_adb")
    connection_sqlalchemy = db.connect()

    df = pd.read_sql("""
                        SELECT
                            c.name "category",
                            AVG(f.length),
                            SUM(f.length),
                            MIN(f.length),
                            MAX(f.length)
                        FROM category c
                        INNER JOIN film_category fc on c.category_id = fc.category_id
                        INNER JOIN film f on f.film_id = fc.film_id
                        WHERE c.name = %(name)s
                        GROUP BY c.name
                     """, con=connection_sqlalchemy, params={"name": name})
    return df
