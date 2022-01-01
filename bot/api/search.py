import duckduckpy

class WebSearch():
    def __init__(self):
        self.search = duckduckpy.query

    def get_result(self, query):
        try:
            res = []
            response = self.search(query, container = "dict")["related_topics"]
            for r in response:
                if "text" in r:
                    res.append({
                        "text" : r["text"],
                        "url": r["first_url"]
                        })
        except:
            res = ["Connection error"]
        return res

# TODO: this api has more potential. Extract images or quick facts!