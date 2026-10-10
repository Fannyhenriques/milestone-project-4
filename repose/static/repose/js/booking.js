const bookingType = document.getElementById("id_booking_type");
const treatmentField = document.getElementById("treatment-field");
const packageField = document.getElementById("package-field");


if (bookingType && treatmentField && packageField) {
  const updateBookingFields = () => {
    treatmentField.style.display = "none";
    packageField.style.display = "none";

    if (bookingType.value === "treatment") {
      treatmentField.style.display = "block";
    } else if (bookingType.value === "package") {
      packageField.style.display = "block";
    }
  };

  bookingType.addEventListener("change", updateBookingFields);
  updateBookingFields();
}

const dateInput = document.querySelector('input[type="date"]');

if (dateInput) {
  dateInput.addEventListener("click", () => {
    if (typeof dateInput.showPicker === "function") {
      dateInput.showPicker();
    }
  });
}