Bballstats
==========

bballstats is a Django app that fetch data from https://stats.nba.com/stats/. For each new endpoint you can define a custom class inheriting the Endpoint class. see: https://github.com/robnanola/bballstats/blob/main/endpoints/leaders.py for the sample implementation.


Quick start
-----------

1. Clone the bballstats repository:

    ```
    git clone https://github.com/robnanola/bballstats.git
    ```

2. Assuming you already have docker installed on your machine, run the ff commands:

    ```
    docker-compose build
    docker-compose up
    ```


3. Run the inital database migration:

    ```
    docker-compose exec app python manage.py migrate  
    ```


4. Load the data from the NBA stats API

    ```
    docker-compose exec app python manage.py fetch_leaders_data
    ```


5. The web application can be accessed via http://127.0.0.1:8000/
