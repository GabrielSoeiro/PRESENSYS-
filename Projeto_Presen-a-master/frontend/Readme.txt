# GUIA COMPLETO — APRESENTAÇÃO PRESENSYS

## O QUE PRECISA TER NO PC DA APRESENTAÇÃO

### Instalar:

* Python
* Git
* Ngrok

---

# 1. INSTALAR PYTHON

Baixar:
https://www.python.org/downloads/

IMPORTANTE:
Marcar:

✔ Add Python to PATH

---

# 2. INSTALAR GIT

Baixar:
https://git-scm.com/downloads

---

# 3. INSTALAR NGROK

Linux:

```bash
sudo snap install ngrok
```

Windows:
Baixar no site:
https://ngrok.com/download

---

# 4. BAIXAR O PROJETO

No terminal:

```bash
git clone https://github.com/bielsoeiro/PRESENSYS-BACK-AND-FRONT.git
```

---

# 5. ENTRAR NA PASTA

```bash
cd PRESENSYS-BACK-AND-FRONT
```

---

# 6. CRIAR AMBIENTE VIRTUAL

Linux:

```bash
python3 -m venv .venv
```

Windows:

```bash
python -m venv .venv
```

---

# 7. ATIVAR AMBIENTE

Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

# 8. INSTALAR DEPENDÊNCIAS

```bash
pip install -r requirements.txt
```

---

# 9. RODAR BACKEND

```bash
python projeto.py
```

Se aparecer:

```txt
Running on http://127.0.0.1:5000
```

está funcionando.

NÃO FECHAR ESSE TERMINAL.

---

# 10. CONFIGURAR NGROK

## Login no site:

https://dashboard.ngrok.com

Copiar token.

---

# 11. ADICIONAR TOKEN

```bash
ngrok config add-authtoken SEU_TOKEN
```

---

# 12. ABRIR NGROK

EM OUTRO TERMINAL:

```bash
ngrok http 5000
```

Vai aparecer algo tipo:

```txt
https://abc123.ngrok-free.app
```

NÃO FECHAR ESSE TERMINAL.

---

# 13. TROCAR LINK NO SCRIPT.JS

Abrir:

```txt
frontend/script.js
```

Trocar:

```javascript
const API = "LINK_ANTIGO"
```

Por:

```javascript
const API = "https://abc123.ngrok-free.app"
```

---

# 14. SUBIR FRONT NO NETLIFY

Entrar:
https://app.netlify.com/drop

Arrastar pasta:

```txt
frontend
```

---

# 15. TESTAR

Abrir site do Netlify.

Testar:

* cadastro
* câmera
* reconhecimento
* presença

---

# IMPORTANTE

NÃO FECHAR:

✔ terminal do Flask
✔ terminal do ngrok

---

# FLUXO DO SISTEMA

Frontend Online
↓
Ngrok
↓
Backend Local
↓
DeepFace
↓
Reconhecimento Facial

---

# OBSERVAÇÕES

* Toda vez que reiniciar o ngrok o link muda.
* Sempre atualizar o script.js.
* TensorFlow pode demorar na primeira inicialização.
* Testar tudo antes da apresentação.

