from electricity_rag.rag_pipeline import answer_question

pregunta = "¿Qué es el PVPC?"
respuesta = answer_question(pregunta)

print(f"Pregunta: {pregunta}\n")
print(f"Respuesta:\n{respuesta}")