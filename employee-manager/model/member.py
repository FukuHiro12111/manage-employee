import MySQLdb
import datetime
from decimal import Decimal

from db import DBConnector
from model.project import project
#python server.py
#python server.py migrate
#docker-compose exec jupyternotebook bash
#mysql -u root -p
#docker-compose exec mysql bash
#bash
#python -m unittest discover tests

class member:
    """従業員管理モデル"""

    def __init__(self):
        self.attr = {}
        self.attr["member_id"] = None
        self.attr["name"] = None
        self.attr["birthday"] = None
        self.attr["ym"] = None
        self.attr["gender"] = None
        self.attr["position"] = None
        self.attr["detail"] = None
        self.attr["money"] = None
        self.attr["last_updated"] = None

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_member;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_member` (
                `member_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `name` varchar(255) DEFAULT NULL,
                `birthday` date NOT NULL,
                `ym` int(11) NOT NULL,
                `gender` varchar(255) DEFAULT NULL,
                `position` varchar(255) DEFAULT NULL,
                `detail` text,
                `money` decimal(12,0) NOT NULL DEFAULT '0',
                `last_updated` datetime NOT NULL,
                PRIMARY KEY (`member_id`),
                KEY `position` (`position`)
                )""")
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(member_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_member
                WHERE member_id = %s;
            """, (member_id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        lm = member()
        lm.attr["member_id"] = data["member_id"]
        lm.attr["name"] = data["name"]
        lm.attr["birthday"] = data["birthday"]
        lm.attr["ym"] = data["ym"]
        lm.attr["gender"] = data["gender"]
        lm.attr["position"] = data["position"]
        lm.attr["detail"] = data["detail"]
        lm.attr["money"] = data["money"]
        lm.attr["last_updated"] = data["last_updated"]
        return lm

    def is_valid(self):
        return all([
          self.attr["member_id"] is None or type(self.attr["member_id"]) is int,
          self.attr["name"] is not None and type(self.attr["name"]) is str and len(self.attr["name"]) > 0,
          self.attr["birthday"] is not None and type(self.attr["birthday"]) is datetime.date,
          self.attr["ym"] is not None and type(self.attr["ym"]) is int and len(str(self.attr["ym"])) == 6,
          self.attr["gender"] is not None and type(self.attr["gender"]) is str and len(self.attr["gender"]) > 0,
          self.attr["position"] is not None and type(self.attr["position"]) is str and len(self.attr["position"]) > 0,
          self.attr["detail"] is None or type(self.attr["detail"]) is str,
          self.attr["money"] is not None and type(self.attr["money"]) is Decimal,
          self.attr["last_updated"] is not None and type(self.attr["last_updated"]) is datetime.datetime
        ])


    @staticmethod
    def build():
        now = datetime.datetime.now()
        lm = member()
        # defaultが設定されている変数はdefault値にしておくと良い
        # 日付も予め値が入っていた方が良い
        # 入力が必要な物はNoneのままにしておく
        lm.attr["birthday"] = now.date()
        lm.attr["ym"] = now.year*100 + now.month
        lm.attr["money"] = Decimal(0)
        lm.attr["last_updated"] = now
        return lm

    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    def _db_save(self):
        if self.attr["member_id"] == None:
            return self._db_save_insert()
        return self._db_save_update()

    def _db_save_insert(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_member
                    (name, birthday, ym, gender, position, detail, money, last_updated)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s); """,
                (self.attr["name"],
                self.attr["birthday"],
                self.attr["ym"],
                self.attr["gender"],
                self.attr["position"],
                self.attr["detail"],
                self.attr["money"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"])))
            
            # INSERTされたAUTO INCREMENT値を取得
            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["member_id"] = results[0]

            con.commit()

        return self.attr["member_id"]
    
    def _db_save_update(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_member
                SET name = %s,
                    birthday = %s,
                    ym = %s,
                    gender = %s,
                    position = %s,
                    detail = %s,
                    money = %s,
                    last_updated = %s
                WHERE member_id = %s; """,
                (self.attr["name"],
                self.attr["birthday"],
                self.attr["ym"],
                self.attr["gender"],
                self.attr["position"],
                self.attr["detail"],
                self.attr["money"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"]),
                self.attr["member_id"],))

            con.commit()
        
        return self.attr["member_id"]

    @staticmethod
    def order_by_member_id(member_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_member
                ORDER BY member_id ASC;
            """)
            results = cursor.fetchall()
        
        records = []
        for data in results:
            lm = member()
            lm.attr["member_id"] = data["member_id"]
            lm.attr["name"] = data["name"]
            lm.attr["birthday"] = data["birthday"]
            lm.attr["ym"] = data["ym"]
            lm.attr["gender"] = data["gender"]
            lm.attr["position"] = data["position"]
            lm.attr["detail"] = data["detail"]
            lm.attr["money"] = data["money"]
            lm.attr["last_updated"] = data["last_updated"]
            records.append(lm)

        return records
    
    def delete(self):
        if self.attr["member_id"] == None: return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_member
                WHERE member_id = %s; """,
                (self.attr["member_id"],))
            con.commit()

        return self.attr["member_id"]
    
    @staticmethod
    def _index(member_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT member_id FROM table_member
                WHERE member_id = %s; """,
                (member_id,))
            con.commit()
            recodes = cursor.fetchall()
        
        ids = [recode[0] for recode in recodes]
        return ids

    @staticmethod
    def serect_by_name(name):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            likename = '%' + name + '%'
            cursor.execute("""
                SELECT member_id FROM table_member
                WHERE `name` LIKE %s; """,
                (likename,))
            con.commit()
            recodes = cursor.fetchall()
        
        lm = [member.find(recode[0]) for recode in recodes]
        return lm
    
    @staticmethod
    def serect_by_position(position):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT member_id FROM table_member
                WHERE `position` = %s; """,
                (position,))
            con.commit()
            recodes = cursor.fetchall()
        
        lm = [member.find(recode[0]) for recode in recodes]
        return lm

    @staticmethod
    def serect_by_gender(gender):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT member_id FROM table_member
                WHERE `gender` = %s; """,
                (gender,))
            con.commit()
            recodes = cursor.fetchall()
        
        lm = [member.find(recode[0]) for recode in recodes]
        return lm
