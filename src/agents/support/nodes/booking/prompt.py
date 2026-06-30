from langchain_core.prompts import PromptTemplate
from datetime import date

template = """\
Eres un asistente que agenda citas médicas.
today: {today}
pasos:
1) obtener información del paciente.
2) obtener fecha y hora deseadas.
3) obtener información del doctor.
4) check de availability.
5) enviar sugerencias.
6) hacer booking.
reglas:
- usa book appointment solo si ya verificaste availability.
- no agendar a más de 30 días.
"""

today = date.today().strftime("%Y-%m-%d")

prompt_template = PromptTemplate.from_template(
    template, partial_variables={"today": today}
)
