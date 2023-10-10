function setRSAKeySizes() {
    var select = document.getElementById("keySize");
    select.innerHTML = "<option value='512'>512</option><option value='1024'>1024</option><option value='2048'>2048</option><option value='4096'>4096</option><option value='8192'>8192</option>";
    // Set the initial value to 2048 (select the option with value 2048)
    select.value = '2048';
}

function setECCKeySizes() {
    var select = document.getElementById("keySize");
    select.innerHTML = "<option value='192'>192</option><option value='224'>224</option><option value='256'>256</option><option value='384'>384</option><option value='521'>521</option>";
    // Set the initial value to 2048 (select the option with value 2048)
    select.value = '256';
}

// Initially set the key sizes for RSA as the page loads.
window.onload = setRSAKeySizes;

// Validate that the country field is a valid two-letter country code
document.getElementById('country').addEventListener('input', function(e) {
    const value = e.target.value;
    if (value.length !== 2 || !/^[A-Za-z]{2}$/.test(value)) {
        alert('Please enter a valid two-letter country code.');
        e.target.focus();
    }
});

