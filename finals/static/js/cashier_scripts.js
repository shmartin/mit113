document.addEventListener('DOMContentLoaded', function() {
    // --- Keypad and Change Calculation (adapted for Modal) ---
    const amountTenderedInput = document.getElementById('modal-amount-tendered'); // Input field in the modal
    // Select all buttons within the modal's keypad
    const keys = document.querySelectorAll('#payment-modal .keypad .key');
    const modalCalculatedChangeLabel = document.getElementById('modal-calculated-change'); // Change display in the modal
    const saleGrandTotalLabel = document.getElementById('sale-grand-total'); // Grand Total label on the main page
    const modalGrandTotalLabel = document.getElementById('modal-grand-total'); // Grand Total display in the modal
    const paymentModalMessage = document.getElementById('payment-modal-message'); // Message area in the modal (if you added it)

    // Get the grand total initially (will be updated when modal opens)
    let grandTotal = parseFloat(saleGrandTotalLabel.textContent.replace(/[^0-9.-]+/g,"")) || 0;


    // Add event listeners to all buttons within the modal's keypad
    keys.forEach(key => {
        key.addEventListener('click', function() {
            const currentValueString = amountTenderedInput.value;
            // Parse the current value as a float, default to 0 if empty or invalid
            let currentValue = parseFloat(currentValueString) || 0;
            const keyValue = this.value; // Get the value attribute of the clicked button

            // Handle special buttons first
            if (this.classList.contains('clear')) {
                amountTenderedInput.value = '';
                currentValue = 0; // Reset current value to 0
            } else if (this.classList.contains('backspace')) {
                // Backspace for this type of calculator is tricky.
                // If you want to remove the *last added denomination*, you'd need to track history.
                // A simpler backspace might just clear the field.
                // Let's make it clear the field for simplicity in this design.
                amountTenderedInput.value = '';
                currentValue = 0; // Reset current value to 0
                // If you prefer true backspace, you'd need a different input method or logic.
            }
            // Handle denomination buttons
            else {
                // Parse the value of the clicked denomination button as a float
                const denominationValue = parseFloat(keyValue);

                // Check if the parsed value is a valid number
                if (!isNaN(denominationValue)) {
                    // Add the denomination value to the current amount
                    currentValue += denominationValue;
                    // Update the input field with the new total amount
                    amountTenderedInput.value = currentValue.toFixed(2); // Format to 2 decimal places
                }
                // else, it's likely the "Exact" button or another special key without a numeric value
                // You could add specific logic for an "Exact" button here if needed.
                 // else if (this.classList.contains('exact')) {
                 //     amountTenderedInput.value = grandTotal.toFixed(2); // Set amount tendered to total
                 //     currentValue = grandTotal;
                 // }

            }

            // Update change calculation after input update
            updateModalChange();

            // Optional: Clear message area when input changes after a failed confirmation
            if (paymentModalMessage) {
                paymentModalMessage.textContent = '';
            }
            // Optional: Reset buttons if implementing two-step process
            // const confirmPaymentButton = document.getElementById('confirm-payment-button');
            // const completeSaleButton = document.getElementById('complete-sale-button');
            // if (confirmPaymentButton && completeSaleButton) {
            //     confirmPaymentButton.style.display = 'block';
            //     completeSaleButton.style.display = 'none';
            // }
        });
    });

     // Add event listener for manual input changes as well
     // This might be less common with denomination buttons, but good practice
    amountTenderedInput.addEventListener('input', function() {
         updateModalChange();
         // Optional: Clear message area and reset buttons when input changes
         if (paymentModalMessage) {
             paymentModalMessage.textContent = '';
         }
         // const confirmPaymentButton = document.getElementById('confirm-payment-button');
         // const completeSaleButton = document.getElementById('complete-sale-button');
         // if (confirmPaymentButton && completeSaleButton) {
         //     confirmPaymentButton.style.display = 'block';
         //     completeSaleButton.style.display = 'none';
         // }
    });


    // Function to calculate and update the change in the modal
    function updateModalChange() {
        const amountTendered = parseFloat(amountTenderedInput.value) || 0; // Parse as float
        const change = amountTendered - grandTotal;
        modalCalculatedChangeLabel.textContent = change.toFixed(2); // Display change formatted
    }


    // --- Modal Show/Hide Logic ---
    const paymentModal = document.getElementById('payment-modal');
    const openPaymentModalButton = document.getElementById('open-payment-modal');
    const closeButton = document.querySelector('#payment-modal .close-button');

    // Get the payment action buttons (if implementing two-step)
    // const confirmPaymentButton = document.getElementById('confirm-payment-button');
    // const completeSaleButton = document.getElementById('complete-sale-button');


    // Event listener to open the modal
    if (openPaymentModalButton) {
        openPaymentModalButton.addEventListener('click', function() {
            // Update the grand total in the modal just before showing it
            const currentGrandTotalText = saleGrandTotalLabel.textContent.replace(/[^0-9.-]+/g,"");
            grandTotal = parseFloat(currentGrandTotalText) || 0;

            modalGrandTotalLabel.textContent = `Php ${grandTotal.toFixed(2)}`;
            amountTenderedInput.value = ''; // Clear previous amount tendered
            updateModalChange(); // Calculate initial change

            // Optional: Reset buttons to initial state when modal opens
            // if (confirmPaymentButton && completeSaleButton) {
            //     confirmPaymentButton.style.display = 'block';
            //     completeSaleButton.style.display = 'none';
            // }
             // Optional: Clear message area
            // if (paymentModalMessage) {
            //     paymentModalMessage.textContent = '';
            // }

            paymentModal.style.display = 'block'; // Show the modal
        });
    }


    // Event listener to close the modal using the close button
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            paymentModal.style.display = 'none'; // Hide the modal
        });
    }


    // Close the modal if the user clicks outside of the modal content (on the overlay)
    if (paymentModal) {
        window.addEventListener('click', function(event) {
            if (event.target === paymentModal) {
                event.preventDefault();
                paymentModal.style.display = 'none';
            }
        });
    }


    // --- Optional: "Confirm Payment" Button Logic (if implementing two-step) ---
    // if (confirmPaymentButton && completeSaleButton && paymentModalMessage) {
    //     confirmPaymentButton.addEventListener('click', function() {
    //         const amountTendered = parseFloat(amountTenderedInput.value) || 0;
    //
    //         if (amountTendered >= grandTotal) {
    //             // Sufficient amount, hide Confirm, show Complete Sale
    //             paymentModalMessage.textContent = ''; // Clear any insufficient message
    //             confirmPaymentButton.style.display = 'none';
    //             completeSaleButton.style.display = 'block';
    //         } else {
    //             // Insufficient amount, display message
    //             const needed = (grandTotal - amountTendered).toFixed(2);
    //             paymentModalMessage.textContent = `Insufficient funds. Php ${needed} more needed.`;
    //             // Keep Confirm Payment visible, Complete Sale hidden
    //             confirmPaymentButton.style.display = 'block';
    //             completeSaleButton.style.display = 'none';
    //         }
    //     });
    // }


    // The "Complete Sale" button is a submit button.
    // Clicking it will submit the form #complete-sale-form-modal.
    // The server-side logic in your Django view handles the final completion.

});