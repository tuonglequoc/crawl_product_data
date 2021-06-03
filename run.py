import json

import requests

from bs4.element import NavigableString
from bs4 import BeautifulSoup as bs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import insert
from sqlalchemy.exc import IntegrityError

from models import Product
from config import DATABASE_URL, COUNTRY_OF_ORIGIN, REMARKS, LIMIT


BASE_URL = "https://www.matsukiyo.co.jp"
QUERY_PRODUCT = "po[]={category}&o={offset}&limit={limit}&sort=id"


engine = create_engine(DATABASE_URL)
session_local = sessionmaker(engine)


def get_data_from_url(url: str, params: dict = None):
    """Fetch data from an enpoint url"""
    params = params or {}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.text
    else:
        raise Exception(f"Request failed. Status: {res.status_code}: {res.text}")


def get_bs_data(html_text: str):
    return bs(html_text, "html.parser")


def get_categories(bs_home_data: bs):
    bs_categories = bs_home_data.find(text="カテゴリでさがす").parent.find_next().children
    return (
        {"href": cat_tag.get("href"), "name": cat_tag.get_text()}
        for cat_tag in (a.find("a") for a in bs_categories if a.find("a") != -1)
    )


def first_get_product_ids(bs_cat_data: bs):
    products = json.loads(bs_cat_data.find(id="extecViewParams").get("value"))
    return (item["id"] for item in products["ecommerce"]["impressions"])


def get_products_list(category: str):
    offset = 0
    while True:
        data = get_data_from_url(
            BASE_URL + "/store/api/search/next",
            {
                "query": QUERY_PRODUCT.format(
                    category=category, offset=offset, limit=LIMIT
                )
            },
        )
        try:
            products = json.loads(json.loads(data)["extecViewParams"])
        except:
            break
        yield (
            {"id": item["id"], "price": item["price"]}
            for item in products["ecommerce"]["impressions"]
        )
        offset += LIMIT


def get_products(products, category_name):
    for product in products:
        bs_product_data = get_bs_data(
            get_data_from_url(BASE_URL + "/store/online/p/" + product["id"])
        )
        product_result = {}
        product_result["barcode"] = int(product["id"])
        product_result["product_name"] = (
            bs_product_data.find(class_="goodsBox").find("h3").get_text()
        )
        product_result["category"] = category_name
        product_result["country_of_origin"] = COUNTRY_OF_ORIGIN
        product_result["link"] = BASE_URL + "/store/online/p/" + product["id"]
        product_result["thumbnail"] = BASE_URL + bs_product_data.find(
            class_="popBxslider"
        ).find("img").get("src")
        product_result["price"] = int(product["price"])
        product_result["status"] = True
        product_result["description"] = "\n".join(
            line
            for line in bs_product_data.find(text="商品詳細").parent.find_next().contents
            if type(line) is NavigableString
        )
        product_result["remarks"] = REMARKS
        yield product_result


def insert_to_database(product: dict):
    stmt = insert(Product).values(**product)
    with session_local.begin() as session:
        try:
            session.execute(stmt)
        except Exception as e:
            raise e
    print(
        "Inserted product {} from category {}".format(
            product["barcode"], product["category"]
        )
    )


def main():
    bs_home_data = get_bs_data(get_data_from_url(BASE_URL + "/store/online"))
    categories = get_categories(bs_home_data)
    for cat in categories:
        # bs_cat_data = get_bs_data(get_data_from_url(BASE_URL + cat["href"]))
        # first_ids = first_get_product_ids(bs_cat_data)
        products_list = get_products_list(cat["name"])
        for products in products_list:
            try:
                product_data = get_products(products, cat["name"])
                for product_item in product_data:
                    insert_to_database(product_item)
            except IntegrityError:
                break
            except Exception as e:
                print("WARNING: {}".format(str(e)))
                continue
        print("Got all products in category {}".format(cat["name"]))


if __name__ == "__main__":
    main()
