import os

def load_pg_config():      
    # PostgreSQL connection config    

    pg_config = {}
    
    pg_config["host"] = os.environ.get('POSTGRES_HOST', 'localhost')
    pg_config["port"] = int(os.environ.get('POSTGRES_PORT', 5432))
    pg_config["database"] = os.environ.get('POSTGRES_DB', 'postgres')
    pg_config["user"] = os.environ.get('POSTGRES_USER', 'postgres')
    pg_config["password"] = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    
    return pg_config


def load_number_of_records():    
    return int(os.environ.get('NUMBER_OF_RECORDS', 10000))
  

def load_number_of_threads():     
    return int(os.environ.get('NUMBER_OF_THREADS', 10))


if __name__ == '__main__':
    
    pg_config = load_pg_config()
    print(pg_config)
    number_of_records = load_number_of_records() 
    print(number_of_records)
    number_of_threads = load_number_of_threads()
    print(number_of_threads)