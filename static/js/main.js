// document.addEventListener("DOMContentLoaded", function() {
    
//     const loadContent = (target, url) => {
//         fetch(url)
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error(`Failed to load content: ${response.statusText}`);
//                 }
//                 return response.text();
//             })
//             .then(data => {
//                 document.getElementById(target).innerHTML = data;
//                 setRSAKeySizes(); // Set initial RSA key sizes on page load
//             })
//             .catch(error => console.error('Error loading content:', error));
//     };

//     const activateTab = (tab) => {
//         const targetPanel = tab.getAttribute('data-target');
//         const url = `/${targetPanel}`;

//         document.querySelectorAll('[role=tab]').forEach(t => t.removeAttribute('aria-current'));
//         tab.setAttribute('aria-current', 'true');

//         document.querySelectorAll('[role=tabpanel]').forEach(tp => tp.setAttribute('hidden', 'true'));
//         document.getElementById(targetPanel).removeAttribute('hidden');

//         loadContent(targetPanel, url);
//     };

//     // Initial load for the first tab
//     const defaultTab = document.querySelector('[role=tab]');
//     activateTab(defaultTab);
    

//     // Event listener for tab clicks
//     document.querySelectorAll('[role=tab]').forEach(tab => {
//         tab.addEventListener('click', function(e) {
//             e.preventDefault();
//             activateTab(this);
//         });
//     });
// });

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

function setProfile(profile) {
    const groupCheckboxes = document.querySelectorAll('input.keyGroup[type="checkbox"]');
    groupCheckboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    })
    if (profile === "SSL") {
        document.getElementById('digitalsignature').checked = true;
        document.getElementById('keyencipher').checked = true;
        document.getElementById('serverauth').checked = true;
        document.getElementById('clientauth').checked = true;
    }
    if (profile === "SMIME") {
        document.getElementById('digitalsignature').checked = true;
        document.getElementById('keyencipher').checked = true;
        document.getElementById('keyagree').checked = true;
        document.getElementById('nonrepudation').checked = true;
        document.getElementById('emailprotect').checked = true;
    }
    if (profile === "CODESIGN") {
        document.getElementById('digitalsignature').checked = true;
        document.getElementById('sign').checked = true;
        document.getElementById('timestamp').checked = true;
    }
    if (profile === "DOCUSIGN") {
        document.getElementById('digitalsignature').checked = true;
        document.getElementById('nonrepudation').checked = true;
        document.getElementById('sign').checked = true;
    }
}

// Validate that the country field is a valid two-letter country code
document.getElementById('country').addEventListener('input', function(e) {
    const value = e.target.value;
    if (value.length !== 2 || !/^[A-Za-z]{2}$/.test(value)) {
        alert('Please enter a valid two-letter country code.');
        e.target.focus();
    }
});

