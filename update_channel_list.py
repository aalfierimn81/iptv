import re
import os
import shutil
import requests
from PIL import Image

def add_menu (lista,html):
    menu=""
    for i in range (0,len(lista)):
        menu = menu + "<a href=\""+lista[i]+".html\"><li>"+lista[i]+"</li></a>"
    html = html + menu
    return html

def get_stream_link (string_link):
    sl=string_link.split('(')
    sl=sl[1]
    sl=sl[:len(sl)-1]
    return sl

def get_img_link (string_link):
    il=string_link.split("src=")
    il=il[1]
    il=il[1:len(il)-3]
    return il

def create_channel_folder(country, num, name, stream, img):
    #os.makedirs(str(num))
    root=os.getcwd()
    os.makedirs(os.getcwd()+"/"+country+"/channels/"+str(num))
    os.chdir(os.getcwd()+"/"+country+"/channels/"+str(num))
    # create link for stream
    filename=name.replace(" ", "")+".m3u"
    filename=name.replace("/", "")+".m3u" # teleagrigento/magictv
    f=open(filename,"w+")
    f.write("#EXTM3U\n")
    f.write("#EXTVLCOPT:http-user-agent=HbbTV/1.6.1\n")
    f.write(stream)
    f.close
    # create channel icon
    save_as=img.split('/')
    response = requests.get(img, headers = {'User-agent': 'your bot 0.1'}) # to avoid HTTP 429 error
    with open(save_as[-1], 'wb') as file:
        file.write(response.content)
    file=save_as[-1].split('.')
    fext = file[-1]
    fname = ""
    for i in range (0, len(file)-1):
        fname = fname+file[i]+"."
    fname = fname[:len(fname)-1]
    os.rename(fname+'.'+fext, name.replace(" ", "").replace("/","")+'.'+fext)
    if (fext=="jpg" or fext=="jpeg"):
        im = Image.open(name.replace(" ", "").replace("/","")+'.'+fext)
        im.save(name.replace(" ", "").replace("/","")+'.png')
    os.chdir(root)

def init_tv(country):
    channel_no = 1
    f = open("IPTV-master/lists/"+country+".md", "r")  
    linelist = f.readlines()
    shutil.rmtree(os.getcwd()+"/"+country)
    for i in range (0, len(linelist)):
        if (linelist[i][0] == "|" and linelist[i][0:7] != "| #   |" and linelist[i][0:7] != "|:---:|" and linelist[i][0:7] != "|  #  |" and linelist[i][0:6] != "| #  |" and linelist[i][0:6] != "|:--:|"):
            data = linelist[i].split('|')        
            data[2]=re.sub(r'[^\x00-\x7f]',r' ',data[2]).strip()       
            data[3]=re.sub(r'[^\x00-\x7f]',r' ',data[3]).strip()
            stream_link = get_stream_link(data[3])
            data[4]=re.sub(r'[^\x00-\x7f]',r' ',data[4]).strip()
            img_link=get_img_link(data[4])
            create_channel_folder (country,channel_no, data[2], stream_link, img_link)
            channel_no = channel_no + 1
    f.close()

    web_path = "file:///var/www/html/tv"
    local_path = country + "/channels/"
    web_path = web_path + "/" + local_path

    thtml = open("html_template/template_1_country.html", "r").read()
    
    page_web_code = thtml + "<h1>" + country + "</h1>"
    
    thtml = open("html_template/template_2_country.html", "r").read()

    page_web_code = page_web_code + thtml

    page_web_code = page_web_code + "<body> \n"

    page_web_code = page_web_code + "<table border=\"1\"> \n"
    
    for i in range (1, channel_no):
        page_web_code = page_web_code + "<tr> \n"
        files = os.listdir(os.getcwd()+"/"+country+"/channels/"+str(i)) 
        img_file = ""
        stream_file = ""
        for j in range (0, len(files)):
            if (files[j][-3:]=="png"):
                img_file = files[j]
            if (files[j][-3:]=="m3u"):
                stream_file = files[j]
        page_web_code = page_web_code + "<td>" + stream_file[:-4] + "</td>"
        page_web_code = page_web_code + "<td> <img src=\"" + local_path + str(i)+"/"+img_file+ "\" class=\"responsive\"> </td>"
        page_web_code = page_web_code + "<td>" "<form id = \"submitForm\" action=\"cambia_canale.php\" method=\"post\">" + "<input type=\"hidden\" name=\"canale\" value=\""+local_path+str(i)+"/"+stream_file+"\"> <button type=\"submit\" class=\"button\"  name=\"submit\">Guarda</button> </form>"
        page_web_code = page_web_code + "</tr> \n"

    thtml = open("html_template/template_3_country.html", "r").read()

    page_web_code = page_web_code + thtml

    fhtml = open(country+".html", "w")
    fhtml.write(page_web_code)
    fhtml.close()

def create_index (arr):
    thtml = open("html_template/template_inizio_index.html", "r").read()
    
    fhtml = open("index.html", "w")
    index_page_code = thtml
    
    index_page_code = add_menu(arr,index_page_code)

    thtml = open("html_template/template_fine_index.html", "r").read()
    index_page_code = index_page_code + thtml
    fhtml.write(index_page_code)
    fhtml.close()

countries = []
countries.append("germany")
countries.append("italy")
countries.append("zz_news_en")

for i in range (0,len(countries)):
    init_tv(countries[i])

create_index(countries)



