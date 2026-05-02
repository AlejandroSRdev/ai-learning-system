const API_BASE = import.meta.env.VITE_API_URL;

if (!API_BASE) {
  throw new Error("VITE_API_URL is not defined");
}

let studentId = null;
let hasExplanation = false;
let hasEvaluation = false;
let currentQuestions = [];
let selectedAnswers = [];

async function createStudent() {
  const level = document.getElementById("level").value;
  const goal = document.getElementById("goal").value;
  const current_topic = document.getElementById("current_topic").value;
  try {
    const url = `${API_BASE}/students`;
    console.log("Request:", url);
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ level, goal, current_topic })
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    document.getElementById("error-msg").style.display = "none";
    studentId = data.student_id;
    const display = document.getElementById("student-display");
    display.textContent = "Student ID: " + studentId;
    display.style.display = "block";
    document.getElementById("section-2").style.display = "block";
  } catch (e) {
    showError(e.message || "Request failed.");
  }
}

async function getExplanation() {
  if (!requireStudent()) return;
  try {
    const url = `${API_BASE}/explain/${studentId}`;
    console.log("Request:", url);
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    document.getElementById("error-msg").style.display = "none";
    hasExplanation = true;
    document.getElementById("exp-title").textContent = data.title;
    document.getElementById("exp-body").textContent = data.body;
    const list = document.getElementById("exp-concepts");
    list.innerHTML = "";
    data.key_concepts.forEach(function(concept) {
      const li = document.createElement("li");
      li.textContent = concept;
      list.appendChild(li);
    });
    document.getElementById("exp-difficulty").textContent = "Difficulty: " + data.difficulty_applied;
    document.getElementById("section-3").style.display = "block";
  } catch (e) {
    showError(e.message || "Request failed.");
  }
}

async function getEvaluation() {
  if (!requireStudent()) return;
  hasEvaluation = false;
  currentQuestions = [];
  selectedAnswers = [];
  try {
    const url = `${API_BASE}/evaluate/${studentId}`;
    console.log("Request:", url);
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    document.getElementById("error-msg").style.display = "none";
    currentQuestions = data.questions.map(function(q) {
      return { question: q.question, options: q.options };
    });
    selectedAnswers = Array(currentQuestions.length).fill(null);
    hasEvaluation = true;
    renderQuestions();
    document.getElementById("section-4").style.display = "block";
  } catch (e) {
    showError(e.message || "Request failed.");
  }
}

function renderQuestions() {
  const container = document.getElementById("questions-container");
  container.innerHTML = "";
  currentQuestions.forEach(function(item, i) {
    const div = document.createElement("div");
    const p = document.createElement("p");
    p.textContent = (i + 1) + ". " + item.question;
    div.appendChild(p);
    item.options.forEach(function(option) {
      const label = document.createElement("label");
      const input = document.createElement("input");
      input.type = "radio";
      input.name = "q" + i;
      input.value = option;
      input.setAttribute("onchange", "updateAnswer(" + i + ", this.value)");
      label.appendChild(input);
      label.appendChild(document.createTextNode(" " + option));
      div.appendChild(label);
    });
    container.appendChild(div);
  });
  document.getElementById("progress").textContent = "Answered 0 / 10";
}

function updateAnswer(index, value) {
  selectedAnswers[index] = value;
  const answered = selectedAnswers.filter(function(a) { return a !== null; }).length;
  document.getElementById("progress").textContent = "Answered " + answered + " / 10";
}

async function submitCorrection() {
  if (!requireStudent()) return;
  if (!requireEvaluation()) return;
  if (!requireAllAnswered()) return;
  try {
    const url = `${API_BASE}/correct/${studentId}`;
    console.log("Request:", url);
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ questions: currentQuestions, answers: selectedAnswers })
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    document.getElementById("error-msg").style.display = "none";
    document.getElementById("result-score").textContent = "Score: " + data.score;
    document.getElementById("result-decision").textContent = "Decision: " + data.decision;
    document.getElementById("section-5").style.display = "block";
  } catch (e) {
    showError(e.message || "Request failed.");
  }
}

function requireStudent() {
  if (!studentId) { showError("Create a student first."); return false; }
  return true;
}

function requireEvaluation() {
  if (!hasEvaluation) { showError("Run evaluation first."); return false; }
  return true;
}

function requireAllAnswered() {
  if (selectedAnswers.some(function(a) { return a === null; })) {
    showError("Answer all 10 questions before submitting.");
    return false;
  }
  return true;
}

function showError(message) {
  const el = document.getElementById("error-msg");
  el.textContent = message;
  el.style.display = "block";
}

// Expose functions called from inline HTML onclick/onchange attributes
window.createStudent = createStudent;
window.getExplanation = getExplanation;
window.getEvaluation = getEvaluation;
window.submitCorrection = submitCorrection;
window.updateAnswer = updateAnswer;
