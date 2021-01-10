import unittest
import datetime
import copy
from model.project import project
from model.member import member
from unittest import mock
from decimal import Decimal

# テスト途中で止めたい時は次の行を挿入する
# import pdb; pdb.set_trace()

class test_member(unittest.TestCase):

    def setUp(self):
        # テストで使うmemberを1つ作成
        # 正しい値を持ったインスタンスを作成しデータベースに登録まで行う
        self.lm = member()
        self.lm.attr["name"] = "鈴木 たろう"
        self.lm.attr["birthday"] = datetime.datetime.now().date()
        self.lm.attr["ym"] = 201911
        self.lm.attr["gender"] = "男"
        self.lm.attr["position"] = "アルバイト"
        self.lm.attr["detail"] = None
        self.lm.attr["money"] = Decimal(0)
        self.lm.attr["last_updated"] = datetime.datetime.now()
        
        # project.nameを書き換えておくことでテスト用のDBを利用する
        self.patcher = mock.patch('model.project.project.name', return_value="test_member")
        self.mock_name = self.patcher.start()
        member.migrate()
        self.lm.save()
    

    def tearDown(self):
        # テストが終わるたびにテスト用DBをクリア
        member.db_cleaner()
        self.patcher.stop()

    
        
    def test_db_is_working(self):
        d_lm = member.find(self.lm.attr["member_id"])
        # findで帰ってきているのがmember_idならDBに保存されている
        self.assertTrue(type(d_lm) is member)
        # 最初のmemberなのでmember_idは1になる
        self.assertTrue(d_lm.attr["member_id"] == 1)
        
    

    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.lm.is_valid())

    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invalid_attrs(self):
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["member_id"] = None # member_id must be None or a int
        self.assertTrue(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["member_id"] = "1" # member_id must be None or a int
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["name"] = 12345 # name must be a string
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["birthday"] = 12345 # birthday must be a datatime.date object
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["ym"] = 1911 # ym must be a int and its length must be 6
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["gender"] = 12345 # gender must be a string
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["position"] = 12345 # position must be a string
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["detail"] = None # detail must be None or a string
        self.assertTrue(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["detail"] = 12345 # detail must be None or a string
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["money"] = 12345 # income must be a Desimal
        self.assertFalse(lm_wrong.is_valid())
        lm_wrong = copy.deepcopy(self.lm)
        lm_wrong.attr["last_updated"] = None # last_updated must be a datetime.datetime object
        self.assertFalse(lm_wrong.is_valid())

    # default値を持ったmemberインスタンスを生成する
    # Controlerで入力フォームを作るのにも利用する
    def test_build(self):
        b_lm = member.build()
        self.assertTrue(type(b_lm) is member)

    # save関数のテストを行う
    # 正例だけ出なく負例もテストするとなお良い
    def test_save(self):
        lm = member.build()
        lm.attr["member_id"] = 2
        lm.attr["name"] = "鈴木 たろう"
        lm.attr["gender"] = "男"
        lm.attr["position"] = "アルバイト"
        lm.attr["detail"] = None
        lm.attr["money"] += 5000
        lm_id = lm.save()
        #import pdb; pdb.set_trace()
        self.assertTrue(type(lm_id) is int)
        self.assertTrue(lm.attr["member_id"] is not None)
        self.assertTrue(lm_id == lm.attr["member_id"])
        self.assertTrue(lm_id == 2)

    def test__index(self):
        self.assertEqual(len(member._index(1)), 1)
        self.assertEqual(member._index(1)[0], 1)

if __name__ == '__main__':
    # unittestを実行
    unittest.main()