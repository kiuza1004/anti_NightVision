#!/usr/bin/env python3
"""
Night Vision Local Development Server
외부 의존성 없이 Python 표준 라이브러리만으로 동작하는 로컬 HTTP 서버입니다.
"""

import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # 개발 중 변경사항 즉시 반영을 위한 캐시 비활성화 헤더
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def run_server(port=8000):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, NoCacheHandler)
    
    print(f"==================================================")
    print(f" Night Vision 로컬 개발 서버 시작됨")
    print(f" - 로컬 접속: http://localhost:{port}")
    print(f" - 루프백 접속: http://127.0.0.1:{port}")
    print(f" ※ 카메라(getUserMedia)는 localhost 환경에서 정상 작동합니다.")
    print(f" 종료하려면 Ctrl+C를 누르세요.")
    print(f"==================================================")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
        httpd.server_close()

if __name__ == '__main__':
    port_arg = 8000
    if len(sys.argv) > 1:
        try:
            port_arg = int(sys.argv[1])
        except ValueError:
            print(f"잘못된 포트 번호: {sys.argv[1]}. 기본값 8000을 사용합니다.")
    run_server(port_arg)
