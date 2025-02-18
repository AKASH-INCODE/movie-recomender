import requests
res=requests.get(rf'https://www.omdbapi.com/?i={x}&apikey=d7a5ccec')

# https://www.omdbapi.com/?i=tt3896198&apikey=d7a5ccec
print(res.json()["Poster"])