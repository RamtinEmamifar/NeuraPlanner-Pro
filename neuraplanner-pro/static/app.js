/**
 * NeuraPlanner Pro - frontend logic.
 * Talks to the Flask API and re-renders the UI after every change.
 */

// ---------- API wrapper ----------
const API = {
    getTasks: () =>
        fetch('/get_tasks').then(r => r.json()),

    addTask: (title, priority) =>
        fetch('/add_task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, priority }),
        }).then(r => r.json()),

    completeTask: (id) =>
        fetch('/complete_task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id }),
        }).then(r => r.json()),

    getProgress: () =>
        fetch('/get_progress').then(r => r.json()),

    getPlan: () =>
        fetch('/get_plan').then(r => r.json()),
};

// ---------- DOM references ----------
const el = {
    form:         document.getElementById('task-form'),
    title:        document.getElementById('task-title'),
    priority:     document.getElementById('task-priority'),
    taskList:     document.getElementById('task-list'),
    planList:     document.getElementById('plan-list'),
    progressFill: document.getElementById('progress-fill'),
    progressMeta: document.getElementById('progress-meta'),
    statPercent:  document.getElementById('stat-percent'),
    statRemaining:document.getElementById('stat-remaining'),
    regenerate:   document.getElementById('regenerate-plan'),
};

// ---------- Render helpers ----------
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function renderTasks(tasks) {
    if (!tasks.length) {
        el.taskList.innerHTML = '<li class="task-empty">No tasks yet.</li>';
        return;
    }

    el.taskList.innerHTML = tasks
        .map(t => `
            <li class="task-item ${t.completed ? 'completed' : ''}" data-id="${t.id}">
                <button class="task-check" aria-label="Complete task"></button>
                <span class="task-title-text">${escapeHtml(t.title)}</span>
                <span class="task-priority-tag" data-priority="${t.priority}">${t.priority}</span>
            </li>
        `)
        .join('');

    // Wire up the new check buttons.
    el.taskList.querySelectorAll('.task-item').forEach(item => {
        const id = Number(item.dataset.id);
        item.querySelector('.task-check').addEventListener('click', async () => {
            if (item.classList.contains('completed')) return;
            await API.completeTask(id);
            await refresh();
        });
    });
}

function renderProgress({ percent, completed, total, remaining }) {
    el.progressFill.style.width = `${percent}%`;
    el.progressMeta.textContent = `${completed} of ${total} completed`;
    el.statPercent.textContent  = `${percent}%`;
    el.statRemaining.textContent = remaining;
}

function renderPlan(plan) {
    if (!plan.length) {
        el.planList.innerHTML = '<li class="plan-empty">Add a task to generate your plan.</li>';
        return;
    }

    el.planList.innerHTML = plan
        .map(p => `
            <li class="plan-item" data-priority="${p.priority}">
                <span class="plan-slot">${p.slot}</span>
                <span class="plan-title">${escapeHtml(p.title)}</span>
                <span class="plan-priority">${p.priority}</span>
            </li>
        `)
        .join('');
}

// ---------- Main refresh loop ----------
async function refresh() {
    try {
        const [{ tasks }, progress, { plan }] = await Promise.all([
            API.getTasks(),
            API.getProgress(),
            API.getPlan(),
        ]);
        renderTasks(tasks);
        renderProgress(progress);
        renderPlan(plan);
    } catch (err) {
        console.error('Failed to refresh UI', err);
    }
}

// ---------- Event wiring ----------
el.form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = el.title.value.trim();
    if (!title) return;
    await API.addTask(title, el.priority.value);
    el.form.reset();
    el.priority.value = 'medium';
    el.title.focus();
    await refresh();
});

el.regenerate.addEventListener('click', refresh);

// First paint
refresh();
