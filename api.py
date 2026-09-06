import requests




def make_request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # выбросит ошибку если статус кода не 2хх (например 404, 500 и тд..)
        return response.json()

    except requests.exceptions.Timeout:
        print('Сервер не ответил за 10 секунд.')
        raise

    except requests.exceptions.HTTPError:
        print('Не удалось получить данные от сервера.')
        raise

    except requests.exceptions.RequestException:
        print('Произошла ошибка при выполнении HTTP-запроса.')
        raise