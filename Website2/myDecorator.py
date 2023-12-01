def check_information_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Check and replace empty values
        if not result['vendor']:
            result['vendor'] = 'No Vendor Found'
        if not result['title']:
            result['title'] = 'No Title Found'
        if not result['price']:
            result['price'] = '$0.00'
        if not result['img']:
            result['img'] = 'No Image URL Found'
        if not result['url']:
            result['url'] = 'No Product URL Found'

        return result

    return wrapper