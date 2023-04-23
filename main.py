import asyncio
from webscraper import WebScraper

async def main():
    query = input("Enter your search: ")
    search_engines = ["google", "bing", "yahoo", "yandex"]
    
    scrapers = [WebScraper(query, search_engine) for search_engine in search_engines]
    results = await asyncio.gather(*(scraper.get_results() for scraper in scrapers))

    for search_engine, result in zip(search_engines, results):
        print(f"\Results of {search_engine.capitalize()}:")
        if "error" in result:
            print(result["error"])
        else:
            for i, link in enumerate(result, start=1):
                print(f"[{i}] => {link}\n")

if __name__ == "__main__":
    asyncio.run(main())
