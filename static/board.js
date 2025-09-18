// Persistent Dark Mode
  const body = document.body;
  const darkModeBtn = document.querySelector('.dark-mode-btn');
  if(localStorage.getItem('darkMode') === 'true') body.classList.add('dark-mode');
  darkModeBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
  });

  // Drag & drop
  let draggedTask = null;
  document.querySelectorAll('.task').forEach(task => {
    task.addEventListener('dragstart', () => { draggedTask = task; task.style.opacity = '0.5'; });
    task.addEventListener('dragend', () => { draggedTask = null; task.style.opacity = '1'; });
  });
  document.querySelectorAll('.column').forEach(col => {
    col.addEventListener('dragover', e => e.preventDefault());
    col.addEventListener('drop', () => {
      if (!draggedTask) return;
      col.appendChild(draggedTask);
      fetch("{% url 'update_task_status' %}", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": "{{ csrf_token }}" },
        body: `task_id=${draggedTask.dataset.id}&status=${col.dataset.status}`
      }).then(res => res.json()).then(data => { if (!data.success) alert("Error updating task!"); });
    });
  });

  // Filter functionality
  const filterAssigned = document.getElementById('filter-assigned');
  const filterDeadline = document.getElementById('filter-deadline');
  const filterBtn = document.getElementById('filter-btn');
  const resetBtn = document.getElementById('reset-btn');

  function applyFilter() {
    const assignedVal = filterAssigned.value.trim().toLowerCase();
    const deadlineVal = filterDeadline.value; // YYYY-MM-DD
    document.querySelectorAll('.task').forEach(task => {
      const assignedTo = task.querySelector('.assigned').textContent.trim().toLowerCase();
      let taskDeadline = task.querySelector('.deadline').textContent.trim();
      if (taskDeadline.includes(' ')) taskDeadline = taskDeadline.split(' ')[0];
      let show = true;
      if (assignedVal && !assignedTo.includes(assignedVal)) show = false;
      if (deadlineVal && taskDeadline !== deadlineVal) show = false;
      task.style.display = show ? 'block' : 'none';
    });
  }

  filterBtn.addEventListener('click', applyFilter);
  resetBtn.addEventListener('click', () => {
    filterAssigned.value = '';
    filterDeadline.value = '';
    document.querySelectorAll('.task').forEach(task => task.style.display = 'block');
  });