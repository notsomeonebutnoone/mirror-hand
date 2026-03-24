const barsContainer = document.getElementById("finger-bars");
const latencyValue = document.getElementById("latency-value");
const waveContainer = document.getElementById("latency-wave");

const barCount = 5;
const waveCount = 14;

function createBars() {
  for (let i = 0; i < barCount; i += 1) {
    const bar = document.createElement("div");
    bar.className = "bar";
    bar.style.width = `${40 + i * 8}%`;
    barsContainer.appendChild(bar);
  }
  for (let i = 0; i < waveCount; i += 1) {
    const wave = document.createElement("div");
    wave.className = "wave-bar";
    wave.style.height = `${10 + Math.random() * 50}px`;
    waveContainer.appendChild(wave);
  }
}

function updateTelemetry() {
  const bars = barsContainer.querySelectorAll(".bar");
  bars.forEach((bar) => {
    const width = 40 + Math.random() * 60;
    bar.style.width = `${width}%`;
  });

  const latency = Math.round(12 + Math.random() * 18);
  latencyValue.textContent = latency;

  const waves = waveContainer.querySelectorAll(".wave-bar");
  waves.forEach((wave) => {
    wave.style.height = `${8 + Math.random() * 50}px`;
  });
}

createBars();
setInterval(updateTelemetry, 700);
