function fetchBitcoinPrice() {
  fetch("/crypto/bitcoin")
    .then((response) => response.json())
    .then((data) => {
      const priceElement = document.getElementById("crypto-price");

      // Verificar se os dados estão corretos antes de atualizar o DOM
      if (data && data.current_price !== undefined) {
        // Limpar o conteúdo anterior para evitar duplicação
        priceElement.innerText = `
            Name: ${data.name}
            Symbol: ${data.symbol}
            Price: $${data.current_price}
            Market Cap: $${data.market_cap}
            24h Change: ${data["24h_change"]}%
        `;
      } else {
        console.error("Data format error:", data);
      }
    })
    .catch((error) => console.error("Error fetching data:", error));
}

// Atualizar o preço a cada 5 segundos
setInterval(fetchBitcoinPrice, 5000);
function fetchBitcoinPrice() {
  fetch("/crypto/bitcoin")
    .then((response) => response.json())
    .then((data) => {
      const priceElement = document.getElementById("crypto-price");

      // Verificar se os dados estão corretos antes de atualizar o DOM
      if (data && data.current_price !== undefined) {
        // Limpar o conteúdo anterior para evitar duplicação
        priceElement.innerText = `
            Name: ${data.name}
            Symbol: ${data.symbol}
            Price: $${data.current_price}
            Market Cap: $${data.market_cap}
            24h Change: ${data["24h_change"]}%
        `;
      } else {
        console.error("Data format error:", data);
      }
    })
    .catch((error) => console.error("Error fetching data:", error));
}

// Atualizar o preço a cada 50 segundos
setInterval(fetchBitcoinPrice, 50000);
