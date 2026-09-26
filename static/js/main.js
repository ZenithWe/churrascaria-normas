const toggle = document.querySelector('.menu-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) {
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    links.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
}

const dateField = document.querySelector('input[type="date"]');
if (dateField) dateField.min = new Date().toISOString().split('T')[0];

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
