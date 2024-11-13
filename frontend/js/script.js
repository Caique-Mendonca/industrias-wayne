document.addEventListener('DOMContentLoaded', () => {
    const formLogin = document.getElementById('formLogin');
    const formRecurso = document.getElementById('formRecurso');
    const btnSair = document.getElementById('btnSair');

    formLogin.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        try {
            const resposta = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, senha })
            });

            const dados = await resposta.json();

            if (resposta.ok) {
                localStorage.setItem('token', dados.token);
                document.getElementById('login').classList.add('escondido');
                document.getElementById('dashboard').classList.remove('escondido');
                carregarDados();
            } else {
                alert('Erro ao fazer login: ' + dados.erro);
            }
        } catch (erro) {
            console.error('Erro:', erro);
            alert('Erro ao conectar com o servidor');
        }
    });

    formRecurso.addEventListener('submit', async (e) => {
        e.preventDefault();

        const recurso = {
            nome: document.getElementById('nomeRecurso').value,
            tipo: document.getElementById('tipoRecurso').value,
            quantidade: parseInt(document.getElementById('quantidadeRecurso').value),
            localizacao: document.getElementById('localizacaoRecurso').value
        };

        try {
            const resposta = await fetch('http://localhost:8000/recursos/adicionar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(recurso)
            });

            if (resposta.ok) {
                formRecurso.reset();
                await carregarDados();
                alert('Recurso adicionado com sucesso!');
            } else {
                alert('Erro ao adicionar recurso');
            }
        } catch (erro) {
            console.error('Erro:', erro);
            alert('Erro ao conectar com o servidor');
        }
    });

    btnSair.addEventListener('click', () => {
        localStorage.removeItem('token');
        document.getElementById('dashboard').classList.add('escondido');
        document.getElementById('login').classList.remove('escondido');
    });

    async function carregarDados() {
        try {
            await Promise.all([
                carregarRecursos(),
                carregarDadosDashboard()
            ]);
        } catch (erro) {
            console.error('Erro ao carregar dados:', erro);
        }
    }

    async function carregarRecursos() {
        try {
            const resposta = await fetch('http://localhost:8000/recursos', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (resposta.ok) {
                const recursos = await resposta.json();
                const listaRecursos = document.getElementById('listaRecursos');
                listaRecursos.innerHTML = '';

                recursos.forEach(recurso => {
                    const div = document.createElement('div');
                    div.className = 'recurso-item';
                    div.innerHTML = `
                        <div>
                            <strong>${recurso.nome}</strong> - 
                            ${recurso.tipo} (${recurso.quantidade} unidades)
                            <br>
                            <small>Localização: ${recurso.localizacao}</small>
                        </div>
                    `;
                    listaRecursos.appendChild(div);
                });
            }
        } catch (erro) {
            console.error('Erro ao carregar recursos:', erro);
        }
    }

    async function carregarDadosDashboard() {
        try {
            const resposta = await fetch('http://localhost:8000/dashboard/dados', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (resposta.ok) {
                const dados = await resposta.json();
                document.getElementById('totalRecursos').textContent = dados.totalRecursos || '0';
                document.getElementById('totalAlertas').textContent = dados.totalAlertas || '0';
            }
        } catch (erro) {
            console.error('Erro ao carregar dados do dashboard:', erro);
        }
    }

    // Se houver token salvo, carrega os dados automaticamente
    if (localStorage.getItem('token')) {
        document.getElementById('login').classList.add('escondido');
        document.getElementById('dashboard').classList.remove('escondido');
        carregarDados();
    }
});