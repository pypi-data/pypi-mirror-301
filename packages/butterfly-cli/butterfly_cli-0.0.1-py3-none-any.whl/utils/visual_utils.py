from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def create_header():
    butterfly_ascii = r"""____  _   _ _____ _____ _____ ____  _____ _  __   __
| __ )| | | |_   _|_   _| ____|  _ \|  ___| | \ \ / /
|  _ \| | | | | |   | | |  _| | |_) | |_  | |  \ V / 
| |_) | |_| | | |   | | | |___|  _ <|  _| | |___| |  
|____/ \___/  |_|   |_| |_____|_| \_\_|   |_____|_|  
"""
    butterfly_line = "🦋 " * 18

    content = Text.assemble(
        (butterfly_ascii, "bold blue"),
        "\n",
        (butterfly_line, "blue")
    )

    return Panel(
        content,
        border_style="blue",
        expand=False,
        width=100
    )

def generate_markdown_report(report_data):
    markdown_content = """
# Butterfly Security Analysis Report

<div style="border: 2px solid #4a0080; border-radius: 10px; padding: 20px; margin-bottom: 20px;">

## Overall Summary

{overall_summary}

</div>

""".format(overall_summary=report_data.get('OVERALL_SUMMARY', 'No overall summary available.'))

    for key, value in report_data.items():
        if key != 'OVERALL_SUMMARY':
            markdown_content += f"""
<div style="border: 2px solid #6a0dad; border-radius: 10px; padding: 20px; margin-bottom: 20px;">

## {key.replace('_', ' ').title()}

{value}

</div>
"""

    markdown_content += """
<div style="border: 2px solid #9370db; border-radius: 10px; padding: 20px; margin-bottom: 20px;">

## Key Recommendations

"""
    recommendations = report_data.get('keyRecommendations', ['No specific recommendations available.'])
    for recommendation in recommendations:
        markdown_content += f"- {recommendation}\n"
    
    markdown_content += "\n</div>"

    return markdown_content

def save_markdown_report(markdown_content, file_path):
    with open(file_path, 'w') as report_file:
        report_file.write(markdown_content)
    console.print("[green]Your full, detailed report is available at your project root.[/green]")

def log_info(message):
    console.print(f"[blue]{message}[/blue]")