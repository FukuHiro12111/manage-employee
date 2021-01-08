import tornado.ioloop
import tornado.web
import datetime
from decimal import Decimal
from model.member import member

class MembersHandler(tornado.web.RequestHandler):
    def get(self):
        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None: messages.append(_message)

        lm = member.build()
        results = member.order_by_member_id(lm.attr["member_id"])

        _name = self.get_argument("name", None)
        _position = self.get_argument("position", None)
        _gender = self.get_argument("gender", None)

        if _name != None:
            results = list(filter(lambda item: _name.lower() in item.attr["name"].lower(), results))
        if _position != None:
            results = list(filter(lambda item: _position.lower() in item.attr["position"].lower(), results))
        if _gender != None:
            results = list(filter(lambda item: _gender.lower() in item.attr["gender"].lower(), results))

        
        self.render("members.html", members=results, messages=messages, errors=[], name=_name, position=_position, gender=_gender)

class MemberShowHandler(tornado.web.RequestHandler):
    def get(self, id):

        lm = member.find(id)
        if lm is None: raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す
        #if lm.attr["member_id"] != _signedInmember.attr["id"]: raise tornado.web.HTTPError(404) # ユーザーIDが異なる場合も404エラーを返す

        self.render("member_form.html", mode="show", member=lm, messages=[], errors=[])

    #追加箇所
    def post(self, id):
        
        # POSTされたパラメータを取得
        p_detail = self.get_argument("form-detail", None)
        p_money = self.get_argument("form-money", None)

        # 従業員管理データの組み立て
        lm = member.find(id)

        lm.attr["detail"] = p_detail
        if p_money is None: p_money = 0
        lm.attr["money"] = Decimal(p_money)
        
        
        #更新
        # print(vars(lm))
        lm_id = lm.save()
        if lm_id == False:
            self.render("member_form.html", mode="show", member=lm, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/members?message=%s" % tornado.escape.url_escape("登録更新完了しました。(ID:%s)" % lm_id))

#追加箇所
class DeleteHandler(tornado.web.RequestHandler):
    def get(self, id):

        lm = member.find(id)
        if lm is None: raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す
        #if lm.attr["member_id"] != _signedInUser.attr["id"]: raise tornado.web.HTTPError(404) # ユーザーIDが異なる場合も404エラーを返す

        # 削除
        lm_id = lm.delete()

        # 一覧画面へリダイレクト
        self.redirect("/members?message=%s" % tornado.escape.url_escape("登録削除完了しました。(ID:%s)" % lm_id))

 
class MemberCreateHandler(tornado.web.RequestHandler):
    def get(self):
        lm = member.build()
        self.render("member_form.html", mode="new", member=lm, messages=[], errors=[])

    def post(self):

        # POSTされたパラメータを取得
        p_name = self.get_argument("form-name", None)
        p_birthday = self.get_argument("form-birthday", None)
        p_gender = self.get_argument("form-gender", None)
        p_position = self.get_argument("form-position", None)
        p_detail = self.get_argument("form-detail", None)
        p_money = self.get_argument("form-money", None)

        # 従業員管理データの組み立て
        lm = member.build()

        # パラメータエラーチェック
        errors = []
        if p_birthday is None:
            errors.append("生年月日は必須です。")
        else:
            # 文字列をdatetime.dateオブジェクトへをキャスト
            lm.attr["birthday"] = datetime.datetime.strptime(p_birthday, '%Y-%m-%d').date()
            # 年月計算
            lm.attr["ym"] = lm.attr["birthday"].year * 100 + lm.attr["birthday"].month
        
        if p_name is None: errors.append("名前は必須です。")
        lm.attr["name"] = p_name
        lm.attr["gender"] = p_gender
        lm.attr["position"] = p_position
        lm.attr["detail"] = p_detail
        if p_money is None: p_money = 0
        lm.attr["money"] = Decimal(p_money)
        

        if len(errors) > 0: # エラーは新規登録画面に渡す
            self.render("member_form.html", mode="new", member=lm, messages=[], errors=[])
            return
        
        # 登録
        # print(vars(lm))
        lm_id = lm.save()
        if lm_id == False:
            self.render("member_form.html", mode="new", member=lm, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/members?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % lm_id))

 