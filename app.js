(() => {
  const form = document.getElementById('resume-form');
  const fileInput = document.getElementById('resumes');
  const selectedFiles = document.getElementById('selected-files');
  const uploadZone = document.getElementById('upload-zone');
  const description = document.getElementById('job_description');
  const descriptionCount = document.getElementById('description-count');
  const submitButton = document.getElementById('submit-button');
  let chosenFiles = [];

  const readableSize = (size) => {
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
  };

  const renderFiles = () => {
    if (!selectedFiles) return;
    selectedFiles.replaceChildren();
    if (!chosenFiles.length) {
      const empty = document.createElement('span');
      empty.className = 'file-empty';
      empty.textContent = 'No files selected yet';
      selectedFiles.appendChild(empty);
      return;
    }
    chosenFiles.forEach((file, index) => {
      const row = document.createElement('div');
      row.className = 'file-item';
      const type = document.createElement('span');
      type.className = 'file-type';
      type.textContent = file.name.toLowerCase().endsWith('.pdf') ? 'PDF' : 'DOCX';
      const meta = document.createElement('div');
      meta.className = 'file-meta';
      const name = document.createElement('strong');
      name.textContent = file.name;
      const size = document.createElement('small');
      size.textContent = readableSize(file.size);
      meta.append(name, size);
      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'file-remove';
      remove.setAttribute('aria-label', `Remove ${file.name}`);
      remove.textContent = '×';
      remove.addEventListener('click', () => {
        chosenFiles.splice(index, 1);
        syncInputFiles();
        renderFiles();
      });
      row.append(type, meta, remove);
      selectedFiles.appendChild(row);
    });
  };

  const syncInputFiles = () => {
    if (!fileInput) return;
    const transfer = new DataTransfer();
    chosenFiles.forEach((file) => transfer.items.add(file));
    fileInput.files = transfer.files;
  };

  const addFiles = (fileList) => {
    const incoming = Array.from(fileList || []);
    for (const file of incoming) {
      if (!/\.(pdf|docx)$/i.test(file.name)) {
        window.alert(`${file.name}: please choose a PDF or DOCX file.`);
        continue;
      }
      if (chosenFiles.some((current) => current.name === file.name && current.size === file.size)) continue;
      chosenFiles.push(file);
    }
    if (chosenFiles.length > 10) {
      window.alert('This prototype supports up to 10 resumes per analysis. Extra files were removed.');
      chosenFiles = chosenFiles.slice(0, 10);
    }
    const totalBytes = chosenFiles.reduce((sum, file) => sum + file.size, 0);
    if (totalBytes > 16 * 1024 * 1024) {
      window.alert('The total file size is over 16 MB. Remove some files and try again.');
      chosenFiles = [];
    }
    syncInputFiles();
    renderFiles();
  };

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      addFiles(fileInput.files);
    });
  }

  if (uploadZone) {
    ['dragenter', 'dragover'].forEach((eventName) => uploadZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      uploadZone.classList.add('dragover');
    }));
    ['dragleave', 'drop'].forEach((eventName) => uploadZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      uploadZone.classList.remove('dragover');
    }));
    uploadZone.addEventListener('drop', (event) => addFiles(event.dataTransfer.files));
  }

  const updateDescriptionCount = () => {
    if (description && descriptionCount) descriptionCount.textContent = `${description.value.length} / 8000`;
  };
  if (description) {
    description.addEventListener('input', updateDescriptionCount);
    updateDescriptionCount();
  }

  if (form && submitButton) {
    form.addEventListener('submit', (event) => {
      const jobTitle = document.getElementById('job_title');
      if (!jobTitle.value.trim() || !description.value.trim() || !chosenFiles.length) {
        event.preventDefault();
        window.alert('Please enter a job title, job description, and at least one resume.');
        return;
      }
      submitButton.disabled = true;
      submitButton.innerHTML = '<span>◌</span> Analyzing resumes…';
    });
  }

  const searchInput = document.getElementById('candidate-search');
  const rows = Array.from(document.querySelectorAll('#candidate-table-body tr'));
  const noResults = document.getElementById('no-search-results');
  if (searchInput && rows.length) {
    searchInput.addEventListener('input', () => {
      const term = searchInput.value.trim().toLowerCase();
      let visible = 0;
      rows.forEach((row) => {
        const match = (row.dataset.search || '').includes(term);
        row.classList.toggle('hidden', !match);
        if (match) visible++;
      });
      if (noResults) noResults.classList.toggle('hidden', visible > 0);
    });
  }

  const csvButton = document.getElementById('download-csv');
  if (csvButton && rows.length) {
    csvButton.addEventListener('click', () => {
      const headers = ['Rank', 'Candidate', 'Filename', 'Match score (%)', 'Matched skills', 'Missing skills', 'Text similarity (%)'];
      const records = rows.filter((row) => !row.classList.contains('hidden')).map((row) => {
        const cells = row.querySelectorAll('td');
        return [
          cells[0]?.innerText.trim() || '',
          cells[1]?.querySelector('strong')?.innerText.trim() || '',
          cells[1]?.querySelector('div span')?.innerText.trim() || '',
          cells[2]?.querySelector('strong')?.innerText.replace('%', '').trim() || '',
          Array.from(cells[3]?.querySelectorAll('.skill-chip') || []).map((item) => item.innerText.trim()).join('; '),
          Array.from(cells[4]?.querySelectorAll('.skill-chip') || []).map((item) => item.innerText.trim()).join('; '),
          cells[5]?.innerText.replace('%', '').trim() || ''
        ];
      });
      const escapeCell = (value) => `"${String(value).replace(/"/g, '""')}"`;
      const csv = [headers, ...records].map((record) => record.map(escapeCell).join(',')).join('\r\n');
      const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'talentlens-candidate-results.csv';
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    });
  }
})();
