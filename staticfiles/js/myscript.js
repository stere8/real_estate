(function () {
  'use strict';

  const forms = document.querySelectorAll('.requires-validation');
  Array.from(forms).forEach(function (form) {
    // Add event listeners for each form element
    const elements = form.querySelectorAll('input, select, textarea');
    elements.forEach(function (element) {
      element.addEventListener('change', function (event) {
        element.checkValidity(); // Check validity on change
        if (element.validity.valid) {
          element.classList.remove('invalid-feedback');
          element.classList.add('valid-feedback');
        } else {
          element.classList.remove('valid-feedback');
          element.classList.add('invalid-feedback');
        }
      });
    });

    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated'); // Add class on submit for styling
    });
  });
})();
