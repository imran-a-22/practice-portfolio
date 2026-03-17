function calculateTotal() {
  const amount = parseFloat(document.getElementById("amount").value) || 0;
  const processing = parseFloat(document.getElementById("processing").value) || 0;
  const markup = parseFloat(document.getElementById("markup").value) || 0;

  const processingFee = amount * (processing / 100);
  const markupFee = amount * (markup / 100);
  const totalPayable = amount + processingFee + markupFee;

  document.getElementById("processingFee").textContent = processingFee.toFixed(2);
  document.getElementById("markupFee").textContent = markupFee.toFixed(2);
  document.getElementById("totalPayable").textContent = totalPayable.toFixed(2);
}