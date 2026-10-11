(function () {
  const cards = document.querySelectorAll('.overview-grid .stat-card, [data-district-sparkline]');
  const namespace = 'http://www.w3.org/2000/svg';
  const patterns = [
    [31, 27, 29, 21, 24, 15, 18],
    [30, 25, 27, 18, 21, 13, 10],
    [32, 28, 30, 24, 19, 21, 14],
    [31, 29, 25, 27, 18, 20, 12]
  ];

  cards.forEach((card, index) => {
    const isDistrictCard = card.hasAttribute('data-district-sparkline');
    if (!isDistrictCard && card.querySelector('.stat-sparkline')) return;

    const valueNode = isDistrictCard ? null : card.querySelector('strong');
    const valueText = isDistrictCard ? card.dataset.sparklineValue : valueNode && valueNode.textContent;
    const value = Number.parseInt(valueText, 10) || 0;
    const wrapper = document.createElement('span');
    const graph = document.createElementNS(namespace, 'svg');
    const path = document.createElementNS(namespace, 'path');
    const point = document.createElementNS(namespace, 'circle');
    const label = document.createElement('small');
    const points = patterns[index % patterns.length];

    wrapper.className = isDistrictCard ? 'stat-sparkline district-card-sparkline' : 'stat-sparkline';
    wrapper.title = `Live reading: ${value} case${value === 1 ? '' : 's'}`;
    if (isDistrictCard) wrapper.setAttribute('aria-label', card.getAttribute('aria-label') || `Live reading: ${value} cases`);
    graph.setAttribute('viewBox', '0 0 96 42');
    graph.setAttribute('role', 'img');
    graph.setAttribute('aria-label', `Live reading: ${value} cases`);
    path.setAttribute('d', points.map((y, pointIndex) => `${pointIndex ? 'L' : 'M'} ${pointIndex * 15 + 2} ${y}`).join(' '));
    point.setAttribute('cx', '92');
    point.setAttribute('cy', String(points[points.length - 1]));
    point.setAttribute('r', '4');
    label.textContent = `LIVE · ${value}`;

    graph.append(path, point);
    wrapper.append(graph, label);
    if (isDistrictCard) {
      card.replaceWith(wrapper);
    } else {
      card.appendChild(wrapper);
    }
  });
})();
