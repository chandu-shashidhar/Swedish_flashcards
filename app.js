const counterEl = document.getElementById('counter');
const frontTextEl = document.getElementById('frontText');
const backTextEl = document.getElementById('backText');
const flipBtn = document.getElementById('flipBtn');
const nextBtn = document.getElementById('nextBtn');
const nextCardBtn = document.getElementById('nextCardBtn');
const againBtn = document.getElementById('againBtn');
const modeBtn = document.getElementById('modeBtn');
const resetBtn = document.getElementById('resetBtn');
const viewBtn = document.getElementById('viewBtn');

const APP_VERSION = 'v5';
const KNOWN_KEY = 'swedish_flashcards_known';
const SENTENCE_KEY = 'swedish_flashcards_sentence_known';

let cards = [];
let sentences = [];
let activeCards = [];
let currentIndex = 0;
let isShowingAnswer = false;
let currentView = 'vocabulary';
let showOnlyNew = {
  vocabulary: true,
  sentences: true
};

function getKnownWords(key) {
  try {
    const saved = JSON.parse(localStorage.getItem(key) || '[]');
    return new Set(Array.isArray(saved) ? saved : []);
  } catch {
    return new Set();
  }
}

function saveKnownWords(key, knownWords) {
  localStorage.setItem(key, JSON.stringify([...knownWords]));
}

function getCurrentDeck() {
  return currentView === 'sentences' ? sentences : cards;
}

function getCurrentKnownKey() {
  return currentView === 'sentences' ? SENTENCE_KEY : KNOWN_KEY;
}

function shuffle(array) {
  const copy = [...array];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function refreshActiveCards() {
  const deck = getCurrentDeck();
  const knownWords = getKnownWords(getCurrentKnownKey());

  if (showOnlyNew[currentView]) {
    activeCards = deck.filter(card => !knownWords.has(card.swedish));
  } else {
    activeCards = [...deck];
  }

  if (!activeCards.length) {
    currentIndex = 0;
    return;
  }

  if (currentIndex >= activeCards.length) {
    currentIndex = 0;
  }
}

function updateCounter() {
  counterEl.textContent = activeCards.length ? `${currentIndex + 1} / ${activeCards.length}` : '0 / 0';
}

function updateButtons() {
  modeBtn.textContent = showOnlyNew[currentView] ? 'New words only: ON' : 'New words only: OFF';
  viewBtn.textContent = currentView === 'sentences' ? 'Switch to vocabulary' : 'Switch to daily sentences';
}

function renderCard() {
  if (!activeCards.length) {
    const emptyMessage = currentView === 'sentences'
      ? 'You have finished all current daily sentences.'
      : 'You have finished all current new words.';
    frontTextEl.textContent = currentView === 'sentences' ? 'All sentences studied' : 'All caught up';
    backTextEl.innerHTML = `${emptyMessage}<br><br>Tap “Reset review” to study again.`;
    backTextEl.classList.remove('hidden');
    isShowingAnswer = true;
    flipBtn.textContent = 'Hide answer';
    updateCounter();
    return;
  }

  const card = activeCards[currentIndex];
  frontTextEl.textContent = card.swedish;

  if (currentView === 'sentences') {
    backTextEl.innerHTML = `<strong>English:</strong> ${card.english}`;
  } else {
    backTextEl.innerHTML = `
      <strong>English:</strong> ${card.english}<br><br>
      <strong>Swedish:</strong> ${card.sentence_sv || card.swedish}<br>
      <strong>English:</strong> ${card.sentence_en || card.english}
    `;
  }

  backTextEl.classList.add('hidden');
  isShowingAnswer = false;
  flipBtn.textContent = 'Show answer';
  updateCounter();
}

function flipCard() {
  if (!activeCards.length) return;
  isShowingAnswer = !isShowingAnswer;
  backTextEl.classList.toggle('hidden', !isShowingAnswer);
  flipBtn.textContent = isShowingAnswer ? 'Hide answer' : 'Show answer';
}

function markKnown() {
  if (!activeCards.length) return;
  const card = activeCards[currentIndex];
  const knownWords = getKnownWords(getCurrentKnownKey());
  knownWords.add(card.swedish);
  saveKnownWords(getCurrentKnownKey(), knownWords);
  nextCard();
}

function nextCard() {
  if (!activeCards.length) return;
  currentIndex = (currentIndex + 1) % activeCards.length;
  renderCard();
}

function nextCardWithoutMarking() {
  if (!activeCards.length) return;
  nextCard();
}

function repeatCard() {
  if (!activeCards.length) return;
  renderCard();
}

function resetStudiedWords() {
  localStorage.removeItem(getCurrentKnownKey());
  currentIndex = 0;
  refreshActiveCards();
  renderCard();
}

function toggleStudyMode() {
  showOnlyNew[currentView] = !showOnlyNew[currentView];
  updateButtons();
  refreshActiveCards();
  renderCard();
}

function toggleView() {
  currentView = currentView === 'sentences' ? 'vocabulary' : 'sentences';
  currentIndex = 0;
  updateButtons();
  refreshActiveCards();
  renderCard();
}

function loadDeckData() {
  Promise.all([
    fetch(`cards.json?cache=${APP_VERSION}`).then((response) => {
      if (!response.ok) {
        throw new Error('Could not load vocabulary cards');
      }
      return response.json();
    }),
    fetch(`sentences.json?cache=${APP_VERSION}`).then((response) => {
      if (!response.ok) {
        throw new Error('Could not load daily sentences');
      }
      return response.json();
    })
  ])
    .then(([vocabulary, sentenceData]) => {
      cards = shuffle(vocabulary);
      sentences = shuffle(sentenceData);

      if (!cards.length || !sentences.length) {
        throw new Error('No data found');
      }

      refreshActiveCards();
      renderCard();
    })
    .catch(() => {
      cards = [
        {
          swedish: 'det',
          english: 'it / that',
          sentence_sv: 'Jag ser det.',
          sentence_en: 'I see it.',
          source: 'lingvoberry',
          rank: 1,
          level: 'A0'
        },
        {
          swedish: 'jag',
          english: 'I',
          sentence_sv: 'Jag går hem.',
          sentence_en: 'I am going home.',
          source: 'lingvoberry',
          rank: 3,
          level: 'A0'
        },
        {
          swedish: 'är',
          english: 'is / am / are',
          sentence_sv: 'Det är bra.',
          sentence_en: 'It is good.',
          source: 'lingvoberry',
          rank: 2,
          level: 'A0'
        }
      ];
      sentences = [
        {
          swedish: 'Hej, hur mår du?',
          english: 'Hi, how are you?',
          sentence_sv: 'Hej, hur mår du?',
          sentence_en: 'Hi, how are you?'
        },
        {
          swedish: 'Jag är trött idag.',
          english: 'I am tired today.',
          sentence_sv: 'Jag är trött idag.',
          sentence_en: 'I am tired today.'
        },
        {
          swedish: 'Vad vill du äta?',
          english: 'What do you want to eat?',
          sentence_sv: 'Vad vill du äta?',
          sentence_en: 'What do you want to eat?'
        }
      ];
      refreshActiveCards();
      renderCard();
    });
}

function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register(`./service-worker.js?cache=${APP_VERSION}`).catch(() => {});
    });
  }
}

flipBtn.addEventListener('click', flipCard);
nextBtn.addEventListener('click', markKnown);
nextCardBtn.addEventListener('click', nextCardWithoutMarking);
againBtn.addEventListener('click', repeatCard);
modeBtn.addEventListener('click', toggleStudyMode);
resetBtn.addEventListener('click', resetStudiedWords);
viewBtn.addEventListener('click', toggleView);

updateButtons();
registerServiceWorker();
loadDeckData();
