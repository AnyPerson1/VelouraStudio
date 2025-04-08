function selectNav(item) {
    // Tüm item'ların genişliğini sıfırla
    const navItems = document.querySelectorAll('.navigationDiv');
    navItems.forEach(navItem => {
        navItem.style.width = '0px';
    });

    // Seçilen item'ın genişliğini 75px yap
    const selectedItem = document.getElementById(item);
    selectedItem.style.width = '75px';
}