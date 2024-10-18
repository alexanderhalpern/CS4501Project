TABLE_STRUCTURES = '''

CREATE TABLE IF NOT EXISTS GreaterManchesterCrime (
	CrimeID	VARCHAR(50) PRIMARY KEY ,
	CrimeTS	TIMESTAMP,
	Location	TEXT,
	LSOA	TEXT,
	Type	TEXT,
	Outcome	TEXT,
	theGeom	GEOMETRY
);
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('0F:67:BA:85:59:6E','2018-08-24 22:22:01','On or near Holland Street','Tameside 025A','Violence and sexual offences','Under investigation',ST_GeomFromText('POINT(-2.125952 53.456924)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('E1:68:4D:92:FB:10','2018-08-23 15:57:24','On or near Back Burnaby Street','Bolton 021E','Violence and sexual offences','Unable to prosecute suspect',ST_GeomFromText('POINT(-2.445266 53.568947)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('F3:AF:79:03:F9:55','2018-08-29 07:47:27','On or near Aldworth Grove','Trafford 019D','Burglary','Investigation complete; no suspect identified',ST_GeomFromText('POINT(-2.354261 53.419073)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('33:F2:BA:C7:2D:88','2018-08-06 19:33:11','On or near Shrewsbury Close','Wigan 016A','Burglary','Investigation complete; no suspect identified',ST_GeomFromText('POINT(-2.563494 53.536908)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('D2:70:22:5F:62:15','2018-08-13 16:44:27','On or near Pym Street','Manchester 007B','Violence and sexual offences','Investigation complete; no suspect identified',ST_GeomFromText('POINT(-2.199558 53.513226)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('C0:D2:21:9B:EE:8A','2018-08-26 22:41:09','On or near Debenham Avenue','Manchester 012E','Public order','Investigation complete; no suspect identified',ST_GeomFromText('POINT(-2.181146 53.495791)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('E8:8B:3A:F9:7F:89','2018-08-25 19:08:15','On or near Parking Area','Manchester 050E','Criminal damage and arson','Investigation complete; no suspect identified',ST_GeomFromText('POINT(-2.265998 53.380426)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('5E:F0:0E:B9:E1:FB','2018-08-06 14:15:50','On or near Airport/Airfield','Manchester 053D','Shoplifting','Awaiting court outcome',ST_GeomFromText('POINT(-2.270186 53.360552)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('0E:B3:34:3A:AE:42','2018-08-21 20:42:30','On or near Redmere Drive','Bury 013C','Public order','Under investigation',ST_GeomFromText('POINT(-2.282882 53.582205)',4326));
INSERT INTO GreaterManchesterCrime (CrimeID,CrimeTS,Location,LSOA,Type,Outcome,theGeom) VALUES ('75:4F:3B:02:1C:B8','2018-08-13 04:41:40','On or near Derwent Street','Tameside 012C','Violence and sexual offences','Unable to prosecute suspect',ST_GeomFromText('POINT(-2.167349 53.483021)',4326));
'''


class SQLGenerator:
    def __init__(self, llm, db_cursor):
        self.llm = llm
        self.db_cursor = db_cursor

    def execute(self, query):
        res = self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f'''

                    Given the following table structure, respond to the user query by generating a SQL query.
                    Your response should only contain the text for the SQL query and nothing else.

                    If asked about where it occured, use Location as opposed to LSOA.

                    TABLE STRUCTURES:
                    {TABLE_STRUCTURES}

                    QUERY:
                    {query}
                    '''

                },
            ]
        )

        sql_query = res.choices[0].message.content
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        try:
            self.db_cursor.execute(sql_query)
        except Exception as e:
            return [], sql_query

        actual = []
        for row in self.db_cursor.fetchall():
            actual.append(row)

        return actual, sql_query
