import sys
import argparse
from pathlib import Path
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text


console = Console()


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_markdown_content(path: Path) -> str:
    """Load markdown content from file."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Menu description not found."


def display_menu_header_and_content(menu_md_path: Path):
    """Display the full menu content using Rich markdown rendering."""
    md_content = load_markdown_content(menu_md_path)
    
    # Create a beautiful panel for the menu
    markdown = Markdown(md_content)
    panel = Panel(
        markdown,
        title="BUas Data Science & AI BBQ Menu",
        title_align="center",
        border_style="bright_blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()


def display_ai_generated_images(data: dict, args):
    """Display AI-generated images as ASCII art for each dish."""
    console.print("[bold cyan]AI-Generated Food Images (converted to ASCII art)[/bold cyan]")
    console.print("=" * 60)
    console.print()
    
    for sec in data.get("sections", []):
        section_title = sec.get("title", "")
        console.print(f"[bold magenta]{section_title}[/bold magenta]")
        console.print("-" * 40)
        
        for itm in sec.get("items", []):
            item_name = itm.get("name", "")
            console.print(f"[bold yellow]{item_name}[/bold yellow]")
            
            try:
                from .menu_image_gen import generate_and_convert_to_ascii
                ascii_art = generate_and_convert_to_ascii(
                    itm, 
                    "generated_images", 
                    args.ascii_width, 
                    args.ascii_height
                )
                if ascii_art:
                    console.print(f"[dim]{ascii_art}[/dim]")
            except ImportError:
                console.print("[red]AI image generation not available.[/red]")
            except Exception as e:
                console.print(f"[red]Error generating AI image: {e}[/red]")
                # Fallback to template ASCII
                from .menu_image_gen import render_ascii_for_item
                ascii_art = render_ascii_for_item(itm)
                if ascii_art:
                    console.print(f"[dim]{ascii_art}[/dim]")
            
            console.print()
        
        console.print()


def print_header(title: str, subtitle: str | None):
    print(f"# {title}")
    if subtitle:
        print(f"({subtitle})")
    print("\n" + "-" * 80 + "\n")


def print_section(title: str, subtitle: str | None):
    if subtitle:
        print(f"## {title} ({subtitle})\n")
    else:
        print(f"## {title}\n")


def print_item(name: str, short: str):
    print(f"- {name}")
    if short:
        print(f"  {short}")
    print()


def print_notes(notes: list[str]):
    if not notes:
        return
    print("Notes:")
    for n in notes:
        print(f"  - {n}")
    print()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print the dinner menu from YAML")
    default_yaml = Path(__file__).parents[3] / "menu" / "dishes.yaml"
    default_menu_md = Path.cwd() / "menu" / "menu.md"  # Use current working directory
    
    parser.add_argument("yaml", nargs="?", default=str(default_yaml), help="Path to dishes.yaml")
    parser.add_argument("--menu-md", default=str(default_menu_md), help="Path to menu.md file")
    parser.add_argument("--with-ai-images", action="store_true", help="Generate AI images and convert to ASCII art")
    parser.add_argument("--ascii-width", type=int, default=60, help="Width of generated ASCII art")
    parser.add_argument("--ascii-height", type=int, default=30, help="Height of generated ASCII art")
    args = parser.parse_args(argv)

    # Display the beautiful Rich markdown menu first
    menu_md_path = Path(args.menu_md)
    display_menu_header_and_content(menu_md_path)

    if args.with_ai_images:
        # Load YAML data for AI image generation
        data = load_yaml(Path(args.yaml))
        display_ai_generated_images(data, args)
    
    console.print("[dim]Images saved in ./generated_images/[/dim]")
    console.print("[dim]Re-run this script anytime to see the menu again.[/dim]")


if __name__ == "__main__":
    sys.exit(main())