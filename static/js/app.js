/* Initialize Materialize components */

document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('select');
    M.FormSelect.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('.modal');
    M.Modal.init(elems);
});

/* Helper functions */

function showLoader() {
    document.getElementById('loader').style.display = 'block';
}

function submitForm() {
    const form = document.querySelector('#search-form');

    showLoader();
    form.submit();
}

function processForm(e) {
    e.preventDefault();

    const urlParams = new URLSearchParams(window.location.search);
    const formData = new FormData(e.target);

    if (urlParams.get('q') == formData.get('q')
        && urlParams.get('top') == formData.get('top')
        && urlParams.get('method') == formData.get('method')) {
        const elem = document.querySelector('#confirm-modal');
        const instance = M.Modal.getInstance(elem);
        instance.open();
    } else {
        showLoader();
        e.target.submit();
    }
}
