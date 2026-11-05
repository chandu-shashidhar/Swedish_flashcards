from pathlib import Path
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent

TRANSLATIONS = {
    "det": {"english": "it / that", "sentence_sv": "Jag ser det.", "sentence_en": "I see it."},
    "är": {"english": "is / am / are", "sentence_sv": "Det är bra.", "sentence_en": "It is good."},
    "jag": {"english": "I", "sentence_sv": "Jag går hem.", "sentence_en": "I am going home."},
    "att": {"english": "to / that", "sentence_sv": "Jag vill att du kommer.", "sentence_en": "I want you to come."},
    "och": {"english": "and", "sentence_sv": "Jag och du går.", "sentence_en": "You and I are walking."},
    "en": {"english": "a / one", "sentence_sv": "Jag har en bok.", "sentence_en": "I have a book."},
    "inte": {"english": "not", "sentence_sv": "Jag inte vill.", "sentence_en": "I do not want to."},
    "i": {"english": "in", "sentence_sv": "Jag är i Sverige.", "sentence_en": "I am in Sweden."},
    "på": {"english": "on / at", "sentence_sv": "Jag är på jobbet.", "sentence_en": "I am at work."},
    "du": {"english": "you", "sentence_sv": "Du är snäll.", "sentence_en": "You are kind."},
    "har": {"english": "have / has", "sentence_sv": "Jag har ett barn.", "sentence_en": "I have a child."},
    "för": {"english": "for / to", "sentence_sv": "Det är bra för mig.", "sentence_en": "It is good for me."},
    "som": {"english": "who / that / as", "sentence_sv": "Han är som min vän.", "sentence_en": "He is like my friend."},
    "med": {"english": "with", "sentence_sv": "Jag pratar med dig.", "sentence_en": "I am talking with you."},
    "om": {"english": "about / if", "sentence_sv": "Jag tänker om dig.", "sentence_en": "I am thinking about you."},
    "vi": {"english": "we", "sentence_sv": "Vi går till skolan.", "sentence_en": "We are going to school."},
    "så": {"english": "so / then", "sentence_sv": "Jag är så glad.", "sentence_en": "I am so happy."},
    "den": {"english": "it / that", "sentence_sv": "Jag köper den.", "sentence_en": "I am buying it."},
    "till": {"english": "to / until", "sentence_sv": "Jag går till affären.", "sentence_en": "I am going to the store."},
    "var": {"english": "was / were", "sentence_sv": "Det var roligt.", "sentence_en": "It was fun."},
    "av": {"english": "of / by", "sentence_sv": "Jag är rädd av dig.", "sentence_en": "I am afraid of you."},
    "de": {"english": "they / the", "sentence_sv": "De är här.", "sentence_en": "They are here."},
    "kan": {"english": "can / may", "sentence_sv": "Jag kan tala svenska.", "sentence_en": "I can speak Swedish."},
    "vad": {"english": "what", "sentence_sv": "Vad gör du?", "sentence_en": "What are you doing?"},
    "ett": {"english": "a / one", "sentence_sv": "Jag vill ha ett hus.", "sentence_en": "I want a house."},
    "han": {"english": "he", "sentence_sv": "Han kommer snart.", "sentence_en": "He is coming soon."},
    "men": {"english": "but", "sentence_sv": "Jag vill, men jag kan inte.", "sentence_en": "I want to, but I cannot."},
    "här": {"english": "here", "sentence_sv": "Jag är här.", "sentence_en": "I am here."},
    "mig": {"english": "me", "sentence_sv": "Han ser mig.", "sentence_en": "He sees me."},
    "ska": {"english": "will / shall", "sentence_sv": "Jag ska äta.", "sentence_en": "I will eat."},
    "nu": {"english": "now", "sentence_sv": "Jag är nu här.", "sentence_en": "I am here now."},
    "bara": {"english": "just / only", "sentence_sv": "Jag bara väntar.", "sentence_en": "I am just waiting."},
    "dig": {"english": "you", "sentence_sv": "Jag träffar dig.", "sentence_en": "I am meeting you."},
    "vill": {"english": "want", "sentence_sv": "Jag vill dricka vatten.", "sentence_en": "I want to drink water."},
    "när": {"english": "when", "sentence_sv": "När kommer du?", "sentence_en": "When are you coming?"},
    "hur": {"english": "how", "sentence_sv": "Hur är det?", "sentence_en": "How is it?"},
    "man": {"english": "one / you / man", "sentence_sv": "Man måste vakna.", "sentence_en": "One must wake up."},
    "kommer": {"english": "come / comes", "sentence_sv": "Han kommer idag.", "sentence_en": "He is coming today."},
    "där": {"english": "there", "sentence_sv": "Jag bor där.", "sentence_en": "I live there."},
    "då": {"english": "then / when", "sentence_sv": "Då gick vi hem.", "sentence_en": "Then we went home."},
    "min": {"english": "my", "sentence_sv": "Det är min bok.", "sentence_en": "This is my book."},
    "från": {"english": "from", "sentence_sv": "Jag kommer från Sverige.", "sentence_en": "I come from Sweden."},
    "skulle": {"english": "would", "sentence_sv": "Jag skulle gå.", "sentence_en": "I would go."},
    "eller": {"english": "or", "sentence_sv": "Te eller kaffe?", "sentence_en": "Tea or coffee?"},
    "bra": {"english": "good", "sentence_sv": "Det är väldigt bra.", "sentence_en": "It is very good."},
    "får": {"english": "may / can / get", "sentence_sv": "Jag får kaffe.", "sentence_en": "I get coffee."},
    "vara": {"english": "be", "sentence_sv": "Jag vill vara glad.", "sentence_en": "I want to be happy."},
    "ha": {"english": "have", "sentence_sv": "Jag vill ha mat.", "sentence_en": "I want food."},
    "ni": {"english": "you (plural)", "sentence_sv": "Ni är snälla.", "sentence_en": "You are kind."},
    "gör": {"english": "do / make", "sentence_sv": "Vad gör du?", "sentence_en": "What are you doing?"},
    "hon": {"english": "she", "sentence_sv": "Hon är min vän.", "sentence_en": "She is my friend."},
    "alla": {"english": "all", "sentence_sv": "Alla kommer idag.", "sentence_en": "Everyone is coming today."},
    "ut": {"english": "out", "sentence_sv": "Jag går ut.", "sentence_en": "I am going out."},
    "sig": {"english": "himself / herself / itself", "sentence_sv": "Han lär sig svenska.", "sentence_en": "He is learning Swedish."},
    "vet": {"english": "know", "sentence_sv": "Jag vet svaret.", "sentence_en": "I know the answer."},
    "hade": {"english": "had", "sentence_sv": "Jag hade en bil.", "sentence_en": "I had a car."},
    "måste": {"english": "must", "sentence_sv": "Jag måste gå.", "sentence_en": "I must go."},
    "ja": {"english": "yes", "sentence_sv": "Ja, jag kommer.", "sentence_en": "Yes, I am coming."},
    "göra": {"english": "do", "sentence_sv": "Jag vill göra mat.", "sentence_en": "I want to cook food."},
    "ta": {"english": "take", "sentence_sv": "Kan du ta boken?", "sentence_en": "Can you take the book?"},
    "upp": {"english": "up", "sentence_sv": "Jag står upp.", "sentence_en": "I am standing up."},
    "in": {"english": "in", "sentence_sv": "Jag går in.", "sentence_en": "I am going in."},
    "finns": {"english": "is / exists", "sentence_sv": "Det finns vatten här.", "sentence_en": "There is water here."},
    "få": {"english": "get / receive", "sentence_sv": "Jag vill få ett brev.", "sentence_en": "I want to receive a letter."},
    "mycket": {"english": "much / a lot", "sentence_sv": "Det finns mycket mat.", "sentence_en": "There is a lot of food."},
    "allt": {"english": "everything", "sentence_sv": "Jag vet allt.", "sentence_en": "I know everything."},
    "din": {"english": "your", "sentence_sv": "Det är din bok.", "sentence_en": "This is your book."},
    "lite": {"english": "a little", "sentence_sv": "Jag vill ha lite vatten.", "sentence_en": "I want a little water."},
    "ju": {"english": "of course / indeed", "sentence_sv": "Du ju vet det.", "sentence_en": "You know it, of course."},
    "tror": {"english": "believe / think", "sentence_sv": "Jag tror på dig.", "sentence_en": "I believe in you."},
    "se": {"english": "see", "sentence_sv": "Jag vill se dig.", "sentence_en": "I want to see you."},
    "än": {"english": "than / more than", "sentence_sv": "Jag är äldre än dig.", "sentence_en": "I am older than you."},
    "blir": {"english": "becomes / gets", "sentence_sv": "Jag blir trött.", "sentence_en": "I am getting tired."},
    "går": {"english": "goes / walks", "sentence_sv": "Jag går till jobbet.", "sentence_en": "I walk to work."},
    "varför": {"english": "why", "sentence_sv": "Varför är du här?", "sentence_en": "Why are you here?"},
    "efter": {"english": "after", "sentence_sv": "Jag kommer efter dig.", "sentence_en": "I am coming after you."},
    "dem": {"english": "them", "sentence_sv": "Jag ser dem.", "sentence_en": "I see them."},
    "oss": {"english": "us", "sentence_sv": "Han hjälper oss.", "sentence_en": "He is helping us."},
    "ingen": {"english": "no one / none", "sentence_sv": "Ingen kommer idag.", "sentence_en": "No one is coming today."},
    "nej": {"english": "no", "sentence_sv": "Nej, tack.", "sentence_en": "No, thank you."},
    "mer": {"english": "more", "sentence_sv": "Jag vill ha mer.", "sentence_en": "I want more."},
    "kanske": {"english": "maybe", "sentence_sv": "Kanske jag kommer.", "sentence_en": "Maybe I will come."},
    "över": {"english": "over / above", "sentence_sv": "Boken ligger över bordet.", "sentence_en": "The book is over the table."},
    "ser": {"english": "sees / looks", "sentence_sv": "Jag ser dig.", "sentence_en": "I see you."},
    "gå": {"english": "go", "sentence_sv": "Jag vill gå nu.", "sentence_en": "I want to go now."},
    "kom": {"english": "came", "sentence_sv": "Jag kom hem.", "sentence_en": "I came home."},
    "bli": {"english": "become", "sentence_sv": "Jag vill bli läkare.", "sentence_en": "I want to become a doctor."},
    "år": {"english": "year", "sentence_sv": "Jag är 30 år.", "sentence_en": "I am 30 years old."},
    "också": {"english": "also / too", "sentence_sv": "Jag kommer också.", "sentence_en": "I am coming too."},
    "något": {"english": "something / anything", "sentence_sv": "Jag behöver något.", "sentence_en": "I need something."},
    "två": {"english": "two", "sentence_sv": "Jag har två barn.", "sentence_en": "I have two children."},
    "sen": {"english": "since / later", "sentence_sv": "Jag kom sen.", "sentence_en": "I came later."},
    "aldrig": {"english": "never", "sentence_sv": "Jag har aldrig sett det.", "sentence_en": "I have never seen it."},
    "mitt": {"english": "my / middle", "sentence_sv": "Det är mitt hus.", "sentence_en": "It is my house."},
    "någon": {"english": "someone / some", "sentence_sv": "Jag träffade någon.", "sentence_en": "I met someone."},
    "tack": {"english": "thank you", "sentence_sv": "Tack för hjälpen.", "sentence_en": "Thank you for the help."},
    "behöver": {"english": "need", "sentence_sv": "Jag behöver vatten.", "sentence_en": "I need water."},
    "igen": {"english": "again", "sentence_sv": "Jag kommer igen.", "sentence_en": "I am coming again."},
    "detta": {"english": "this", "sentence_sv": "Jag gillar detta.", "sentence_en": "I like this."},
    "andra": {"english": "other / second", "sentence_sv": "Jag vill ha en annan.", "sentence_en": "I want another one."},
}


def parse_common_words(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    cards = []
    seen = set()

    for page in reader.pages:
        text = page.extract_text() or ""
        for match in re.finditer(
            r"(?m)^\s*(\d+)\s+([A-Za-zÅÄÖåäöÉéÜüß]+(?:[-'][A-Za-zÅÄÖåäöÉéÜüß]+)*)\s*$",
            text,
        ):
            rank = int(match.group(1))
            word = match.group(2).lower().strip()
            if len(word) < 2 or word in seen:
                continue
            seen.add(word)
            cards.append({
                "word": word,
                "source": "lingvoberry",
                "rank": rank,
                "level": "A0+",
                "type": "common",
            })

    return cards


def parse_core_words(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    seen = set()
    cards = []

    for page in reader.pages:
        text = page.extract_text() or ""
        for word in re.findall(r"[A-Za-zÅÄÖåäöÜüÉé]+", text):
            normalized = word.lower().strip()
            if len(normalized) < 2:
                continue
            if any(ch in normalized for ch in "åäöüé"):
                if normalized in seen:
                    continue
                seen.add(normalized)
                cards.append({
                    "word": normalized,
                    "source": "core2000",
                    "rank": len(cards) + 1,
                    "level": "core",
                    "type": "bonus",
                })

    return cards


def get_entry(word: str):
    entry = TRANSLATIONS.get(word)
    if entry:
        return entry
    return {
        "english": word,
        "sentence_sv": f"Jag gillar {word}.",
        "sentence_en": f"I like {word}.",
    }


def build_deck():
    all_cards = []
    for pdf_file in sorted(ROOT.glob("*.pdf")):
        name = pdf_file.name.lower()
        if "lingvoberry" in name:
            all_cards.extend(parse_common_words(pdf_file))
        elif "core" in name:
            all_cards.extend(parse_core_words(pdf_file))

    deduped = {}
    for card in all_cards:
        deduped.setdefault(card["word"], card)

    deck = []
    for card in deduped.values():
        entry = get_entry(card["word"])
        deck.append({
            "id": len(deck) + 1,
            "swedish": card["word"],
            "english": entry["english"],
            "sentence_sv": entry["sentence_sv"],
            "sentence_en": entry["sentence_en"],
            "source": card["source"],
            "rank": card["rank"],
            "level": card["level"],
            "type": card["type"],
        })

    deck = sorted(deck, key=lambda item: (item["source"] != "lingvoberry", item["rank"]))
    chosen = deck[:200]
    output_path = ROOT / "cards.json"
    output_path.write_text(json.dumps(chosen, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created {len(chosen)} flashcards in {output_path.name}")


if __name__ == "__main__":
    build_deck()
