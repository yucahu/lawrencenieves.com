// Small conveniences. Every page works without this file.
(function () {
  // Keep the current project in view in the index.
  var current = document.querySelector('.index-list [aria-current="page"]');
  if (current && current.scrollIntoView) current.scrollIntoView({ block: 'nearest' });

  // Left and right arrow keys move between projects.
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
    var tag = (e.target && e.target.tagName) || '';
    if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
    var rel = e.key === 'ArrowLeft' ? 'prev' : e.key === 'ArrowRight' ? 'next' : null;
    if (!rel) return;
    var link = document.querySelector('a[rel="' + rel + '"]');
    if (link) location.href = link.href;
  });

  // Projects landing: hovering or focusing a title previews it.
  var preview = document.querySelector('.preview');
  if (!preview) return;
  var fig = preview.querySelector('figure');
  var img = preview.querySelector('img');
  var imgLink = preview.querySelector('figure a');
  var cap = preview.querySelector('figcaption');
  var name = preview.querySelector('.name');
  var meta = preview.querySelector('.preview-text .meta');
  var role = preview.querySelector('.preview-text .role');
  var text = preview.querySelector('.preview-text');
  var hint = document.querySelector('.hint');
  var links = document.querySelectorAll('.index-list a');

  function show(a) {
    var d = a.dataset;
    if (d.img) {
      img.src = d.img;
      img.width = d.w;
      img.height = d.h;
      img.alt = d.cap || '';
      imgLink.href = a.href;
      cap.textContent = d.cap || '';
      fig.hidden = false;
    } else {
      fig.hidden = true;
    }
    name.textContent = a.querySelector('.t').textContent;
    meta.textContent = d.meta || '';
    role.textContent = d.role || '';
    text.hidden = false;
    if (hint) hint.hidden = true;
  }

  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('mouseenter', function () { show(this); });
    links[i].addEventListener('focus', function () { show(this); });
  }

  // Warm the cache so previews appear instantly.
  window.addEventListener('load', function () {
    for (var i = 0; i < links.length; i++) {
      if (links[i].dataset.img) { var im = new Image(); im.src = links[i].dataset.img; }
    }
  });
})();
