"""Temporary script to generate web/locales/pt/app.json and update other locale catalogs with language.portuguese."""

from __future__ import annotations

import json
import pathlib

WEB = pathlib.Path(__file__).resolve().parent.parent / "web"
LOCALES = WEB / "locales"

PORTUGUESE_TRANSLATIONS = {
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
    "Start": "Iniciar",
    "Learn": "Aprender",
    "Research": "Pesquisa",
    "Dashboard": "Painel",
    "Question Generator": "Gerador de Questões",
    "Custom": "Personalizado",
    "Generating": "Gerando",
    "questions": "questões",
    "extended": "estendido",
    "Count": "Contagem",
    "Questions": "Questões",
    "Correct Answer": "Resposta Correta",
    "Explanation": "Explicação",
    "round": "rodada",
    "s": "s",
    "Submitted": "Enviado",
    "Brainstorm": "Brainstorm",
    "Code": "Código",
    "Reason": "Motivo",
    "Arxiv Search": "Busca no arXiv",
    "Papers": "Artigos",
    "Deep Solve": "Deep Solve",
    "Quiz Generation": "Geração de Quiz",
    "Math Animator": "Animador Matemático",
    "Guided Learning": "Aprendizado Guiado",
    "Flexible conversation with any tool": "Conversa flexível com qualquer ferramenta",
    "Multi-step reasoning & problem solving": "Raciocínio em várias etapas e resolução de problemas",
    "Auto-validated question generation": "Geração de questões com validação automática",
    "Comprehensive multi-agent research": "Pesquisa multi-agente abrangente",
    "No KB": "Sem Base de Conhecimento",
    "Tools": "Ferramentas",
    "Loading models": "Carregando modelos",
    "Models unavailable": "Modelos indisponíveis",
    "Refresh models": "Atualizar modelos",
    "Select model": "Selecionar modelo",
    "Choose a model": "Escolha um modelo",
    "Settings": "Configurações",
    "Language": "Idioma",
    "Theme": "Tema",
    "Save": "Salvar",
    "Cancel": "Cancelar",
    "Delete": "Excluir",
    "Edit": "Editar",
    "Search": "Pesquisar",
    "History": "Histórico",
    "New Chat": "Nova Conversa",
    "Chat": "Chat",
    "Knowledge Base": "Base de Conhecimento",
    "Memory": "Memória",
    "Profile": "Perfil",
    "Logout": "Sair",
    "Login": "Entrar",
    "Submit": "Enviar",
    "Back": "Voltar",
    "Next": "Avançar",
    "Close": "Fechar",
    "Confirm": "Confirmar",
    "Loading": "Carregando...",
    "Error": "Erro",
    "Success": "Sucesso",
    "Warning": "Aviso",
    "Info": "Informação",
    # Settings sidebar & General page translations:
    "Back to app": "Voltar ao aplicativo",
    "Search settings": "Pesquisar configurações",
    "Personal": "Pessoal",
    "Workspace": "Espaço de trabalho",
    "Data migration": "Migração de dados",
    "Appearance": "Aparência",
    "Usage statistics": "Estatísticas de uso",
    "Models & services": "Modelos e serviços",
    "Providers": "Provedores",
    "Language models": "Modelos de linguagem",
    "Task models": "Modelos de tarefas",
    "Embedding models": "Modelos de embedding",
    "Voice": "Voz",
    "Multimodal generation": "Geração multimodal",
    "Learning & conversation": "Aprendizado e conversa",
    "Conversation": "Conversa",
    "Attachments": "Anexos",
    "Video Learning": "Aprendizado por vídeo",
    "Learning progress": "Progresso de aprendizado",
    "Make DeepTutor feel at home. Apply your preferences using the bar below.": "Faça o DeepTutor se sentir em casa. Aplique suas preferências usando a barra abaixo.",
    "Interface language": "Idioma da interface",
    "Controls navigation, settings, and status text only.": "Controla apenas a navegação, configurações e textos de status.",
    "Model output language": "Idioma de saída do modelo",
    "Sets the default language for chat and capability responses.": "Define o idioma padrão para as respostas do chat e capacidades.",
    "Layout": "Layout",
    "Interface layout": "Layout da interface",
    "Classic keeps the familiar navigation; Modern is the redesigned interface.": "O clássico mantém a navegação familiar; O moderno é a interface redesenhada.",
    "Set up chat first": "Configure o chat primeiro",
    "Connect a provider and choose a language model. Other services are optional.": "Conecte um provedor e escolha um modelo de linguagem. Outros serviços são opcionais.",
    "Follow the steps below, or let your own Agent help you configure DeepTutor.": "Siga as etapas abaixo ou deixe seu próprio Agente ajudar a configurar o DeepTutor.",
    "Let your Agent help you configure": "Deixe seu Agente ajudar a configurar",
    "1. Connect a provider": "1. Conectar um provedor",
    "Add your provider and credentials, then test the connection.": "Adicione seu provedor e credenciais, depois teste a conexão.",
    "2. Choose a chat model": "2. Escolha um modelo de chat",
    "Add a language model, test it, and select it as the default for conversations.": "Adicione um modelo de linguagem, teste-o e selecione-o como o padrão para conversas.",
    "3. Apply and check": "3. Aplicar e verificar",
    "Apply your changes using the bottom bar, then check service status before starting a conversation.": "Aplique suas alterações usando a barra inferior, depois verifique o status do serviço antes de iniciar uma conversa.",
    # Chat Actions:
    "Explain": "Explicar",
    "Solve": "Resolver",
    "Practice": "Praticar",
    "Plan": "Planejar",
    "Ideas for you": "Ideias para você",
    "New conversation": "Nova conversa",
    # Calendar:
    "Today": "Hoje",
    "Day": "Dia",
    "Week": "Semana",
    "Month": "Mês",
    "Agenda": "Agenda",
    "+ New event": "+ Novo evento",
    "Unscheduled tasks": "Tarefas não agendadas",
    "Every open task has a date.": "Toda tarefa aberta tem uma data.",
    "Calendars": "Calendários",
    "Export all calendars": "Exportar todos os calendários",
    "My calendar": "Meu calendário",
    "+ New calendar": "+ Novo calendário",
    "From this workspace": "Deste espaço de trabalho",
    "Task due dates": "Prazos de tarefas",
    "Reviews coming due": "Revisões a vencer",
    "Automations": "Automações",
    "Learning footprints": "Pegadas de aprendizado",
    "Turn on reminders": "Ativar lembretes",
    # Task Board:
    "All dates": "Todas as datas",
    "Open calendar": "Abrir calendário",
    "Add a task...": "Adicionar uma tarefa...",
    "To do": "A fazer",
    "Next steps and ideas": "Próximos passos e ideias",
    "In progress": "Em andamento",
    "What I am working on": "No que estou trabalhando",
    "Done": "Concluído",
    "Finished work": "Trabalho finalizado",
    "Drop a card here": "Solte um cartão aqui",
    "Tasks are saved to your independent board. Assign them to workspaces or link them to conversations.": "As tarefas são salvas no seu quadro independente. Atribua-as a espaços de trabalho ou vincule-as a conversas.",
    # Notebook:
    "Your notebook is empty": "Seu caderno está vazio",
    "Start a page for a topic, a lecture or a paper. Dito can help you write and turn it into practice.": "Inicie uma página para um tópico, aula ou artigo. O Dito pode ajudá-lo a escrever e colocá-lo em prática.",
    "+ New page": "+ Nova página",
    "Import Word": "Importar Word",
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
        print(f"Updated {app_json} with language.portuguese = {name}")

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
    print(f"Created {pt_app_json} with {len(pt_data)} keys.")

if __name__ == "__main__":
    main()
