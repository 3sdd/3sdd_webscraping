import os
import urllib.request
import xml.etree.ElementTree as ET
import argparse


def download_image(url,file_name):
    with urllib.request.urlopen(url) as response:
        with open(file_name,"wb") as f:
            f.write(response.read())



def download_images(image_folder,max_page,request_tags):
    i=0
    for page in range(0,max_page):
        #100 posts per request
        api_str="https://safebooru.org/index.php?page=dapi&s=post&q=index&pid={pid}&tags={tags}".format(pid=page,tags=request_tags.replace(" ","+"))

        with urllib.request.urlopen(api_str) as response:

            content=response.read()
            xml=ET.fromstring(content)

            for post in xml.iter("post"):
                file_url=post.get("file_url")
                file_name=os.path.basename(file_url)
                dst_path=os.path.join(image_folder,file_name)


                # rating=post.get("rating")
                # tags=post.get("tags")
                # print(i,":",file_name,",",rating,",",tags)
                print(i,":",file_name)
                download_image(file_url,dst_path)
                i+=1


def get_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("--image_folder",type=str,default="./safebooru_images")
    parser.add_argument("--max_page",type=int,default=1)
    parser.add_argument("--tags",type=str,default="face 1girl solo")
    return parser.parse_args()

if __name__=="__main__":
    args=get_arguments()

    
    os.makedirs(args.image_folder,exist_ok=True)

    download_images(args.image_folder,args.max_page,args.tags)

    
