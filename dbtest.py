import pymysql

# Open database connection
db = pymysql.connect(host='52.141.7.91', port=8300, user='phoneticer', passwd='taiho9788', db='phonetic_db',
                     charset='utf8',
                     autocommit=True)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
input_eng_word = 'So'
sql = "select * from dict_eng_phon where engword=%s"
cursor.execute(sql, (input_eng_word))
db_row = cursor.fetchone()
if db_row:
    print(db_row[1])