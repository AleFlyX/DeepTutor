"""Temporary script to generate comprehensive web/locales/pt/app.json in Brazilian Portuguese."""

from __future__ import annotations

import json
import pathlib

WEB = pathlib.Path(__file__).resolve().parent.parent / "web"
LOCALES = WEB / "locales"

PORTUGUESE_TRANSLATIONS = {
    "Home": "Início",
    "Partners": "Parceiros",
    "Personalized Learning": "Aprendizado Personalizado",
    "Learning Space": "Espaço de Aprendizado",
    "Calendar": "Calendário",
    "Task Board": "Quadro de Tarefas",
    "Settings": "Configurações",
    "Knowledge Base": "Base de Conhecimento",
    "Notebook": "Caderno",
    "Reading": "Leitura",
    "Book Library": "Biblioteca de Livros",
    "Skills": "Habilidades",
    "Morning — let's learn something.": "Bom dia — vamos aprender algo.",
    "Good morning.": "Bom dia.",
    "Good afternoon.": "Boa tarde.",
    "Good evening.": "Boa noite.",
    "How can I help you today?": "Como posso te ajudar hoje?",
    "Explain": "Explicar",
    "Solve": "Resolver",
    "Practice": "Praticar",
    "Plan": "Planejar",
    "Research": "Pesquisar",
    "Brainstorm": "Brainstorm",
    "Code": "Código",
    "Visualize": "Visualizar",
    "Quiz": "Quiz",
    "Generating": "Gerando",
    "Generating...": "Gerando...",
    "Send": "Enviar",
    "Stop": "Parar",
    "New Chat": "Nova Conversa",
    "Chat": "Chat",
    "General": "Geral",
    "Workspace": "Espaço de Trabalho",
    "Appearance": "Aparência",
    "Status": "Status",
    "Network": "Rede",
    "Models": "Modelos",
    "LLM": "LLM",
    "Embedding": "Embedding",
    "Search": "Busca",
    "Capabilities": "Capacidades",
    "Memory": "Memória",
    "Tools": "Ferramentas",
    "Save & Apply": "Salvar e Aplicar",
    "Save Draft": "Salvar Rascunho",
    "Apply": "Aplicar",
    "Cancel": "Cancelar",
    "Delete": "Excluir",
    "Edit": "Editar",
    "Save": "Salvar",
    "Back": "Voltar",
    "Next": "Avançar",
    "Close": "Fechar",
    "Confirm": "Confirmar",
    "Loading": "Carregando...",
    "Error": "Erro",
    "Success": "Sucesso",
    "Warning": "Aviso",
    "Info": "Informação",
    "Task List": "Lista de Tarefas",
    "Learning Path": "Trilha de Aprendizado",
    "Mastery Path": "Caminho de Domínio",
    "Deep Research": "Pesquisa Profunda",
    "Start Research": "Iniciar Pesquisa",
    "Retry Research": "Tentar Novamente",
    "Research Complete": "Pesquisa Concluída",
    "Research Outline": "Esboço da Pesquisa",
    "Select model": "Selecionar modelo",
    "Choose a model": "Escolha um modelo",
    "Refresh models": "Atualizar modelos",
    "Models unavailable": "Modelos indisponíveis",
    "Loading models": "Carregando modelos",
    "No KB": "Sem Base de Conhecimento",
    "Correct Answer": "Resposta Correta",
    "Explanation": "Explicação",
    "Questions": "Questões",
    "Question Generator": "Gerador de Questões",
    "Guided Learning": "Aprendizado Guiado",
    "Math Animator": "Animador Matemático",
    "Quiz Generation": "Geração de Quiz",
    "Deep Solve": "Resolução Profunda",
    "Papers": "Artigos",
    "Arxiv Search": "Busca no arXiv",
    "Reason": "Motivo",
    "Submitted": "Enviado",
    "Count": "Contagem",
    "Custom": "Personalizado",
    "Dashboard": "Painel",
    "Theme": "Tema",
    "Light": "Claro",
    "Dark": "Escuro",
    "System": "Sistema",
    "Glass": "Vidro",
    "Default": "Padrão",
    "Profile": "Perfil",
    "Logout": "Sair",
    "Login": "Entrar",
    "Password": "Senha",
    "Username": "Nome de usuário",
    "API Key": "Chave API",
    "Base URL": "URL Base",
    "Port": "Porta",
    "Host": "Host",
    "Partially correct": "Parcialmente correto",
    "These answers could not be submitted. Please review or retry.": "Não foi possível enviar estas respostas. Revise ou tente novamente.",
    "The edit could not be sent. Your draft is still here; please retry.": "Não foi possível enviar a edição. Seu rascunho ainda está aqui; tente novamente.",
    "Discard unsent draft": "Descartar rascunho não enviado",
    "Discarding…": "Descartando…",
    "This draft could not be discarded. Please retry or copy it before leaving.": "Não foi possível descartar este rascunho. Tente novamente ou copie-o antes de sair.",
    "Review rebuild": "Revisar reconstrução",
    "language.english": "Inglês",
    "language.chinese": "中文",
    "language.french": "Français",
    "language.german": "Deutsch",
    "language.ukrainian": "Ucraniano",
    "language.polish": "Polski",
    "language.portuguese": "Português",
    "settingsTour.appearance.title": "Aparência",
    "settingsTour.appearance.desc": "Tema visual e estilo de bloco de código. As alterações se aplicam imediatamente.",
    "settingsTour.status.title": "Status",
    "settingsTour.status.desc": "Verifique a disponibilidade do backend, uso de memória e quais serviços estão prontos nesta página.",
    "settingsTour.network.title": "Rede",
    "settingsTour.network.desc": "Portas, base de API voltada para o navegador e origens CORS — para Docker, rede local e implantações de proxy reverso.",
    "settingsTour.models.title": "Modelos",
    "settingsTour.models.desc": "Escolha modelos por finalidade. Conexões de serviço mantêm credenciais reutilizáveis; a atribuição de modelo escolhe o que cada tarefa usa.",
    "settingsTour.knowledge.title": "Base de Conhecimento",
    "settingsTour.knowledge.desc": "Escolha o motor de análise de documentos que converte uploads em texto.",
    "settingsTour.chat.title": "Chat",
    "settingsTour.chat.desc": "Ajuste sugestões da tela inicial e tempos limite de resposta. Ferramentas e capacidades de aprendizado têm suas próprias páginas na barra lateral.",
    "settingsTour.llm.title": "LLM",
    "settingsTour.llm.desc": "Gerencie perfis de LLM — provedor, endpoint e modelo. O modelo ativo alimenta o chat e a maioria dos raciocínios dos agentes.",
    "settingsTour.embedding.title": "Embedding",
    "settingsTour.embedding.desc": "Configure o provedor de embedding e as dimensões usadas para recuperação e ingestão na base de conhecimento.",
    "settingsTour.search.title": "Busca",
    "settingsTour.search.desc": "Escolha o provedor de busca na web e ajuste as configurações de proxy / solicitação.",
    "settingsTour.capabilities.title": "Capacidades",
    "settingsTour.capabilities.desc": "Ajuste parâmetros de LLM por capacidade e limites de execução para cada capacidade exibida no chat (chat / resolver / questão / pesquisa / …).",
    "settingsTour.memory.title": "Memória",
    "settingsTour.memory.desc": "Ajuste o consolidador de memória: divisão em blocos, orçamentos de LLM, desduplicação e políticas de referência.",
    "settingsTour.mcp.title": "Servidores MCP",
    "settingsTour.mcp.desc": "Conecte servidores MCP (Model Context Protocol) externos para expor mais ferramentas ao agente (em breve).",
    "settingsTour.tools.title": "Ferramentas",
    "settingsTour.tools.desc": "Ative ou desative as ferramentas selecionáveis pelo usuário aqui; ferramentas bloqueadas são montadas automaticamente quando o agente de chat precisar delas.",
    "settingsTour.apply.title": "Salvar e Aplicar",
    "settingsTour.apply.desc": "Salvar Rascunho persiste suas alterações; Aplicar as ativa imediatamente. Ambos os controles ficam na barra de ferramentas superior, sempre ao seu alcance.",
    "settings.configNote": "Salvar Rascunho persiste todos os perfis em model_catalog.json, que o DeepTutor lê em tempo de execução. Aplicar ativa o perfil selecionado e atualiza os clientes em tempo de execução. Você pode manter vários perfis no catálogo e alternar entre eles a qualquer momento.",
    "guidedLearning.title": "Caminho de Domínio",
    "guidedLearning.description": "Aprendizado estruturado baseado em domínio com repetição espaçada",
    "guidedLearning.noModules": "Nenhum módulo ainda",
    "guidedLearning.startLearning": "Iniciar Caminho de Domínio",
    "guidedLearning.modules": "Módulos",
    "guidedLearning.knowledgePoints": "pontos de conhecimento",
    "guidedLearning.knowledgePointsLabel": "Pontos de Conhecimento",
    "guidedLearning.mastered": "Dominado",
    "guidedLearning.stages": "Estágios de Aprendizado",
    "guidedLearning.ready": "Pronto para iniciar o Caminho de Domínio",
    "guidedLearning.selectModule": "Selecionar um Módulo",
    "guidedLearning.selectModuleDesc": "Escolha um módulo para iniciar o Caminho de Domínio",
    "guidedLearning.generatingDiagnostic": "Gerando perguntas de diagnóstico...",
    "guidedLearning.connectionError": "Erro de conexão",
    "guidedLearning.stageFailed": "A execução do estágio falhou. Progresso salvo, este estágio será tentado novamente.",
    "guidedLearning.moduleProgress": "{{count}} ponto(s) de conhecimento",
    "guidedLearning.masteredProgress": "{{mastered}}/{{total}} dominados",
    "guidedLearning.inputPlaceholder": "Digite sua resposta...",
    "guidedLearning.submit": "Enviar",
    "guidedLearning.noModulesLoaded": "Nenhum módulo carregado",
    "guidedLearning.createModule": "Criar Módulo",
    "guidedLearning.tabCurrent": "Em Andamento",
    "guidedLearning.tabCompleted": "Concluído",
    "guidedLearning.tabAll": "Todos",
    "guidedLearning.continueLearning": "Continuar Aprendizado",
    "guidedLearning.redo": "Refazer",
    "guidedLearning.redoConfirm": "Isso redefinirá seu progresso mas manterá os módulos. Continuar?",
    "guidedLearning.redoFailed": "Falha ao refazer o progresso",
    "guidedLearning.delete": "Excluir",
}

PORTUGUESE_NAMES_FOR_LOCALES = {
    "en": "Portuguese",
    "zh": "葡萄牙语",
    "fr": "Portugais",
    "de": "Portugiesisch",
    "uk": "Португальська",
    "pl": "Portugalski",
    "pt": "Português",
}

def main() -> None:
    # 1. Update existing locale catalogs with language.portuguese
    for locale_dir in LOCALES.iterdir():
        if not locale_dir.is_dir():
            continue
        app_json = locale_dir / "app.json"
        if not app_json.exists():
            continue
        code = locale_dir.name
        data = json.loads(app_json.read_text(encoding="utf-8"))
        name = PORTUGUESE_NAMES_FOR_LOCALES.get(code, "Portuguese")
        data["language.portuguese"] = name
        app_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Reload en_data after updating en/app.json
    en_path = LOCALES / "en" / "app.json"
    en_data = json.loads(en_path.read_text(encoding="utf-8"))

    # 2. Create web/locales/pt/app.json
    pt_dir = LOCALES / "pt"
    pt_dir.mkdir(parents=True, exist_ok=True)
    pt_data = {}
    for k, v in en_data.items():
        if k in PORTUGUESE_TRANSLATIONS:
            pt_data[k] = PORTUGUESE_TRANSLATIONS[k]
        else:
            pt_data[k] = v

    pt_app_json = pt_dir / "app.json"
    pt_app_json.write_text(json.dumps(pt_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated comprehensive {pt_app_json} with {len(pt_data)} keys.")

if __name__ == "__main__":
    main()
