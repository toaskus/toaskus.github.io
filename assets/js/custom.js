// Scroll reveal animation
(function() {
  var items = document.querySelectorAll('.list__item');
  if (!items.length) return;

  items.forEach(function(item) {
    item.classList.add('reveal-on-scroll');
  });

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  items.forEach(function(item) {
    observer.observe(item);
  });
})();
