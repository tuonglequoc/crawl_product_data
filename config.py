DB_HOST = "localhost"
DB_NAME = "matsukiyo"
DB_USER = "user"
DB_PASSWORD = "password"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)


COUNTRY_OF_ORIGIN = "Japan"
REMARKS = "Auto crawler"
LIMIT = 30  # Max 30
