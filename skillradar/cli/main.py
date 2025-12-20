import json
from skillradar.core.fetch.hh import HHRegionFetcher
from skillradar.core.fetch.hh import HHFetcher


def main():
    # config = parse_args()

    fetcher = HHRegionFetcher() 
    
    print(fetcher.fetch())
    # pipeline = Pipeline(fetcher)

    # pipeline.run(config) 


if __name__ == "__main__":
    main()
