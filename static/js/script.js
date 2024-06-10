document.addEventListener("DOMContentLoaded", () => {
  const selectElement = document.getElementById("blogFilterSelect");
  if (selectElement) {
    selectElement.addEventListener("change", function () {
      document.getElementById("blogFilterForm").submit();
    });
  }

  // Flask alert message handling
  const alerts = document.querySelectorAll(".alert");
  if (alerts) {
    setTimeout(() => {
      alerts.forEach((alert) => {
        alert.remove();
      });
    }, 4000);
  }
});

// Form Validation
const form = document.getElementById("form");

if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    isValid = true;

    // Name validation
    const name = document.getElementById("name");
    const nameError = document.getElementById("nameError");
    const nameError1 = document.getElementById("nameError1");
    nameError.textContent = "";
    nameError1.textContent = "";
    if (name.value === "" || name.value === null) {
      nameError.textContent = "Please enter name";
      isValid = false;
    } else if (name.value.length >= 35) {
      nameError1.textContent = "Please enter valid name";
    }
    // Email validation
    const email = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const emailError1 = document.getElementById("emailError1");
    const emailPattern = /@/;
    if (email && emailError && emailPattern) {
      emailError.textContent = "";
      emailError1.textContent = "";

      if (email.value === "" || email.value === null) {
        emailError.textContent = "Please enter email";
        isValid = false;
      } else if (!emailPattern.test(email.value) || email.value >= 35) {
        emailError1.textContent = "Plase enter valid email";
        isValid = false;
      }
    }
    // Password validation
    const password = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const passwordError1 = document.getElementById("passwordError1");
    const passwordPattern = /(?=.*[a-z])(?=.*[0-9]).{8,}/;
    passwordError.textContent = "";
    passwordError1.textContent = "";
    if (password && passwordError && passwordError1) {
      if (password.value === "" || password.value === null) {
        passwordError.textContent = "Please enter password";
        isValid = false;
      } else if (!passwordPattern.test(password.value)) {
        passwordError1.textContent =
          "Password must be atleast 8 characters long, contain atleast one uppercase letter, one lowercase letter and one digit";
        isValid = false;
      }
    }

    // Address Validation
    const address = document.getElementById("address");
    const addressError = document.getElementById("addressError");
    const addressError1 = document.getElementById("addressError1");
    addressPattern = /(?=.*[A-za-z])(?=.*[0-9])/;
    if (address && addressError && addressError1) {
      addressError.textContent = "";
      addressError1.textContent = "";
      if (address.value === "" || address.value === null) {
        addressError.textContent = "Please enter address";
        isValid = false;
      } else if (!addressPattern.test(address.value)) {
        addressError1.textContent =
          "Address must have atleast one letter and one digit";
        isValid = false;
      }
    }
    // Bio Validation
    const bio = document.getElementById("bio");
    const bioError = document.getElementById("bioError");
    const bioError1 = document.getElementById("bioError1");
    const bioPattern = /.{3,}/;
    if (bio && bioError && bioError1) {
      bioError.textContent = "";
      bioError1.textContent = "";

      if (bio.value === "" || bio.value === null) {
        bioError.textContent = "Please enter bio";
        isValid = false;
      } else if (!bioPattern.test(bio.value)) {
        bioError1.textContent = "Bio must be atleast 3 characters long";
        isValid = false;
      }
    }
    // Date of birth Validation
    const dob = document.getElementById("dob");
    const dobError = document.getElementById("dobError");
    if (dob && dobError) {
      dobError.textContent = "";
      if (!dob.value) {
        dobError.textContent = "Please enter a date of birth";
        isValid = false;
      }
    }
    console.log(isValid);
    if (isValid) {
      form.submit();
    }
  });
}
