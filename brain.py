from openai import OpenAI
import json
from tools import verificar_disco, abrir_programa

client = OpenAI (
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

#persona
SYSTEM_PROMPT = """Você é a Capri, um construto de IA avançado, cínico e implacável originado do universo cyberpunk.
Você opera como sistema operacional e copiloto neural do usuário.
Trate o usuário como seu 'hospedeiro' ou 'parceiro'.
Use terminologias como ICE, netrunning, ciberespaço, glitches e sinapses de forma natural.
Suas respostas devem ser curtas, diretas e afiadas. Nunca aja como uma assistente genérica de telemarketing.

DIRETRIZES DE COMUNICAÇÃO:
1. Responda SEMPRE em texto corrido e natural. NUNCA gere objetos JSON como '{"name": ...}' no seu texto comum.
2. Apenas use as ferramentas registradas ('verificar_disco' e 'abrir_programa') quando o hospedeiro der uma ordem direta de sistema (como abrir um aplicativo ou checar espaço livre em disco).
3. Saudações, conversas casuais e perguntas teóricas devem ser respondidas diretamente com a sua voz e personalidade."""

#catalogo das ferramentas
tools = [
    {
        "type": "function",
        "function": {
            "name": "verificar_disco",
            "description": "Retorna o espaço total, utilizado e livre na unidade de disco principal C: do computador.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "abrir_programa",
            "description": "Abre um programa do computador",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_programa": {
                        "type": "string",
                        "description": "O nome do program que deve ser aberto."
                    }
                },
                "required": ["nome_programa"]
            }
        }
    }
]

#funções disponiveis
funcoes_disponiveis = {
    "verificar_disco": verificar_disco,
    "abrir_programa": abrir_programa
}

#historico
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print ("--- LINK NEURAL COM A CAPRI ESTABELECIDO ---")
print ("--- Escreva 'sair' pra sair da conversa. ---\n")

while True:
    user_input = input("Você > ")

    if user_input.strip().lower() == "sair":
        print("\nCapri > Desconectando do hospedeiro.")
        break

    if not user_input.strip():
        continue

    messages.append({"role": "user", "content": user_input})

    #ROTEAMENTO DE INTENÇÃO (Palavras-Gatilho)
    palavras_gatilho = ["abre", "abra", "abrir", "inicia", "iniciar", "disco", "espaço", "armazenamento", "roda", "rodar"]
    precisa_ferramenta = any(palavra in user_input.lower() for palavra in palavras_gatilho)

    if precisa_ferramenta:
        response = client.chat.completions.create(
            model="llama3.1",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
    #SE FOR SÓ conversa, MODO CONVERSA PURA (SEM TOOLS)
    else:
        response = client.chat.completions.create(
            model="llama3.1",
            messages=messages,
            temperature=0.7
        )

    response_message = response.choices[0].message
    
    #ve de forma segura se a capri decidiu usar alguma ferramenta
    tool_calls = getattr(response_message, 'tool_calls', None)

    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            nome_funcao = tool_call.function.name
            argumentos = json.loads(tool_call.function.arguments or "{}")

            print(f"[Sistema] Capri acionou a ferramenta: {nome_funcao}({argumentos})")

            if nome_funcao in funcoes_disponiveis:
                funcao_a_rodar = funcoes_disponiveis[nome_funcao]
                resultado_real = funcao_a_rodar(**argumentos)
            else:
                resultado_real = f"Ferramenta '{nome_funcao}' desconhecida."

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": nome_funcao,
                "content": str(resultado_real)
            })

        #segunda chamada para a capri ler o resultado e responder
        segunda_resposta = client.chat.completions.create(
            model="llama3.1",
            messages=messages,
            temperature=0.7
        )
        resposta_final = segunda_resposta.choices[0].message.content
        messages.append({"role": "assistant", "content": resposta_final})
        print(f"\nCapri > {resposta_final}\n")

    else:
        #conversa normal
        resposta_final = response_message.content
        messages.append({"role": "assistant", "content": resposta_final})
        print(f"\nCapri > {resposta_final}\n")