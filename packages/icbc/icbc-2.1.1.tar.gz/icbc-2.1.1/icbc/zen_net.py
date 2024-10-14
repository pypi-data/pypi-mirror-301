# coding:utf-8
from icbc import z
try:
    import tornado.web
except:
    print("引入tornado失败，本模块功能基于tornado，为了方便内网环境无网使用基础模块，最新版本已移除tornado依赖，请另行使用pip install tornado安装以用zen_net功能")
    input()
def post(url, post_data):
    import urllib.request
    try:
        req_data = post_data.encode("utf-8")
    except:
        req_data = post_data
    request = urllib.request.Request(url, req_data)
    response = urllib.request.urlopen(request)
    return response.read()
    
def get(url):
    import urllib.request
    response = urllib.request.urlopen(url)
    return response.read()

def push_web(server, key, web):
    "note:only for gae api,web"
    result = {"api":"web", "key":key, "content":web, "permission":"icbc", "action" : "push"}
    result = z.json_dumps(result)
    post(server, result)

def tornado_server(port=8888):
    "tornado_server标准参考例子"
    import tornado.ioloop
    import tornado.web
    class main_handler(tornado.web.RequestHandler):
        def get(self):
            print(self.get_argument(''))
            self.write("get")
        def post(self):
            client_ip = self.request.remote_ip
            for i in  self.request.arguments:
                print(i)
            s = self.get_arguments("body")
            print(s)
            self.write("post")
    application = tornado.web.Application([(r"/", main_handler), ])
    application.listen(port)
    print("start web")
    tornado.ioloop.IOLoop.instance().start()


def file_server(nado, url=r"/file" , port=8031):
    import tornado.ioloop
    import tornado.web
    class UploadFileHandler(tornado.web.RequestHandler):
        def get(self):
            self.write('''
            <html>
              <body>
                <form action='file' enctype="multipart/form-data" method='post'>
                <input type='submit' value='submit'/>
                <input type='file' name='file'/>
                </form>
              </body>
            </html>''')
        def post(self):
            file_metas = self.request.files['file']
            for meta in file_metas:
                filename = meta['filename']
                filename_save = z.join(nado, filename)
                with open(filename_save, 'wb') as up:
                    up.write(meta['body'])
                self.write(filename + ' finished!')
    address = "http://%s:%d%s" % (z.get_ip() , port, url)
    print(address)
    app = tornado.web.Application([
        (url, UploadFileHandler),
    ])
     
    if __name__ == '__main__':
        app.listen(port)
        tornado.ioloop.IOLoop.instance().start()

url_router=[]
def router_regist(url, handler):
    url_router.append((r"/" + url, handler))
def router_static_regist(url="static", path="./static"):
    url_router.append(('/'+url+'/(.*)', tornado.web.StaticFileHandler, {'path': path}))
def router_static_regist(url="static", path="./static"):
    url_router.append(('/'+url+'/(.*)', tornado.web.StaticFileHandler, {'path': path}))
def func_file(filepath="file", url=r"/file"):
    class upload_file_handler(tornado.web.RequestHandler):
        def get(self):
            self.write('''
            <html>
            <head>
            <link href="favicon.ico" rel="shortcut icon">
            </head>
              <body>
                <form action='file' enctype="multipart/form-data" method='post'>
                <input type='submit' value='submit'/>
                <input type='file' name='file'/>
                </form>
              </body>
            </html>''')
        def post(self):
            file_metas = self.request.files['file']
            for meta in file_metas:
                filename = meta['filename']
                filename_save = z.join(z.folder(filepath), filename)
                with open(filename_save, 'wb') as up:
                    up.write(meta['body'])
                self.write(filename + ' finished!')
    router_regist("file",upload_file_handler)
    
def basic_server(port=8888,router=None,static_switch=False,file_switch=False):
    import tornado.ioloop
    import tornado.web
    z.dbp("服务器启动,服务端口：",port)
    if router ==None:
        router=url_router
        z.dbp("路由采用router_regist模式")
    if static_switch:
        router_static_regist()
    if file_switch:
        func_file()
    print("-"*20+"router list"+"-"*20)
    for i in router:
        print(i[0],max((20-len(i[0])),0)*" ",i[1])
    print("-"*50)
    settings={
        "gzip" : True,
        "debug" : True,
    }
    application = tornado.web.Application(router,**settings)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    
##def push_web():
##    z.sleep(2)
##    print("start demo")
##    push_web("http://127.0.0.1:8888/", "test", "ttttttttttttt")
##def test_tornado_server():
##    z.new_thread()
##    tornado_server()
##def test_file_server():
##    file_server("/Users/l/code/test/")
if __name__ == "__main__":
##    print(z.getcwd())
##    file_server(z.getcwd())
    basic_server(80,static_switch=True,file_switch=True)
