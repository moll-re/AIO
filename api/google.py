import googlesearch


def query(params):
    param_string = ""
    for word in params:
        param_string += word + "+"
    param_string = param_string[:-1]
    search_url = "https://google.com/search?q=" + param_string

    try:
        res = googlesearch.search(param_string.replace("+"," ") ,num=5,start=0,stop=5)
        send_string = "Google search for <b>" + param_string.replace("+"," ") + "</b>:\n"
        for url in res:
            send_string += url + "\n\n"
        send_string += "Search url:\n" + search_url
    except:
        send_string = "Search url:\n" + search_url

    return send_string
