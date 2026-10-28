
import json
import urllib.request
import urllib.error


class OllamaAIService:
    """Комуникация с локалния AI модел чрез Ollama API."""

    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"

    def generate_response(self, user_message, tasks=None):
        if not user_message.strip():
            return "Моля, въведете въпрос."

        task_context = "Няма добавени задачи."

        if tasks:
            task_lines = []

            for task in tasks:
                task_lines.append(
                    f"Задача: {task[1]}\n"
                    f"Предмет: {task[2]}\n"
                    f"Описание: {task[3] or 'Няма'}\n"
                    f"Краен срок: {task[4] or 'Няма'}\n"
                    f"Приоритет: {task[5] or 'Няма'}"
                )

            task_context = "\n\n".join(task_lines)

        prompt = f"""
Ти си AI асистент за студенти в приложението TaskManager.

Правила:
- Отговаряй само на български език.
- Използвай правилна българска граматика.
- Помагай с организацията на ученето.
- Съобразявай се с крайните срокове и приоритетите.
- Не измисляй задачи, които не са предоставени.
- Ако липсва информация, посочи го.

Задачи на студента:
{task_context}

Въпрос на студента:
{user_message}
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4
            }
        }

        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(
                request, timeout=180
            ) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            return result.get(
                "response", "AI не върна отговор."
            ).strip()

        except urllib.error.URLError:
            return (
                "Неуспешна връзка с Ollama. "
                "Проверете дали програмата работи."
            )

        except TimeoutError:
            return "AI моделът не отговори навреме."

        except (ValueError, KeyError):
            return "Невалиден отговор от AI модела."


