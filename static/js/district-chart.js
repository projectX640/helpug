/* Render the operations overview's district volume chart. */
(function () {
  const canvas = document.getElementById("district-case-chart");
  const source = document.getElementById("district-chart-data");
  if (!canvas || !source || typeof Chart === "undefined") return;

  const districts = JSON.parse(source.textContent);
  const canvasShell = canvas.parentElement;
  const labels = districts.map((district) => district.label);
  const values = districts.map((district) => district.count);
  const context = canvas.getContext("2d");
  const fill = context.createLinearGradient(0, 0, 0, 280);

  fill.addColorStop(0, "rgba(112, 164, 199, .38)");
  fill.addColorStop(1, "rgba(218, 235, 244, .06)");

  if (labels.length > 6) canvasShell.style.width = `${Math.max(720, labels.length * 72)}px`;

  new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Cases",
        data: values,
        backgroundColor: fill,
        borderColor: "#6e9fc2",
        borderWidth: 4,
        pointBackgroundColor: "#fff",
        pointBorderColor: "#6e9fc2",
        pointBorderWidth: 4,
        pointRadius: 8,
        pointHoverRadius: 10,
        tension: 0.32,
        fill: true,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {duration: 650, easing: "easeOutQuart"},
      interaction: {mode: "index", intersect: false},
      layout: {padding: {top: 12, right: 18, bottom: 4, left: 8}},
      plugins: {
        legend: {display: false},
        tooltip: {
          displayColors: false,
          callbacks: {label: (context) => `${context.parsed.y} active case${context.parsed.y === 1 ? "" : "s"}`},
        },
      },
      scales: {
        x: {
          title: {display: true, text: "District", color: "#536170", font: {weight: "600"}},
          grid: {color: "rgba(112, 145, 166, .18)", drawBorder: false},
          ticks: {color: "#58718a", maxRotation: 40, minRotation: 0, autoSkip: false, font: {size: 11, weight: "600"}},
        },
        y: {
          beginAtZero: true,
          title: {display: true, text: "Cases", color: "#536170", font: {weight: "600"}},
          grid: {color: "rgba(112, 145, 166, .2)", drawBorder: false},
          border: {display: false},
          ticks: {color: "#58718a", precision: 0, stepSize: 1, padding: 8},
        },
      },
    },
  });
}());
