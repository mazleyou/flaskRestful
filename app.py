# 필요한 모듈을 불러온다
from flask import Flask, request
from flask_restplus import Api, Resource, fields
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup
import configparser
import json


config = configparser.ConfigParser()
config.read('config.ini')

with open('config.json', 'r') as f:
    config = json.load(f)

host_addr = config['DEFAULT']['HOST_ADDR'] # 'secret-key-of-myapp'

# Open database connection
db = pymysql.connect(host=host_addr, port=8300, user='phoneticer', passwd='taiho9788', db='phonetic_db',
                     charset='utf8',
                     autocommit=True)

# prepare a cursor object using cursor() method
cursor = db.cursor()


app = Flask(__name__) # Flask App 생성한다
api = Api(app, version='1.0', title='phonetic translator', description='발음기호 사전') # API 만든다
ns = api.namespace('phonetic', description='발음기호 조회, 추가') # /phonetic/ 네임스페이스를 만든다

# REST Api에 이용할 데이터 모델을 정의한다
model_phonetic = api.model('row_phonetics', {
    'eng_word': fields.String(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'phon_word': fields.String(required=True, description='상품명', help='상품명은 필수')
})

class GoodsDAO(object):
    '''영어단어 발음기호 Data Access Object'''
    def __init__(self):
        self.counter = 0
        self.rows    = []

    def get(self, input_eng_word):
        '''영어단어를 이용하여 발음기호를 조회한다'''

        # execute SQL query using execute() method.
        sql = "select * from dict_eng_phon where engword=%s"
        cursor.execute(sql, (input_eng_word))
        db_row = cursor.fetchone()
        if db_row:
            # DB에 결과가 있으면 결과를 리턴
            return {'eng_word': db_row[1], 'phon_word': db_row[2]}
        else:
            html = urlopen('https://dictionary.cambridge.org/ko/%EC%82%AC%EC%A0%84/%EC%98%81%EC%96%B4/' + input_eng_word)
            bsObject = BeautifulSoup(html, 'html.parser')

            phon_from_crawling = bsObject.select(
                'span.us.dpron-i > span.pron.dpron > span'
            )
            sql = "insert into dict_eng_phon(engword,phonword) values (%s, %s)"
            if phon_from_crawling[0].text:
                cursor.execute(sql, (input_eng_word, phon_from_crawling[0].text))
                db.commit()
                # DB에 결과가 없고 크롤링한 결과가 있으면 크롤링 결과를 리턴하고 DB에 인서트
                return {'eng_word': input_eng_word, 'phon_word': phon_from_crawling[0].text}
            else:
                cursor.execute(sql, (input_eng_word, '<'+input_eng_word+'>'))
                db.commit()
                # DB에 결과가 없고 크롤링한 결과가 없으면 질의한 단어에 <>를 감싸서 리턴하고 DB에 인서트
                return {'eng_word': input_eng_word, 'phon_word': '<'+input_eng_word+'>'}

    def create(self, data):
        '''발음기호를 가져온다'''
        row = data
        self.rows.append(row)
        return row

    # def update(self, id, data):
    #     '''입력 id의 data를 수정한다'''
    #     row = self.get(id)
    #     row.update(data)
    #     return row
    #
    # def delete(self, id):
    #     '''입력 id의 data를 삭제한다'''
    #     row = self.get(id)
    #     self.rows.remove(row)

DAO = GoodsDAO() # DAO 객체를 만든다

@ns.route('/') # 네임스페이스 x.x.x.x/phonetic 하위 / 라우팅
class GoodsListManager(Resource):
    @ns.marshal_list_with(model_phonetic)
    def get(self):
        '''전체 리스트 조회한다'''
        return 1

    # @ns.expect(model_phonetic)
    # @ns.marshal_with(model_phonetic, code=201)
    # def post(self):
    #     '''새로운 id 추가한다'''
    #     # request.json[파라미터이름]으로 파라미터값 조회할 수 있다
    #     print('input goods_name is', request.json['goods_name'])
    #     return DAO.create(api.payload), 201


@ns.route('/<string:engword>') # 네임스페이스 x.x.x.x/eng_word 하위 /문자 라우팅
@ns.response(404, '단어를 찾을 수가 없어요')
@ns.param('engword', '영어단어를 입력해주세요')
class GoodsRUDManager(Resource):
    @ns.marshal_with(model_phonetic)
    def get(self, engword):
        '''해당 영어단어의 발음기호를 조회한다'''
        return DAO.get(engword)

    # def delete(self, id):
    #     '''해당 id 삭제한다'''
    #     DAO.delete(id)
    #     return '', 200
    #
    # @ns.expect(model_goods)
    # @ns.marshal_with(model_goods)
    # def put(self, id):
    #     '''해당 id 수정한다'''
    #     return DAO.update(id, api.payload)
