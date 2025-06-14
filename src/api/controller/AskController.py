from src.assets.pattern.singleton import SingletonMeta
from src.api.models import Question, Response

from google import genai
from src.api.database.MyVanna import MyVanna

from src.assets.aux.env import env
# Gemini env vars
GEMINI_API_KEY = env["GEMINI_API_KEY"]
GEMINI_MODEL_NAME = env["GEMINI_MODEL_NAME"]

class AskController(metaclass=SingletonMeta):
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.vn = MyVanna(config={
            'print_prompt': False, 
            'print_sql': False,
            'api_key': GEMINI_API_KEY,
            'model_name': GEMINI_MODEL_NAME
        })

        self.vn.prepare()

    def ask(self, question: Question):
        client = genai.Client(api_key=GEMINI_API_KEY)

        vn = MyVanna(config={
            'print_prompt': False, 
            'print_sql': False,
            'api_key': GEMINI_API_KEY,
            'model_name': GEMINI_MODEL_NAME
        })

        sql_gerado = vn.generate_sql(question.question)
        resultado = vn.run_sql(sql_gerado)
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents="Transforme "+ str({"result": resultado}) +" em uma frase",
            config={
                "response_mime_type": "application/json",
                "response_schema": list[Response],
                }
            )
        texto = response.parsed[0].texto
        return {"output":texto}