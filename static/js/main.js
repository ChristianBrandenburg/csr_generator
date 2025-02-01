document.addEventListener("DOMContentLoaded", function () {
    // Check if the current page is "/csrgen"
    if (window.location.pathname === "/csrgen") {
        setRSAKeySizes(); // Load RSA key sizes only on /csrgen page

        // Add event listener for key type selection
        const keyTypeSelect = document.getElementById("keyType");
        if (keyTypeSelect) {
            keyTypeSelect.addEventListener("change", function () {
                if (this.value === "RSA") {
                    setRSAKeySizes();
                } else if (this.value === "ECC") {
                    setECCKeySizes();
                }
            });
        }
    }

    // Validate that the country field is a valid two-letter country code
    const countryInput = document.getElementById("country");
    if (countryInput) {
        countryInput.addEventListener("input", function (e) {
            const value = e.target.value;
            if (value.length !== 2 || !/^[A-Za-z]{2}$/.test(value)) {
                alert("Please enter a valid two-letter country code.");
                e.target.focus();
            }
        });
    }
});

// Function to set RSA Key Sizes
function setRSAKeySizes() {
    var select = document.getElementById("keySize");
    if (!select) return; // Prevent errors if element is missing
    select.innerHTML =
        "<option value='512'>512</option>" +
        "<option value='1024'>1024</option>" +
        "<option value='2048'>2048</option>" +
        "<option value='4096'>4096</option>" +
        "<option value='8192'>8192</option>";
    select.value = "2048"; // Default to 2048
}

// Function to set ECC Key Sizes
function setECCKeySizes() {
    var select = document.getElementById("keySize");
    if (!select) return; // Prevent errors if element is missing
    select.innerHTML =
        "<option value='192'>192</option>" +
        "<option value='224'>224</option>" +
        "<option value='256'>256</option>" +
        "<option value='384'>384</option>" +
        "<option value='521'>521</option>";
    select.value = "256"; // Default to 256
}

// Function to set profile settings
function setProfile(profile) {
    const groupCheckboxes = document.querySelectorAll("input.keyGroup[type='checkbox']");
    groupCheckboxes.forEach(function (checkbox) {
        checkbox.checked = false;
    });

    if (profile === "SSL") {
        document.getElementById("digitalsignature").checked = true;
        document.getElementById("keyencipher").checked = true;
        document.getElementById("serverauth").checked = true;
        document.getElementById("clientauth").checked = true;
    }
    if (profile === "SMIME") {
        document.getElementById("digitalsignature").checked = true;
        document.getElementById("keyencipher").checked = true;
        document.getElementById("keyagree").checked = true;
        document.getElementById("nonrepudation").checked = true;
        document.getElementById("emailprotect").checked = true;
    }
    if (profile === "CODESIGN") {
        document.getElementById("digitalsignature").checked = true;
        document.getElementById("sign").checked = true;
        document.getElementById("timestamp").checked = true;
    }
    if (profile === "DOCUSIGN") {
        document.getElementById("digitalsignature").checked = true;
        document.getElementById("nonrepudation").checked = true;
        document.getElementById("sign").checked = true;
    }
}
