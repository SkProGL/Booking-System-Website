document.addEventListener('DOMContentLoaded', function () {
    const toolbarContainer = document.getElementById('navigation_bar');
    navigation_option = toolbarContainer.getAttribute("nav-option");
    if (navigation_option) document.getElementById(navigation_option).parentElement.setAttribute('active-menu', '');
});