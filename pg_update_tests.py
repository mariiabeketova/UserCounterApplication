import psycopg2
import threading
import time
import logging
import config #import load_config
 

def recreate_table(pg_config):
        # Recreate user_counter table and populate it with values
    try:
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS user_counter")
                cursor.execute("CREATE TABLE user_counter (user_id integer not null, counter integer not null, version integer null)")
                cursor.execute("INSERT INTO user_counter (user_id, counter, version) VALUES(1,1,0)")
        logging.info('Table user_counter has been recreated')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)            

def upd_func_lost_update(pg_config, number_of_records):
        # Lost-update test
    try:
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor() as cursor:
                for _ in range(number_of_records):
                    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1") 
                    counter = cursor.fetchone()[0]
                    counter = counter + 1
                    cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))   
                    conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
def upd_func_inplace_update(pg_config, number_of_records):
        # In-place update test
    try:
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor() as cursor:
                for _ in range(number_of_records):
                    cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s", (1,))   
                    conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def upd_func_row_level_locking(pg_config, number_of_records):
        # Row-level locking test
    try:
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor() as cursor:
                for _ in range(number_of_records):
                    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE") 
                    counter = cursor.fetchone()[0]
                    counter = counter + 1
                    cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))   
                    conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
def upd_func_optimistic_concurrency_control(pg_config, number_of_records):
        # Optimistic concurrency control test
    try:
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor() as cursor:
                for _ in range(number_of_records):
                    while (True):
                        cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1") 
                        (counter, version)  = cursor.fetchone()
                        counter = counter + 1
                        cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s and version = %s", (counter, version + 1, 1, version))   
                        conn.commit()
                        count = cursor.rowcount
                        if (count > 0): break
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def last_updated_value(pg_config):
        # Get last updated COUNTER value
    try:
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1") 
                counter = cursor.fetchone()[0]
                logging.info(f"LAST counter value = {counter}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)  
        
def updates_performance_calculations(upd_func, pg_config, number_of_records, number_of_threads):
        # Test updates with upd_fun

    # Recreate user_counter table at the beggining of each test
    recreate_table(pg_config) 
    
    start_time = time.time()
    
    # Create threads to execute the update statement concurrently
    threads = []
    for _ in range(number_of_threads):
        thread = threading.Thread(target=upd_func, args=(pg_config, number_of_records))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        
    end_time = time.time()
    
    # Duration of the updates
    delta = end_time - start_time
    logging.info(f"DELTA(seconds) = {delta}")
    
    # Get last updated COUNTER value at the end of the each test
    last_updated_value(pg_config)
    

if __name__ == '__main__':
    
    # Set logging configurations
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
    
    # Set config variables
    pg_config = config.load_pg_config()
    number_of_records = config.load_number_of_records()    
    number_of_threads = config.load_number_of_threads()
    
    logging.info("-----------------------------")
    logging.info("TABLE UPDATE TESTS:")
    logging.info(f"Number of updates = {number_of_records}")
    logging.info(f"Number of threads = {number_of_threads}")
    logging.info("-----------------------------")
    
    #1 Lost-update
    logging.info("--- 1. Lost-update test ---")
    upd_func = upd_func_lost_update
    updates_performance_calculations(upd_func, pg_config, number_of_records, number_of_threads)
    
    #2 In-place update
    logging.info("--- 2. In-place update test ---")
    upd_func = upd_func_inplace_update
    updates_performance_calculations(upd_func, pg_config, number_of_records, number_of_threads)

    #3 Row-level locking
    logging.info("--- 3. Row-level locking test ---")
    upd_func = upd_func_row_level_locking
    updates_performance_calculations(upd_func, pg_config, number_of_records, number_of_threads)
    
    #4 Optimistic concurrency control
    logging.info("--- 4. Optimistic concurrency control test ---")
    upd_func = upd_func_optimistic_concurrency_control
    updates_performance_calculations(upd_func, pg_config, number_of_records, number_of_threads)