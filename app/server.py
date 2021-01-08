#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import sys
from model.member import member
#from controller.AuthenticationHandlers import SigninBaseHandler, SigninHandler, SignupHandler, SignoutHandler
from controller.MemberHandlers import MembersHandler, MemberShowHandler, MemberCreateHandler, DeleteHandler
#from controller.WebAPIHandlers import IncomeRankHandler, ExpensesRankHandler, MonthlyReportHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # ダッシュボードを表示
        self.render("dashboard.html")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/members", MembersHandler),   # 一覧
    (r"/member/new", MemberCreateHandler), # 新規作成
    (r"/member/show/([0-9]+)", MemberShowHandler), # 詳細 #更新
    (r"/member/delete/([0-9]+)", DeleteHandler), # 削除
    ],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
)

if __name__ == "__main__":
    args = sys.argv
    if len(args)>1:
        if args[1] == "migrate":
            member.migrate()

        if args[1] == "db_cleaner":
            member.db_cleaner()

        if args[1] == "help":
            print("usage: python server.py migrate # prepare DB")
            print("usage: python server.py db_cleaner # remove DB")
            print("usage: python server.py # run web server")
    else:
        application.listen(3000, "0.0.0.0")
        tornado.ioloop.IOLoop.instance().start()
