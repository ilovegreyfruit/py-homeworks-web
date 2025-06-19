import requests

BASE_URL = 'http://127.0.0.1:5000/ads'


def create_ad():
    ad_data = {
        "title": "Сдаю квартиру",
        "description": "2-комнатная, метро рядом",
        "owner": "Мария"
    }
    r = requests.post(BASE_URL, json=ad_data)
    print(r.status_code, r.json())


def get_ad(ad_id):
    r = requests.get(f"{BASE_URL}/{ad_id}")
    print(r.status_code, r.json())


def update_ad(ad_id):
    updated_data = {
        "title": "Сдаю квартиру (обновлено)",
        "description": "Теперь с мебелью"
    }
    r = requests.put(f"{BASE_URL}/{ad_id}", json=updated_data)
    print(r.status_code, r.json())


def delete_ad(ad_id):
    r = requests.delete(f"{BASE_URL}/{ad_id}")
    print(r.status_code, r.json())


if __name__ == '__main__':
    create_ad()
    get_ad(1)
    update_ad(1)
    delete_ad(1)