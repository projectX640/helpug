(function () {
  const svgs = document.querySelectorAll('.trend-svg, .mini-trend-box svg, .district-mini-graph svg');
  const namespace = 'http://www.w3.org/2000/svg';

  svgs.forEach((svg) => {
    const line = svg.querySelector('.trend-line-cases');
    if (!line || !line.points || svg.querySelector('.trend-node')) return;

    const nodes = document.createElementNS(namespace, 'g');
    nodes.setAttribute('aria-hidden', 'true');

    for (let index = 0; index < line.points.numberOfItems; index += 1) {
      const point = line.points.getItem(index);
      const node = document.createElementNS(namespace, 'circle');
      node.setAttribute('class', 'trend-node');
      node.setAttribute('cx', point.x);
      node.setAttribute('cy', point.y);
      node.setAttribute('r', '3.5');
      nodes.appendChild(node);
    }

    svg.appendChild(nodes);
  });
})();
