const API = "https://5afe-2804-b2c-996-e886-8caa-be6a-ba6d-59f.ngrok-free.app"

const totalPresencas = document.getElementById("totalPresencas")
const statusSistema = document.getElementById("statusSistema")
const listaPresencas = document.getElementById("listaPresencas")

const formCadastro = document.getElementById("formCadastro")
const preview = document.getElementById("preview")
const previewPlaceholder = document.getElementById("previewPlaceholder")

const inputFoto = document.getElementById("fotoAluno")
const cameraInput = document.getElementById("cameraInput")

const menuMobile = document.getElementById("menuMobile")
const sidebar = document.getElementById("sidebar")
const overlay = document.getElementById("overlay")

let fotoSelecionada = null

async function carregarDashboard() {
  try {
    const response = await fetch(`${API}/dashboard`)
    const dados = await response.json()

    if (totalPresencas) {
      totalPresencas.innerText = dados.total_presencas
    }

    if (statusSistema) {
      statusSistema.innerText = dados.status
    }
  } catch (erro) {
    console.log(erro)
  }
}

async function carregarPresencas() {
  if (!listaPresencas) return

  try {
    const response = await fetch(`${API}/presencas`)
    const dados = await response.json()

    listaPresencas.innerHTML = ""

    dados.forEach((presenca) => {
      const item = document.createElement("div")
      item.classList.add("presenca-item")

      item.innerHTML = `
        <div class="presenca-info">
          <h3>${presenca.aluno}</h3>
          <p>${presenca.horario}</p>
        </div>

        <div class="status-presente">
          ${presenca.status}
        </div>
      `

      listaPresencas.appendChild(item)
    })
  } catch (erro) {
    console.log(erro)
  }
}

function mostrarPreview(arquivo) {
  if (!arquivo) return

  fotoSelecionada = arquivo

  const leitor = new FileReader()

  leitor.onload = (event) => {
    if (preview) {
      preview.src = event.target.result
      preview.style.display = "block"
    }

    if (previewPlaceholder) {
      previewPlaceholder.style.display = "none"
    }
  }

  leitor.readAsDataURL(arquivo)
}

if (cameraInput) {
  cameraInput.addEventListener("change", (event) => {
    const arquivo = event.target.files[0]

    if (!arquivo) return

    inputFoto.value = ""

    mostrarPreview(arquivo)
  })
}

if (inputFoto) {
  inputFoto.addEventListener("change", (event) => {
    const arquivo = event.target.files[0]

    if (!arquivo) return

    if (cameraInput) {
      cameraInput.value = ""
    }

    mostrarPreview(arquivo)
  })
}

if (formCadastro) {
  formCadastro.addEventListener("submit", async (event) => {
    event.preventDefault()

    const nome = document.getElementById("nomeAluno").value.trim()

    if (!nome) {
      alert("Digite o nome do aluno.")
      return
    }

    if (!fotoSelecionada) {
      alert("Tire uma foto ou escolha um arquivo.")
      return
    }

    const formData = new FormData()

    formData.append("nome", nome)
    formData.append("foto", fotoSelecionada, `${nome}.jpeg`)

    try {
      const response = await fetch(`${API}/cadastrar-aluno`, {
        method: "POST",
        body: formData
      })

      const dados = await response.json()

      alert(dados.mensagem || "Aluno cadastrado com sucesso.")

      formCadastro.reset()
      fotoSelecionada = null

      if (preview) {
        preview.src = ""
        preview.style.display = "none"
      }

      if (previewPlaceholder) {
        previewPlaceholder.style.display = "flex"
      }
    } catch (erro) {
      console.log(erro)
      alert("Erro ao cadastrar aluno.")
    }
  })
}

if (menuMobile && sidebar && overlay) {
  menuMobile.addEventListener("click", () => {
    sidebar.classList.add("active")
    overlay.classList.add("active")
    menuMobile.classList.add("hidden")
  })

  overlay.addEventListener("click", () => {
    sidebar.classList.remove("active")
    overlay.classList.remove("active")
    menuMobile.classList.remove("hidden")
  })

  const linksMenu = sidebar.querySelectorAll("a")

  linksMenu.forEach((link) => {
    link.addEventListener("click", () => {
      sidebar.classList.remove("active")
      overlay.classList.remove("active")
      menuMobile.classList.remove("hidden")
    })
  })
}

async function iniciarSistema() {
  await carregarDashboard()
  await carregarPresencas()
}

setInterval(() => {
  carregarDashboard()
  carregarPresencas()
}, 3000)

iniciarSistema()