#!/usr/bin/env python3
"""
Spanish Flashcard Trainer - Módulo 1
Ett enkelt CLI-verktyg för att öva spanska glosor.

Användning:
    python flashcard-trainer.py              # Kör alla kategorier
    python flashcard-trainer.py --category   # Välj kategori
    python flashcard-trainer.py --stats      # Visa statistik
"""

import json
import random
import os
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR.parent / "courses" / "sandra-gonzales" / "modulo-1-data.json"
PROGRESS_FILE = SCRIPT_DIR / "flashcard-progress.json"

# ANSI Colors for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def load_data():
    """Ladda glosdata från JSON-filen."""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_progress():
    """Ladda användarens progress."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"correct": 0, "wrong": 0, "sessions": [], "word_stats": {}}

def save_progress(progress):
    """Spara användarens progress."""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def clear_screen():
    """Rensa terminalen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Skriv ut header."""
    print(f"\n{Colors.CYAN}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}   🇪🇸 Spanish Flashcard Trainer - Módulo 1 🇪🇸{Colors.END}")
    print(f"{Colors.CYAN}{'='*50}{Colors.END}\n")

def get_flashcards_from_category(data, category_key):
    """Extrahera flashcards från en kategori."""
    cards = []
    category = data["categories"].get(category_key, {})

    if "items" in category:
        for item in category["items"]:
            if "es" in item and "sv" in item:
                cards.append({
                    "es": item["es"],
                    "sv": item["sv"],
                    "category": category.get("name", category_key),
                    "note": item.get("note", "")
                })
            elif "letter" in item:  # Alfabetet
                cards.append({
                    "es": f"{item['letter']} ({item['pronunciation']})",
                    "sv": f"Bokstaven {item['letter']}, uttalas '{item['pronunciation']}'",
                    "category": "Alfabetet",
                    "note": item.get("note", "")
                })
            elif "pregunta" in item:  # Presentationsfrågor
                cards.append({
                    "es": item["pregunta"],
                    "sv": item["sv_q"],
                    "category": "Presentación",
                    "note": f"Svar: {item['respuesta']}"
                })

    return cards

def get_all_flashcards(data):
    """Hämta alla flashcards från alla kategorier."""
    all_cards = []

    # Enkla kategorier med es/sv
    simple_categories = [
        "numeros_cardinales", "numeros_ordinales", "saludos",
        "interrogativos", "familia", "estado_civil", "colores",
        "emociones", "adjetivos_personalidad", "dias_semana",
        "tiempo_dia", "verbos_rutina"
    ]

    for cat_key in simple_categories:
        all_cards.extend(get_flashcards_from_category(data, cat_key))

    # Länder och nationaliteter
    if "paises_nacionalidades" in data["categories"]:
        for item in data["categories"]["paises_nacionalidades"]["items"]:
            all_cards.append({
                "es": item["pais"],
                "sv": item["sv"].split("/")[0],
                "category": "Länder",
                "note": f"Man: {item['m']}, Kvinna: {item['f']}"
            })

    # Verb böjningar
    if "verbos_basicos" in data["categories"]:
        verbs = data["categories"]["verbos_basicos"]["verbs"]
        for verb_name, verb_data in verbs.items():
            # Lägg till infinitiv
            all_cards.append({
                "es": verb_name,
                "sv": verb_data["meaning"],
                "category": "Verb (infinitiv)",
                "note": ""
            })
            # Lägg till yo-form
            if "conjugation" in verb_data:
                yo_form = verb_data["conjugation"][0]["form"]
                all_cards.append({
                    "es": yo_form,
                    "sv": f"jag {verb_data['meaning'].replace('att ', '')}",
                    "category": "Verb (yo)",
                    "note": f"Infinitiv: {verb_name}"
                })

    # SER och ESTAR böjningar
    if "ser_vs_estar" in data["categories"]:
        ser_estar = data["categories"]["ser_vs_estar"]
        for conj in ser_estar["ser"]["conjugation"]:
            all_cards.append({
                "es": f"SER: {conj['form']}",
                "sv": f"att vara ({conj['person']})",
                "category": "SER böjning",
                "note": "Permanenta egenskaper"
            })
        for conj in ser_estar["estar"]["conjugation"]:
            all_cards.append({
                "es": f"ESTAR: {conj['form']}",
                "sv": f"att vara/befinna sig ({conj['person']})",
                "category": "ESTAR böjning",
                "note": "Tillfälliga tillstånd & plats"
            })

    return all_cards

def show_categories(data):
    """Visa tillgängliga kategorier."""
    print(f"{Colors.BOLD}Tillgängliga kategorier:{Colors.END}\n")
    categories = [
        ("1", "numeros_cardinales", "Siffror (kardinaltal)"),
        ("2", "numeros_ordinales", "Ordningstal"),
        ("3", "saludos", "Hälsningar och avsked"),
        ("4", "interrogativos", "Frågeord"),
        ("5", "familia", "Familjen"),
        ("6", "estado_civil", "Civilstånd"),
        ("7", "colores", "Färger"),
        ("8", "emociones", "Känslor"),
        ("9", "paises_nacionalidades", "Länder & nationaliteter"),
        ("10", "verbos_basicos", "Grundverb"),
        ("11", "ser_vs_estar", "SER vs ESTAR"),
        ("12", "dias_semana", "Veckodagar"),
        ("13", "presentacion_personal", "Presentera dig"),
        ("0", "all", "ALLA kategorier"),
    ]

    for num, key, name in categories:
        count = len(get_flashcards_from_category(data, key)) if key != "all" else "alla"
        print(f"  {Colors.CYAN}{num}{Colors.END}. {name} ({count} kort)")

    return categories

def run_quiz(cards, mode="es_to_sv"):
    """Kör ett quiz med de givna korten."""
    if not cards:
        print(f"{Colors.RED}Inga kort att öva på!{Colors.END}")
        return 0, 0

    random.shuffle(cards)
    correct = 0
    wrong = 0

    print(f"\n{Colors.BOLD}Quiz startar! ({len(cards)} kort){Colors.END}")
    print(f"Skriv ditt svar eller tryck Enter för att se svaret.")
    print(f"Skriv 'q' för att avsluta.\n")

    for i, card in enumerate(cards, 1):
        if mode == "es_to_sv":
            question = card["es"]
            answer = card["sv"]
            lang_from, lang_to = "🇪🇸", "🇸🇪"
        else:
            question = card["sv"]
            answer = card["es"]
            lang_from, lang_to = "🇸🇪", "🇪🇸"

        print(f"{Colors.BLUE}[{i}/{len(cards)}]{Colors.END} {lang_from} {Colors.BOLD}{question}{Colors.END}")

        if card.get("note"):
            print(f"   {Colors.YELLOW}💡 {card['note']}{Colors.END}")

        user_input = input(f"   {lang_to} Ditt svar: ").strip()

        if user_input.lower() == 'q':
            print(f"\n{Colors.YELLOW}Quiz avslutat!{Colors.END}")
            break

        # Enkel matchning (case insensitive, trimma whitespace)
        is_correct = user_input.lower() == answer.lower()

        if is_correct:
            print(f"   {Colors.GREEN}✓ Rätt!{Colors.END}\n")
            correct += 1
        else:
            print(f"   {Colors.RED}✗ Fel!{Colors.END} Rätt svar: {Colors.GREEN}{answer}{Colors.END}\n")
            wrong += 1

    return correct, wrong

def show_stats(progress):
    """Visa statistik."""
    print(f"\n{Colors.BOLD}📊 Din statistik:{Colors.END}\n")

    total = progress["correct"] + progress["wrong"]
    if total > 0:
        percentage = (progress["correct"] / total) * 100
        print(f"  Totalt antal svar: {total}")
        print(f"  {Colors.GREEN}Rätt: {progress['correct']}{Colors.END}")
        print(f"  {Colors.RED}Fel: {progress['wrong']}{Colors.END}")
        print(f"  Träffsäkerhet: {Colors.BOLD}{percentage:.1f}%{Colors.END}")
    else:
        print("  Ingen statistik ännu. Börja öva!")

    if progress.get("sessions"):
        print(f"\n  Senaste session: {progress['sessions'][-1]}")

def main():
    """Huvudfunktion."""
    clear_screen()
    print_header()

    # Ladda data
    try:
        data = load_data()
    except FileNotFoundError:
        print(f"{Colors.RED}Kunde inte hitta datafilen!{Colors.END}")
        print(f"Förväntad plats: {DATA_FILE}")
        return

    progress = load_progress()

    # Huvudmeny
    while True:
        print(f"\n{Colors.BOLD}Vad vill du göra?{Colors.END}")
        print(f"  {Colors.CYAN}1{Colors.END}. Öva glosor (Spanska → Svenska)")
        print(f"  {Colors.CYAN}2{Colors.END}. Öva glosor (Svenska → Spanska)")
        print(f"  {Colors.CYAN}3{Colors.END}. Välj kategori")
        print(f"  {Colors.CYAN}4{Colors.END}. Visa statistik")
        print(f"  {Colors.CYAN}5{Colors.END}. Nollställ statistik")
        print(f"  {Colors.CYAN}q{Colors.END}. Avsluta")

        choice = input(f"\n{Colors.BOLD}Ditt val: {Colors.END}").strip()

        if choice == "1":
            cards = get_all_flashcards(data)
            correct, wrong = run_quiz(cards, "es_to_sv")
            progress["correct"] += correct
            progress["wrong"] += wrong
            progress["sessions"].append(datetime.now().isoformat())
            save_progress(progress)

        elif choice == "2":
            cards = get_all_flashcards(data)
            correct, wrong = run_quiz(cards, "sv_to_es")
            progress["correct"] += correct
            progress["wrong"] += wrong
            progress["sessions"].append(datetime.now().isoformat())
            save_progress(progress)

        elif choice == "3":
            print()
            categories = show_categories(data)
            cat_choice = input(f"\n{Colors.BOLD}Välj kategori (nummer): {Colors.END}").strip()

            selected_cat = None
            for num, key, name in categories:
                if cat_choice == num:
                    selected_cat = key
                    break

            if selected_cat == "all":
                cards = get_all_flashcards(data)
            elif selected_cat:
                cards = get_flashcards_from_category(data, selected_cat)
            else:
                print(f"{Colors.RED}Ogiltigt val!{Colors.END}")
                continue

            if cards:
                mode = input("Riktning? (1=ES→SV, 2=SV→ES): ").strip()
                mode = "sv_to_es" if mode == "2" else "es_to_sv"
                correct, wrong = run_quiz(cards, mode)
                progress["correct"] += correct
                progress["wrong"] += wrong
                save_progress(progress)

        elif choice == "4":
            show_stats(progress)

        elif choice == "5":
            confirm = input(f"{Colors.YELLOW}Nollställa all statistik? (ja/nej): {Colors.END}")
            if confirm.lower() == "ja":
                progress = {"correct": 0, "wrong": 0, "sessions": [], "word_stats": {}}
                save_progress(progress)
                print(f"{Colors.GREEN}Statistik nollställd!{Colors.END}")

        elif choice.lower() == "q":
            print(f"\n{Colors.CYAN}¡Hasta luego! 👋{Colors.END}\n")
            break

        else:
            print(f"{Colors.RED}Ogiltigt val!{Colors.END}")

if __name__ == "__main__":
    main()
