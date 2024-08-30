function fetchBitcoinPrice() {
  fetch("/crypto/bitcoin")
    .then((response) => response.json())
    .then((data) => {
      const priceElement = document.getElementById("crypto-price");
      const detailsElement = document.getElementById("bitcoin-details");
      const lastUpdatedElement = document.getElementById(
        "bitcoin-last-updated"
      );

      if (data && data.name === "Bitcoin" && data.current_price !== undefined) {
        priceElement.innerText = `$${data.current_price.toFixed(2)}`;
        detailsElement.innerHTML = `
                  <p>Name: ${data.name}</p>
                  <p>Symbol: ${data.symbol}</p>
                  <p>Market Cap: $${data.market_cap}</p>
                  <p>24h Change: ${data["24h_change"]}%</p>
              `;
        lastUpdatedElement.innerText = new Date().toLocaleString();
      } else {
        console.error("Unexpected data for Bitcoin:", data);
        resetBitcoinData();
      }
    })
    .catch((error) => {
      console.error("Error fetching Bitcoin data:", error);
      resetBitcoinData();
    });
}

function fetchDogecoinPrice() {
  fetch("/crypto/dogecoin")
    .then((response) => response.json())
    .then((data) => {
      const priceElement = document.getElementById("crypto-price-dogecoin");
      const detailsElement = document.getElementById("dogecoin-details");
      const lastUpdatedElement = document.getElementById(
        "dogecoin-last-updated"
      );

      if (
        data &&
        data.name === "Dogecoin" &&
        data.current_price !== undefined
      ) {
        priceElement.innerText = `$${data.current_price.toFixed(4)}`;
        detailsElement.innerHTML = `
                  <p>Name: ${data.name}</p>
                  <p>Symbol: ${data.symbol}</p>
                  <p>Market Cap: $${data.market_cap}</p>
                  <p>24h Change: ${data["24h_change"]}%</p>
              `;
        lastUpdatedElement.innerText = new Date().toLocaleString();
      } else {
        console.error("Unexpected data for Dogecoin:", data);
        resetDogecoinData();
      }
    })
    .catch((error) => {
      console.error("Error fetching Dogecoin data:", error);
      resetDogecoinData();
    });
}

function resetBitcoinData() {
  document.getElementById("crypto-price").innerText = "Loading...";
  document.getElementById("bitcoin-details").innerHTML =
    "<p>Data not available</p>";
  document.getElementById("bitcoin-last-updated").innerText = "Never";
}

function resetDogecoinData() {
  document.getElementById("crypto-price-dogecoin").innerText = "Loading...";
  document.getElementById("dogecoin-details").innerHTML =
    "<p>Data not available</p>";
  document.getElementById("dogecoin-last-updated").innerText = "Never";
}

function startTimer(timerElement, fetchFunction) {
  let timeLeft = 50;
  setInterval(() => {
    timeLeft -= 1;
    timerElement.innerText = timeLeft;
    if (timeLeft <= 0) {
      fetchFunction();
      timeLeft = 50; // Reset timer
    }
  }, 1000);
}

// Inicialização e execução dos timers
fetchBitcoinPrice(); // Carrega dados iniciais para Bitcoin
fetchDogecoinPrice(); // Carrega dados iniciais para Dogecoin

startTimer(document.getElementById("bitcoin-timer"), fetchBitcoinPrice);
startTimer(document.getElementById("dogecoin-timer"), fetchDogecoinPrice);
