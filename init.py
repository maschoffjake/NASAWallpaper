import urllib.request
from bs4 import BeautifulSoup
import os.path

"""
This program grabs all the images of the day in NASA's image of the day archive,
and then exports it into a local folder. Fun little script so you can set these images
as your background if you want. 

Author: Jake Maschoff
Last Update: 2/11/18
Version: 1.0
"""

# If any of the webpages are unable to be downloaded initially, add them to a list to try downloading
# them later
webpages_to_redownload = []

# If the webpages download correctly, but the images don't add them to this list. Try re-downloading the images
# after going through all the webpages
images_to_redownload = []

# Where you want to place all of the image files
filename_placement = "/Users/jakemaschoff/Documents/Out Of This World Pix/"

# NASA's picture of the day archive
url_to_grab = "https://apod.nasa.gov/apod/archivepix.html"

# Grab the bytes read in from the URL
html_doc = urllib.request.urlopen(url_to_grab)
html_bytes = html_doc.read()

# Let BeautifulSoup4 parse the
soup = BeautifulSoup(html_bytes, 'html.parser')

# Grab all the links in the html so we can go into the nested HTML files to grab the images
for link in soup.find_all('a'):
    link_string = link.get('href')
    if link_string.startswith("ap") and link_string.endswith(".html"):

        # Grab the nested html file which contains the actual JPEG image
        nested_html = "https://apod.nasa.gov/apod/" + link_string

        image_url = "https://apod.nasa.gov/apod/"

        # Try opening this nested HTML page. If unable, add it to a list to try
        # downloading again later
        try:
            html_doc = urllib.request.urlopen(nested_html)
        except Exception as e:
            print("Unable to download " + nested_html + ", will add it to a list to"
                                                        "try later\n"
                                                        "Got error: " + str(e))
            webpages_to_redownload.append(nested_html)
            continue

        # Grab the bytes read in from the URL
        html_bytes = html_doc.read()

        # Let BeautifulSoup4 parse the file
        new_soup = BeautifulSoup(html_bytes, 'html.parser')

        # Grab all of the links in this nested HTML file
        for nested_link in new_soup.find_all('a'):
            nested_link_string = nested_link.get('href')

            # If the string doesn't contain anything, just continue
            if nested_link_string == None:
                continue

            # If the link is an image and a jpeg, download it!
            if nested_link_string.startswith("image") and nested_link_string.endswith(".jpg"):

                # Add the img path to the absolute path name
                image_url += nested_link_string

                # When downloading the image, use the filename path and then the actual name of the image.
                # The actual name of the image starts 10 characters into the img path
                file_name = filename_placement + nested_link_string[10:]

                # If the image is already downloaded, don't redownload it!
                if os.path.exists(file_name):
                    print("Already downloaded : " + image_url)
                    continue

                print(image_url)


                # Try to download the img, or print an error message
                try:
                    urllib.request.urlretrieve(image_url, file_name)
                except Exception as e:
                    print("Unable to download: " + image_url + ", will try and re-download later"
                                                               "\nGot error : " + str(e))
                    images_to_redownload.append(image_url)

                # Reset the image_url back to the only the absolute path, just in case the embedded
                # html file contains more than one jpg image
                image_url = "https://apod.nasa.gov/apod/"


# RE-TRY DOWNLOADING WEBPAGES IF ERRORS
# Will try re-downloading the webpages that were unable to download earlier
# in the script
for link in webpages_to_redownload:
    try:
        html_doc = urllib.request.urlopen(nested_html)
    except Exception as e:
        print("Unable to download " + nested_html + ", try downloading manually or"
                                                    "re-running the script\n"
                                                    "Got error: " + str(e))
        continue
    html_bytes = html_doc.read()

    # Let BeautifulSoup4 parse the file
    new_soup = BeautifulSoup(html_bytes, 'html.parser')

    for nested_link in new_soup.find_all('a'):
        nested_link_string = nested_link.get('href')

        # If the string doesn't contain anything, just continue
        if nested_link_string == None:
            continue

        # If the link is an image and a jpeg, download it!
        if nested_link_string.startswith("image") and nested_link_string.endswith(".jpg"):

            # Add the img path to the absolute path name
            image_url += nested_link_string
            print(image_url)

            # When downloading the image, use the filename path and then the actual name of the image.
            # The actual name of the image starts 10 characters into the img path
            file_name = filename_placement + nested_link_string[10:]

            # Try to download the img, or print an error message
            try:
                urllib.request.urlretrieve(image_url, file_name)
                webpages_to_redownload.remove(link)
            except Exception as e:
                print("Unable to download: " + image_url + ", will try and re-download later"
                                                           "\nGot error : " + str(e))
                images_to_redownload.append(image_url)

            # Reset the image_url back to the only the absolute path, just in case the embedded
            # html file contains more than one jpg image
            image_url = "https://apod.nasa.gov/apod/"


# RE-TRY DOWNLOADING THE IMAGES
# Try downloading the actual images that were unable to download earlier in the script
for image_path in images_to_redownload:
    # Add the img path to the absolute path name
    image_url += nested_link_string
    print(image_url)

    # When downloading the image, use the filename path and then the actual name of the image.
    # The actual name of the image starts 10 characters into the img path
    file_name = filename_placement + nested_link_string[10:]

    # Try to download the img, or print an error message
    try:
        urllib.request.urlretrieve(image_url, file_name)
        images_to_redownload.remove(image_path)
    except Exception as e:
        print("Unable to download: " + image_url + ", try downloading manually or re-run script"
                                                   "\nGot error : " + str(e))

    # Reset the image_url back to the only the absolute path, just in case the embedded
    # html file contains more than one jpg image
    image_url = "https://apod.nasa.gov/apod/"

print("Did not download these webpages:\n")
for link in webpages_to_redownload:
    print(link)

print("Did not download these images:\n")
for image_path in images_to_redownload:
    print(image_path)