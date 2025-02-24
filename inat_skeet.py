from pyinaturalist import *
from random import randrange
import requests
from atproto import Client, client_utils, models
import os
from PIL import Image
import image_understanding_lib as glib

# Settings
per_page = 1
user_id = os.getenv('INAT_ID')
user_id_num = os.getenv('INAT_ID_NUMBER')
my_handle = os.getenv('BSKY_HANDLE')
my_password = os.getenv('BSKY_PASSWORD')

prompt = "Please provide an extemely brief visual description of this image. This image contains an organism named "

# Get number of observations for pagination
num_obs = get_user_by_id(user_id_num)

def main() -> None:
    obs_details()

def ai_alt_text(path, fullname):
    image_bytes = glib.get_bytes_from_file(path)
    response = glib.get_response_from_model(
        prompt_content=prompt+fullname, 
        image_bytes=image_bytes,
    )
    return(response)

def resize_images(paths):
    images = []
    path = paths
    if os.path.getsize(path) >= 900000: # This might be wrong! bsky limits file upload sizes.
        path = recompress_image(path)
        return(path)
    else:
        images.append(path)
        return(path)

def post_images(fullname, observed_on, place_guess, uri, paths, iconic_taxon_name, quality_grade):
    images = []
    alt_text = []
    for path in paths:
        alt_text.append(ai_alt_text(path, fullname))
        with open(path, 'rb') as f:
            images.append(f.read())
    print(alt_text)
    client = Client()
    client.login(my_handle, my_password)
    # This is horrible, I need to unfuck this completely
    if iconic_taxon_name == 'Insecta':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('insects','insects').text('\n').tag('inverts','inverts').text('\n').tag('bugs','bugs').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Animalia':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('animals','animals').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Aves':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('birds','birds').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Amphibia':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('amphibians','amphibians').text('\n').tag('herps','herps').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Reptilia':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('reptiles','reptiles').text('\n').tag('herps','herps').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Mammalia':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('mammals','mammals').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Actinopterygii':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('fish','fish').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Mollusca':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('molluscs','molluscs').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Arachnida':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('arachnids','arachnids').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Plantae':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('plants','plants').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Fungi':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('fungi','fungi').text('\n').tag('mycology','mycology').text('\n').tag('mushrooms','mushrooms').text('\n').tag('fungifriends','fungifriends').text('\nWarning! AI generated alt text.')
    elif iconic_taxon_name == 'Protozoa':
        text=client_utils.TextBuilder().text(fullname).text('\n\n').text('Quality grade: '+quality_grade+'\n').text(observed_on).text('\n').text(place_guess).text('\n').link(uri, uri).text('\n\n').tag('macrophotography','macrophotography').text('\n').tag('nature','nature').text('\n').tag('inaturalist','inaturalist').text('\n').tag(iconic_taxon_name, iconic_taxon_name).text('\n').tag('Protozoa','Protozoa').text('\nWarning! AI generated alt text.')
    else:
        pass
    client.send_images(
        text=text, images=images, image_alts=alt_text,)
    
    # 🤮🤮🤮🤮🤮🤮🤮🤮

def getobs(user_id, per_page):
        page = randrange(0, int(num_obs['observations_count']/per_page))
        observations = get_observations(user_id=user_id, page=page, per_page=per_page)
        my_observations = Observation.from_json_list(observations)
        # Lets pull single observations by ID
        inat_ids = []
        for inat_id in my_observations:
            inat_ids.append(inat_id.id)
        return(inat_ids)

def obs_details():
    obs = getobs(user_id, per_page)
    for id in obs:
        observation = get_observations_by_id(id)['results'][0]
        photo_urls = []
        for photo in observation['photos']:
            url = photo['url']
            photo_urls.append(url.replace("square", "original"))
    
        # Extract details
        try:
            taxon_name = str(observation['taxon']['name'])
        except:
            taxon_name = ' '
        try:
            preferred_common_name = str(observation['taxon']['preferred_common_name'])
        except:
            preferred_common_name = ' '
        try:
            iconic_taxon_name = str(observation['taxon']['iconic_taxon_name'])
        except:
            iconic_taxon_name = ' '
        try:
            quality_grade = observation['quality_grade']
        except:
            quality_grade = ' '
        fullname = taxon_name+' - '+preferred_common_name
        uri = observation['uri']
        observed_on = str(observation['observed_on'])
        place_guess = observation['place_guess']
        inat_id = observation['id']
        images = download_images(inat_id, photo_urls)
        # Done extracting
    
        post_images(fullname, observed_on, place_guess, uri, images, iconic_taxon_name, quality_grade)

def download_images(id, photo_urls):
    img_index = 0
    photo_names = []
    observation = id
    for img_url in photo_urls:
        data = requests.get(img_url).content
        filename = str(id)+str('_'+str(img_index))+'.jpg'
        img_index = img_index+1
        f = open(filename,'wb')
        f.write(data)
        f.close()
        photo_names.append(filename)
    paths = []
    for path in photo_names:
        paths.append(resize_images(path))
    return(paths)

def recompress_image(filepath):
    picture = Image.open(filepath) 
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
                 quality = 70) 
    return(new_filename)


if __name__ == '__main__':
    main()
