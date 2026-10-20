import json
import os
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path("/Users/pedrotgon/Developer/Start AI/tg-video-studio/sistema_priscila")
PORT = 8088

DB_FILE = BASE_DIR / "db.json"

DEFAULT_DATA = {
    "profile": {
        "username": "priscila_lpss",
        "full_name": "Priscila Lopes",
        "title": "Massoterapia Integrativa",
        "address": "Av. Antônio Carlos Sales Júnior, 325 - Jardim Proença, Campinas/SP",
        "followers": 12840,
        "following": 820,
        "posts_count": 48,
        "reach_30d": 48920,
        "engagement_rate": "7,8%",
        "interactions_30d": 4150,
        "avatar_url": "assets/avatar_priscila.jpg",
        "bio": "Cuidado integral, alívio de dores e descompressão profunda no Jardim Proença, Campinas.\nAtendimento individual com hora marcada."
    },
    "posts": [
        {
            "id": "post-01",
            "title": "Post 01 · Novo Endereço de Atendimento",
            "status": "pronto",
            "format": "Feed 4:5 / Stories",
            "date": "19 out",
            "image": "assets/Post_01_Novo_Endereco.png",
            "caption": "Cuidado, silêncio e presença em um novo endereço.\n\nNosso espaço de atendimento agora está localizado no Jardim Proença, em Campinas. Um ambiente preparado com carinho em cada detalhe, com iluminação acolhedora, privacidade total e o conforto que o seu corpo precisa para desacelerar.\n\nLocalização:\nAv. Antônio Carlos Sales Júnior, 325\nJardim Proença, Campinas/SP\n\nAtendimento individual com hora marcada.",
            "hashtags": "#massoterapia #campinas #jardimproenca #bemestar #aliviodeestresse",
            "approved": True
        },
        {
            "id": "post-02",
            "title": "Post 02 · O Santuário do Jardim Proença",
            "status": "producao",
            "format": "Feed 4:5 / Carrossel",
            "date": "21 out",
            "image": "assets/Post_02_O_Espaco.png",
            "caption": "O silêncio que a sua mente precisa.\n\nQuando você entra na sala de atendimento, o ritmo acelerado da rotina fica do lado de fora. Iluminação suave à luz de velas, aromaterapia selecionada, maca ampla e acolhedora, além de climatização suave pensada para o seu relaxamento profundo.",
            "hashtags": "#espaçoterapeutico #massoterapiacampinas #relaxamentoprofundo #silencio",
            "approved": False
        },
        {
            "id": "post-03",
            "title": "Post 03 · Massoterapia Clínica & Alívio de Dores",
            "status": "aprovacao",
            "format": "Feed 4:5 / Vídeo",
            "date": "23 out",
            "image": "assets/Post_03_Massoterapia_Clinica.png",
            "caption": "Alívio que vai além da superfície.\n\nDores cervicais, nós de tensão nos ombros e peso constante na região lombar não precisam fazer parte da sua rotina. Através da massoterapia clínica, aplicamos manobras precisas para desativar pontos de gatilho e restaurar o equilíbrio muscular.",
            "hashtags": "#massoterapiaclinica #liberacaomiofascial #aliviodedores #postura",
            "approved": False
        },
        {
            "id": "post-04",
            "title": "Post 04 · Rituais de Cuidado Integrativo",
            "status": "producao",
            "format": "Feed 4:5 / Stories",
            "date": "25 out",
            "image": "assets/Post_04_Rituais_Cuidado.png",
            "caption": "O tempo que o seu corpo merece.\n\nConheça os protocolos dedicados ao alívio e renovação integral:\n1. Massoterapia Terapêutica (Alívio de dores e contraturas)\n2. Relaxante com Pedras Quentes (Termoterapia profunda)\n3. Drenagem Linfática Integrativa (Desinchaço e leveza)",
            "hashtags": "#protocolosdebemestar #massagemrelaxante #pedrasquentes #campinas",
            "approved": False
        }
    ],
    "consultorio_renders": [
        {
            "id": "render-01",
            "title": "Perspectiva Principal · Maca & Carrinho de Carvalho",
            "image": "assets/consultorio_transformado_01.jpg",
            "desc": "Maca vestida em linho branco com peseira waffle caramelo, quadro da lótus e carrinho em carvalho com toalhas hoteleiras."
        },
        {
            "id": "render-02",
            "title": "Vista Angular · Pendente Difuso & Painel Ripado",
            "image": "assets/consultorio_transformado_02.jpg",
            "desc": "Luz indireta 2400K substituindo a lâmpada crua, sanca quente, arandela sobre o quadro e painel ripado."
        },
        {
            "id": "render-03",
            "title": "Bancada Terapêutica · Vidros Âmbar & Pedras Vulcânicas",
            "image": "assets/consultorio_detalhes_zen.jpg",
            "desc": "Frascos âmbar de aromaterapia, pedras quentes de basalto, xícara de chá e vela vegetal."
        }
    ]
}

def load_db():
    if not DB_FILE.exists():
        save_db(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class PriscilaOSHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = load_db()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        if self.path == "/api/posts/approve":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            req = json.loads(body.decode("utf-8"))
            post_id = req.get("id")
            
            data = load_db()
            for p in data.get("posts", []):
                if p["id"] == post_id:
                    p["approved"] = True
                    p["status"] = "pronto"
                    break
            save_db(data)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": data}).encode("utf-8"))
            return

        if self.path == "/api/apify/scrape":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            req = json.loads(body.decode("utf-8")) if body else {}
            token = req.get("token") or os.environ.get("APIFY_TOKEN", "")
            username = req.get("username", "priscila_lpss")

            if not token:
                # Return current baseline cached metrics
                data = load_db()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                resp = {
                    "source": "cached_baseline",
                    "message": "Token do Apify não configurado. Exibindo dados locais de referência.",
                    "profile": data["profile"]
                }
                self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
                return

            # Call Apify API
            apify_url = f"https://api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items?token={token}"
            payload = json.dumps({"usernames": [username]}).encode("utf-8")
            api_req = urllib.request.Request(
                apify_url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(api_req, timeout=45) as response:
                    raw = response.read().decode("utf-8")
                    apify_res = json.loads(raw)
                    data = load_db()
                    if isinstance(apify_res, list) and len(apify_res) > 0:
                        first = apify_res[0]
                        data["profile"]["followers"] = first.get("followersCount", data["profile"]["followers"])
                        data["profile"]["following"] = first.get("followsCount", data["profile"]["following"])
                        data["profile"]["posts_count"] = first.get("postsCount", data["profile"]["posts_count"])
                        data["profile"]["bio"] = first.get("biography", data["profile"]["bio"])
                        save_db(data)

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"source": "apify_live", "data": apify_res}).encode("utf-8"))
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"source": "error_fallback", "error": str(e), "profile": load_db()["profile"]}).encode("utf-8"))
            return

        super().do_POST()

def run_server():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, PriscilaOSHandler)
    print(f"Sistema Priscila Lopes rodando em: http://127.0.0.1:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
