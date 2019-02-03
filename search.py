import random
from google_images_search import GoogleImagesSearch

# return path to image recieved from search
def search():
    f = open('GoogleCustomSearchApiKey.txt')
    KEY = f.readline()[:-1]
    CX = f.readline()[:-1]
    gis = GoogleImagesSearch(KEY, CX)

    adjectives = [line[:-1] for line in open('adjectives.txt', 'r')]
    nouns = [line[:-1] for line in open('nouns.txt', 'r')]
    visited = [line[:-1] for line in open('AlreadyDone.txt', 'r')]

    searchPass = 1

    while True:
        print "Pass: " + str(searchPass)
        query = "%s %s" % (adjectives[random.randint(0, len(adjectives) - 1)], nouns[random.randint(0, len(nouns) - 1)])
        print "Generating Query"
        print "Query: " + query

        print "Forming Search Parameters"
        search_params = {
            'q': query,
            'num': 10,
            'safe': 'off',
            'fileType': 'png',
            'imgType': 'photo',
            'searchType': 'image',
        }
        print "Initiating Search"
        gis.search(search_params=search_params)
        print "Storing results"
        results = gis.results()
        print "Processing Results"
        if len(results) > 0:
            for i in range(len(results)-1, -1, -1):
                fileName = gis.results()[i].url[gis.results()[i].url.rfind('/')+1:]
                if fileName in visited:
                    del results[i]

            if len(results) > 0:
                index = random.randint(0, len(results) - 1)
                fileName = results[index].url[results[index].url.rfind('/')+1:]
                visited.append(fileName)
                results[index].download('images')
                f = open('AlreadyDone.txt', 'w')
                toWrite = ""
                for term in visited:
                    toWrite += term + "\n"
                f.write(toWrite)
                return 'images/' + fileName
        searchPass += 1

def main():
    search()

if __name__ == "__main__":
    main()
