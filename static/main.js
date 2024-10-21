let volumeUpdateInterval = 100; // Valor padrão de 500 ms
let volumeIntervalId; // Variável para armazenar o ID do intervalo

function updateVolume() {
  fetch("/get_volume")
    .then((response) => response.json())
    .then((data) => {
      const volume = Math.min(data.volume, 10);
      const height = Math.max(0, ((volume + 60) / 60) * 100);
      const volumeLevel = document.getElementById("volume-level");
      volumeLevel.style.height = height + "%";

      if (height < 45) {
        volumeLevel.style.backgroundColor = "#4caf50"; // Verde
      } else if (height < 80) {
        volumeLevel.style.backgroundColor = "#ffeb3b"; // Amarelo
      } else {
        volumeLevel.style.backgroundColor = "#f44336"; // Vermelho
      }
    });
}

function selectDevice(deviceId) {
  fetch(`/set_device/${deviceId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("selected-device").innerText = deviceId;
        document.getElementById("stop-capture-btn").style.display = "block";

        const buttons = document.querySelectorAll(".device-list button");
        buttons.forEach((button) => {
          button.classList.remove("active");
        });

        document.getElementById(`device-${deviceId}`).classList.add("active");
      }
    });
}

document
  .getElementById("stop-capture-btn")
  .addEventListener("click", function () {
    fetch("/stop_capture", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Captação parada com sucesso!");
          this.style.display = "none";

          document.getElementById("selected-device").innerText = "Nenhum";

          const volumeLevel = document.getElementById("volume-level");
          volumeLevel.style.height = "0%";
          volumeLevel.style.backgroundColor = "#777";

          const activeButton = document.querySelector(
            ".device-list button.active"
          );
          if (activeButton) {
            activeButton.classList.remove("active");
          }
        }
      });
  });

function updateVolumeInterval() {
  const selectedValue = document.getElementById("update-interval").value;
  volumeUpdateInterval = parseInt(selectedValue);

  clearInterval(volumeIntervalId);

  volumeIntervalId = setInterval(updateVolume, volumeUpdateInterval);
}

volumeIntervalId = setInterval(updateVolume, volumeUpdateInterval);
