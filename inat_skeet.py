from pyinaturalist import *
from random import randrange
import requests
from atproto import Client, client_utils, models
import os
from PIL import Image


# Settings
per_page = 1
user_id = os.environ['INAT_ID']
user_id_num = os.environ['INAT_ID_NUMBER']
my_handle = os.environ['BSKY_HANDLE']
my_password = os.environ['BSKY_PASSWORD']

# Get number of observations for pagination
num_obs = get_user_by_id(user_id_num)

def main() -> None:
    client = Client()
    client.login(my_handle, my_password)
    observation = download_images()
    details = observation[1]
    paths = observation[0]
    fullname = details[1]
    uri = details[2]
    observed_on = details[3]
    place_guess = details[4]

    images = []
    for path in paths:
        print(os.path.getsize(path))
        if os.path.getsize(path) >= 1000000: # This might be wrong! bsky limits file upload sizes.
            path = recompress_image(path)
            with open(path, 'rb') as f:
                images.append(f.read())
        else:
            with open(path, 'rb') as f:
                images.append(f.read())

    client.send_images(
        text=client_utils.TextBuilder().text(fullname+'\n\n'+observed_on+'\n'+place_guess+'\n').link(uri, uri),
        images=images,
    )

def getobs(user_id, per_page):
        page = randrange(0, int(num_obs['observations_count']/per_page))
        observations = get_observations(user_id=user_id, page=page, per_page=per_page)
        my_observations = Observation.from_json_list(observations)
        photo_urls = []
        for photo in my_observations[0].photos:
           photo_urls.append(photo.url.replace("square", "original"))
        fullname = my_observations[0].taxon.full_name
        uri = my_observations[0].uri
        observed_on = str(my_observations[0].observed_on)
        place_guess = my_observations[0].place_guess
        inat_id = my_observations[0].id
        return(photo_urls, fullname, uri, observed_on, place_guess, inat_id)

def download_images():
    img_index = 0
    photo_names = []
    observation = getobs(user_id, per_page)
    for img_url in observation[0]:
        img_index = img_index+1
        data = requests.get(img_url).content
        filename = str(getobs(user_id, per_page)[5])+str('_'+str(img_index))+'.jpg'
        f = open(filename,'wb')
        f.write(data) 
        f.close()
        photo_names.append(filename)
    return(photo_names, observation)

def recompress_image(filepath):
    picture = Image.open(filepath) 
    print(filepath)
    # Save the picture with desired quality 
    # To change the quality of image, 
    # set the quality variable at 
    # your desired level, The more  
    # the value of quality variable  
    # and lesser the compression 
    new_filename = "Compressed_"+filepath
    picture.save(new_filename,  
                 optimize = True, 
                 subsampling=0, 
                 quality = 75) 
    return(new_filename)


if __name__ == '__main__':
    main()