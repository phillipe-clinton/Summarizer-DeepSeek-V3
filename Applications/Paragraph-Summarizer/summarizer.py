import requests
import time
import sys
from rich.console import Console

console = Console()

def type_effect(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()


def summarize_paragraphs(paragraphs, max_tokens):
    API_URL = "https://api.deepinfra.com/v1/inference/deepseek-ai/DeepSeek-V3"
    API_KEY = "HPgijrzxITI8arAO1GnijTYteSFFVswV"  # Replace with your actual API key

    summaries = []
    for i, paragraph in enumerate(paragraphs, 1):
        console.print(f"[bold green]Generating summary {i} of {len(paragraphs)}...[/bold green]")
        prompt = f"Summarize the following paragraph concisely in about {max_tokens // 4} words:\n\n{paragraph}\n\nSummary:"

        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "input": prompt,
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.95,
            }
        )

        if response.status_code == 200:
            summary = response.json()["results"][0]["generated_text"].strip()
            summaries.append(summary)
        else:
            summaries.append("Error: Failed to generate summary.")

    return summaries

if __name__ == "__main__":
    console.print("[bold cyan]Enter the paragraphs you want to summarize (press Enter twice to finish):[/bold cyan]")
    user_input = []
    while True:
        line = input()
        if line.strip() == "" and user_input and user_input[-1] == "":
            break
        user_input.append(line)

    paragraphs = "\n".join(user_input).split("\n\n")

    while True:
        try:
            max_tokens = int(input("Enter desired summary length (20-500 tokens): "))
            if 20 <= max_tokens <= 500:
                break
            else:
                console.print("[bold red]Please enter a number between 20 and 200.[/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a valid number.[/bold red]")

    console.print("\n[bold green]Input received. Generating summaries...[/bold green]")
    
    summaries = summarize_paragraphs(paragraphs, max_tokens)

    for i, summary in enumerate(summaries, 1):
        console.print(f"\n[bold cyan]Summary for paragraph {i}:[/bold cyan]")
        type_effect(summary)
