from get_isi_berita import GetIsiBerita

NAMA_FILE = "links.txt"

with open(NAMA_FILE, "r") as f:
    all_links = f.readlines()

list_berita = []
count = 1
for link in all_links:
    tmp_list = []
    isi_berita = GetIsiBerita().request_web(link)
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {count}/{len(isi_links)}")
    count += 1
    tmp_list.append(link)
    tmp_list.append(isi_berita)
    list_berita.append(tmp_list)
    
df_link_berita = pd.DataFrame(list_berita, columns=["LINK", "ISI BERITA"])
print(df_link_berita)
df_link_berita.to_excel("df_links_isi_berita.xlsx")
