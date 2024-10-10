import logging
import psycopg2 as pg

class PostgresLogHandler(logging.Handler):
    def __new__(cls, logger_name, job_id, table, db_config):
        try:
            instance = super(PostgresLogHandler, cls).__new__(cls)
            instance.__init__(logger_name, job_id, table, db_config)
            return instance.logger
        except Exception as e:
            logging.error(f"Error creating PostgresLogHandler: {e}")
            return None

    def __init__(self, logger_name, job_id, table, db_config):
        try:
            if '' in [logger_name, job_id, table] or None in [logger_name, job_id, table]:
                raise Exception("Invalid parameters")
            logging.Handler.__init__(self)
            self.connection = pg.connect(**db_config)
            self.cursor = self.connection.cursor()
            self.logger_name = logger_name
            self.table = table
            self.job_id = job_id
            self._create_table_if_not_exists()
            self.logger = self._setup_logging()
        except Exception as e:
            logging.error(f"Error setting up PostgresLogHandler: {e}")

    def _create_table_if_not_exists(self):
        try:
            self.cursor.execute("set time zone 'UTC'")
            self.cursor.execute(f"""
            create table if not exists {self.table} (
                id serial primary key,
                created_at timestamptz default now(),
                name varchar(255),
                levelname varchar(50),
                message text,
                job_id varchar(255) not null
            )""", (self.table,))
            self.connection.commit()
        except Exception as e:
            logging.error(f"Error creating table {self.table}: {e}")

    def _setup_logging(self):
        try:
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(logging.DEBUG)

            self.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.setFormatter(formatter)

            logger.addHandler(self)
            logger.info(f"Logger: {self.logger_name} setup with job_id: {self.job_id}")

            return logger
        except Exception as e:
            logging.error(f"Error setting up logging: {e}")        

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.cursor.execute(f"""
            insert into {self.table}
            (name, levelname, message, job_id) 
            values 
            (%s, %s, %s, %s)
            """, (record.name, record.levelname, log_entry, self.job_id))
            self.connection.commit()
        except Exception as e:
            logging.error(f"Error emitting log record: {e}")

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            logging.Handler.close(self)
        except Exception as e:
            logging.error(f"Error closing connection: {e}")