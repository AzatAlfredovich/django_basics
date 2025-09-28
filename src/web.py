from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "localhost"
PORT = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обрабатываем GET-запросы и возвращаем contacts.html"""
        try:
            with open("contacts.html", "r", encoding="utf-8") as file:
                html_content = file.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Файл contacts.html не найден.".encode("utf-8"))

    def do_POST(self):
        """Дополнительное задание: принимаем POST-запрос и печатаем данные"""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        print("Данные, полученные от пользователя:", post_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<h2>Данные получены! Спасибо!</h2>".encode("utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((HOST, PORT), MyServer)
    print(f"Сервер запущен: http://{HOST}:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Сервер остановлен.")