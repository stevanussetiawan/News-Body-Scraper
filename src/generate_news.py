import pandas as pd
from news_content_fetcher import NewsContentFetcher

def generate_news_to_excel():
    # Load the Excel file and extract unique links
    df = pd.read_excel(r"data/testing_crawling_03_05_2024.xlsx", "data_melanggar").head(10)
    isi_links = df["LINK"].unique().tolist()
    
    # Initialize the content fetcher
    content_fetcher = NewsContentFetcher()
    list_berita = []
    
    # Iterate over the links and fetch their content
    for count, link in enumerate(isi_links, 1):
        isi_berita = content_fetcher.fetch_web_content(link)        
        list_berita.append([link, isi_berita])
    
    # Create a DataFrame from the results and save to an Excel file
    df_link_berita = pd.DataFrame(list_berita, columns=["LINK", "ISI BERITA"])
    print(df_link_berita)
    df_link_berita.to_excel("df_links_isi_berita.xlsx", index=False)

if __name__ == "__main__":
    generate_news_to_excel()
