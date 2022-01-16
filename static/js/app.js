document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('select');
    const instances = M.FormSelect.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('.dropdown-trigger');
    const instances = M.Dropdown.init(elems);
});

function showLoader() {
    document.getElementById("loader").style.display = "block";
}

function submitForm(e) {
    e.preventDefault();

    const urlParams = new URLSearchParams(window.location.search);
    const form = document.querySelector('form');
    const formData = new URLSearchParams(new FormData(form).entries());

    if (urlParams.get("q") !== formData.get("q")
        || urlParams.get("top") !== formData.get("top")
        || urlParams.get("method") !== formData.get("method")) {
        showLoader();
        form.submit();
    }
}
