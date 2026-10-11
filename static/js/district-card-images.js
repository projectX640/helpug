(function () {
  const cards = Array.from(document.querySelectorAll('[data-district-image-card]'));
  const cachePrefix = 'district-card-image:v2:';
  const cacheDuration = 7 * 24 * 60 * 60 * 1000;
  const knownImages = {
    masaka: 'https://commons.wikimedia.org/wiki/Special:FilePath/Equator%20Masaka.jpg?width=720',
    'masaka city': 'https://commons.wikimedia.org/wiki/Special:FilePath/Equator%20Masaka.jpg?width=720',
    mbarara: 'https://commons.wikimedia.org/wiki/Special:FilePath/Mbarara%20town%20monument.jpg?width=720',
    'mbarara city': 'https://commons.wikimedia.org/wiki/Special:FilePath/Mbarara%20town%20monument.jpg?width=720'
  };

  if (!cards.length) return;

  function normalizedName(name) {
    return name.trim().toLowerCase().replace(/\s+/g, ' ');
  }

  function cachedImage(name) {
    try {
      const cached = JSON.parse(window.localStorage.getItem(cachePrefix + normalizedName(name)) || 'null');
      if (cached && cached.url && Date.now() - cached.savedAt < cacheDuration) return cached.url;
    } catch (error) {
      return null;
    }
    return null;
  }

  function saveImage(name, url) {
    try {
      window.localStorage.setItem(cachePrefix + normalizedName(name), JSON.stringify({url, savedAt: Date.now()}));
    } catch (error) {
      return;
    }
  }

  function scorePage(page, name) {
    const title = (page.title || '').toLowerCase();
    const extension = title.split('.').pop();
    if (/map|locator|boundary|flag|logo|coat of arms|diagram|svg/.test(title)) return -100;
    let score = 0;
    if (title.includes(normalizedName(name))) score += 12;
    if (['jpg', 'jpeg', 'png', 'webp'].includes(extension)) score += 6;
    if (/landmark|monument|cathedral|town|street|market|park|lake|falls|bridge/.test(title)) score += 5;
    return score;
  }

  async function searchImage(name, query) {
    const endpoint = 'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=' + encodeURIComponent(query) + '&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url|mime&iiurlwidth=720&format=json&origin=*';
    const response = await fetch(endpoint, {headers: {Accept: 'application/json'}});
    if (!response.ok) return null;
    const payload = await response.json();
    const pages = Object.values((payload.query && payload.query.pages) || {});
    const candidates = pages.map((page) => {
      const imageInfo = page.imageinfo && page.imageinfo[0];
      return imageInfo && (imageInfo.thumburl || imageInfo.url) ? {page, url: imageInfo.thumburl || imageInfo.url} : null;
    }).filter(Boolean).sort((left, right) => scorePage(right.page, name) - scorePage(left.page, name));
    return candidates[0] && scorePage(candidates[0].page, name) >= 0 ? candidates[0].url : null;
  }

  async function findImage(name) {
    const directImage = knownImages[normalizedName(name)];
    if (directImage) return directImage;

    const queries = [
      name + ' Uganda landmark',
      name + ' Uganda monument',
      name + ' town Uganda',
      name + ' Uganda'
    ];
    for (const query of queries) {
      try {
        const image = await searchImage(name, query);
        if (image) return image;
      } catch (error) {
        continue;
      }
    }
    return null;
  }

  async function loadImage(card) {
    const name = card.dataset.districtName;
    const image = card.querySelector('img');
    if (!name || !image) return;

    const fallback = image.src;
    const cached = cachedImage(name);
    const imageUrl = cached || await findImage(name);
    if (!imageUrl) {
      card.classList.add('district-card-image-fallback');
      return;
    }

    image.onload = function () {
      card.classList.add('district-card-image-loaded');
    };
    image.onerror = function () {
      image.onerror = null;
      image.src = fallback;
      card.classList.add('district-card-image-fallback');
    };
    image.src = imageUrl;
    if (!cached) saveImage(name, imageUrl);
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, instance) => {
      entries.filter((entry) => entry.isIntersecting).forEach((entry) => {
        loadImage(entry.target);
        instance.unobserve(entry.target);
      });
    }, {rootMargin: '160px'});
    cards.forEach((card) => observer.observe(card));
  } else {
    cards.forEach(loadImage);
  }
})();
