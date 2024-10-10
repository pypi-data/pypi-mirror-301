import asyncio
from rich.console import Console

console = Console()


async def playground(task):
    console.print(f"\nProcesso de teste iniciado: {task}\n", style="green")
    for numero in range(1, 600):
        console.print(f"Etapa [{numero}] de 600", style="green")
        await asyncio.sleep(1)
    console.print(f"Processo de teste finalizado.", style="green")
    return {"sucesso": True, "mensagem": "Processo de teste executado com sucesso"}
