All .csv files have been uploaded into postgresql and combined on title using the following query:

SELECT *
FROM "PC"
FULL OUTER JOIN "Playstation 4" ON PC.title = "Playstation 4".title
FULL OUTER JOIN "Playstation 5" ON PC.title = "Playstation 5".title
FULL OUTER JOIN "XBOX" ON PC.title = "XBOX".title
FULL OUTER JOIN "NINTENDO" ON PC.title = "Nintendo".title;