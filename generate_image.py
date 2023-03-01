from pyunsplash import PyUnsplash


# Add your Unsplash API key here 
pu = PyUnsplash(api_key="3209302e-6fa8-4651-b1f9-28e8ac2c5854")


def image_generator(first_characteristic, second_characteristic):
    first_photo = pu.photos(type_='random', count=1, featured=True, query=first_characteristic)
    second_photo = pu.photos(type_='random', count=1, featured=True, query=second_characteristic)

    if first_photo and second_photo:
        return (list(first_photo.entries)[0].link_download, list(second_photo.entries)[0].link_download)

