fetch("/crypto/bitcoin")
  .then((response) => response.json())
  .then((data) => {
    document.getElementById("crypto-price").innerText = `
            Name: ${data.name}
            Symbol: ${data.symbol}
            Price: $${data.current_price}
            Market Cap: $${data.market_cap}
            24h Change: ${data["24h_change"]}%
        `;
  })
  .catch((error) => console.error("Error fetching data:", error));
