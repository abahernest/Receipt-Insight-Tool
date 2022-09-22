# Receipt Insight Tool

## STEPS TO RUN THE APP LOCALLY

### APPROACH 1

1. Clone the repo and `cd` into the repo folder
2. Ensure Python and Pipenv are installed on your machine
3. Install dependencies by running 
```
>> pipenv shell
>> pipenv install
```
4. Setup postgres locally and create a database for the application
5. create a `.env` file that contains the necessary information found in `env.example`
6. Make database migrations. 
```
>> python manage.py migrate
```
7. Seed Default Delimiters
```
>> python manage.py loaddata default_delimiters
```
8. Start Application
```
>> python manage.py runserver
```

### APPROACH 2 (With Docker Compose)

1. Clone the appplication and `cd` into the repo folder

2. Run the command below to startup the postgres db as well as the api server
```
>> docker compose up
```

## TEST
```
>> python manage.py test
```

## POSTMAN DOCUMENTATION
[Postman Doc](https://documenter.getpostman.com/view/11044390/2s7YYu4hju)


## DATABASE TABLE RELATIONSHIPS

### TABLE 1: Document
    ```
        {
            name            --name of uploaded file
            description     --description of uploaded file (if provided)
        }
    ```

### TABLE 2: Blocks
    ```
        {
            document_id    --Foreign key to Document Table
            start_row      --Starting X-axis index of block
            start_col      --Starting Y-axis index of block
            end_row        --Ending X-axis index of block
            end_col        --Ending Y-axis index of block
        }
    ```

### TABLE 3: Delimiter
    ```
        {
            value       --JSON encoded string representation of the delimiter
            count       --Integer value of the minimum number of times the delimiter has to occur consequtively to be counted as delimiter.
        }
    ```
## IMPLEMENTATION & DESIGN

Initially I had 2 ways to implement this.

1. Read the contents of .txt file into a variable, then use regex functions to find the positions of the words and the delimeters.

2. Read the .txt file line-by-line using the readline() function in python. This sequence will produce the row index of the words in the file. Just need to find the column index. 

While traversing by rows, 

-  Find the start and end index of the delimiters. For example if delimiter value is `#` and count is `2`. Then Find the various indices of `##` in the word.
-  Merge these indices into one to give you the start and end indices of the delimiter. This approach will help us find delimiters hiding between words.
-  If the Word contains no delimiter, just traverse the word excluding the whitespaces and find the start and end index
-  For words that contains delimiter, for each delimier, find the indices of the words it bound to left and right by slicing from the delimiter's start index to the left and its end index to the right.


I decided to go ahead with the second approach because I would be able to capture multiple delimiters in a single line, as well as delimiters that occupy single lines

