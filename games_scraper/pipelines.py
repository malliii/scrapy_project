from itemadapter import ItemAdapter
import sqlite3


# each item is processed by the pipeline
class GamesScraperPipeline:
    def process_item(self, item, spider):
        # Changed scores to NA if 'tbd'.
        item["user_score"] = "NA" if item["user_score"] == "tbd" else item["user_score"]
        item["meta_score"] = "NA" if item["meta_score"] == "tbd" else item["meta_score"]
        # Remove new line character and trailing whitespaces.
        item["summary"] = "NA" if item["summary"] is None else item["summary"]
        item["summary"] = item["summary"].replace("\n", "").strip()
        item["product_genre"] = " ".join(item["product_genre"])
        return item


class GamesScraperDBPipeline:
    def __init__(self):
        ## Create/Connect to database
        self.con = sqlite3.connect("metacritic.db")

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()

        ## Create quotes table if none exists
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS games(
                title TEXT,
                meta_score TEXT,
                user_score TEXT,
                platform TEXT,
                release_date TEXT,
                summary TEXT,
                product_genre TEXT
            )
            """
        )

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(
            """
            INSERT INTO games (title, meta_score, user_score, platform, release_date, summary, product_genre) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                item["title"],
                str(item["meta_score"]),
                str(item["user_score"]),
                item["platform"],
                item["release_date"],
                item["summary"],
                item["product_genre"],
            ),
        )

        ## Execute insert of data into database
        self.con.commit()
        return item
