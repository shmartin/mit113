document.addEventListener('DOMContentLoaded', function() {
    const amountTenderedInput = document.getElementById('modal-amount-tendered');
    const keys = document.querySelectorAll('#payment-modal .keypad .key');
    const modalCalculatedChangeLabel = document.getElementById('modal-calculated-change');
    const saleGrandTotalLabel = document.getElementById('sale-grand-total');
    const modalGrandTotalLabel = document.getElementById('modal-grand-total');
    const paymentModalMessage = document.getElementById('payment-modal-message');

    let grandTotal = parseFloat(saleGrandTotalLabel.textContent.replace(/[^0-9.-]+/g,"")) || 0;


    keys.forEach(key => {
        key.addEventListener('click', function() {
            const currentValueString = amountTenderedInput.value;
            let currentValue = parseFloat(currentValueString) || 0;
            const keyValue = this.value;

            if (this.classList.contains('clear')) {
                amountTenderedInput.value = '';
                currentValue = 0; // Reset current value to 0
            } else if (this.classList.contains('backspace')) {

                amountTenderedInput.value = '';
                currentValue = 0;
            }
            else {
                const denominationValue = parseFloat(keyValue);

                if (!isNaN(denominationValue)) {
                    currentValue += denominationValue;
                    amountTenderedInput.value = currentValue.toFixed(2);
                }


            }

            updateModalChange();

            if (paymentModalMessage) {
                paymentModalMessage.textContent = '';
            }

        });
    });

    amountTenderedInput.addEventListener('input', function() {
         updateModalChange();
         if (paymentModalMessage) {
             paymentModalMessage.textContent = '';
         }

    });


    function updateModalChange() {
        const amountTendered = parseFloat(amountTenderedInput.value) || 0;
        const change = amountTendered - grandTotal;
        modalCalculatedChangeLabel.textContent = change.toFixed(2);
    }


    const paymentModal = document.getElementById('payment-modal');
    const openPaymentModalButton = document.getElementById('open-payment-modal');
    const closeButton = document.querySelector('#payment-modal .close-button');

    if (openPaymentModalButton) {
        openPaymentModalButton.addEventListener('click', function() {
            const currentGrandTotalText = saleGrandTotalLabel.textContent.replace(/[^0-9.-]+/g,"");
            grandTotal = parseFloat(currentGrandTotalText) || 0;

            modalGrandTotalLabel.textContent = `Php ${grandTotal.toFixed(2)}`;
            amountTenderedInput.value = '';
            updateModalChange();

             paymentModal.style.display = 'block';
        });
    }


    if (closeButton) {
        closeButton.addEventListener('click', function() {
            paymentModal.style.display = 'none';
        });
    }


    if (paymentModal) {
        window.addEventListener('click', function(event) {
            if (event.target === paymentModal) {
                event.preventDefault();
                paymentModal.style.display = 'none';
            }
        });
    }
});