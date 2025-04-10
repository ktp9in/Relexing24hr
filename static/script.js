async function submitQRCode() {
  const qrInput = document.getElementById('qrInput');
  const qrCode = qrInput.value.trim();
  const resultDiv = document.getElementById('result');

  if (!qrCode) {
      resultDiv.textContent = 'Please enter a QR code.';
      resultDiv.className = 'text-danger mt-4 text-center fs-5';
      return;
  }

  try {
      const response = await fetch('/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ qr_code: qrCode })
      });

      const data = await response.json();

      if (data.result?.startsWith('OK') || data.result?.startsWith('New')) {
          resultDiv.textContent = data.result;
          resultDiv.className = 'text-success mt-4 text-center fs-5';
      } else {
          resultDiv.textContent = data.result || 'Unexpected response';
          resultDiv.className = 'text-warning mt-4 text-center fs-5';
      }

      qrInput.value = '';
      loadData(); // Refresh table after every scan

  } catch (error) {
      resultDiv.textContent = 'Error contacting server.';
      resultDiv.className = 'text-danger mt-4 text-center fs-5';
      console.error(error);
  }
}

async function loadData() {
  const tableBody = document.getElementById('scanLog');
  tableBody.innerHTML = '';

  try {
      const res = await fetch('/data');
      const data = await res.json();

      data.forEach(item => {
          const row = document.createElement('tr');
          row.innerHTML = `
              <td>${item.qr_code}</td>
              <td>${item.in_time || ''}</td>
              <td>${item.out_time || ''}</td>
              <td>${item.duration || ''}</td>
              <td class="${item.status === 'Pass' ? 'text-bg-success' : item.status === 'Fail' ? 'text-bg-danger' : 'text-bg-warning'} text-center">${item.status}</td>
          `;
          tableBody.appendChild(row);
      });
  } catch (err) {
      console.error('Failed to load data:', err);
  }
}

window.onload = loadData;
