from itemadapter import ItemAdapter


# each item is processed by the pipeline
class GamesScraperPipeline:
    def process_item(self, item, spider):
        # Changed scores to NA if 'tbd'.
        item["user_score"] = "NA" if item["user_score"] == "tbd" else item["user_score"]
        item["meta_score"] = "NA" if item["meta_score"] == "tbd" else item["meta_score"]
        # Remove new line character and trailing whitespaces.
        item["summary"] = item["summary"].replace("\n", "").strip()
        return item
