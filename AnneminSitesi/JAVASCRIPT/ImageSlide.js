let imageIndex = 0;

function slideImage(to) {
    const slides = document.getElementsByClassName('SlideShowImage');
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }
    slides[to].style.display = 'block';
    imageIndex = to; 
}

// Tüm slaytları devre dışı bırak
function disableAll() {
    const slides = document.getElementsByClassName('SlideShowImage');
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }
}

// Otomatik geçiş için bir örnek
function nextSlide() {
    const slides = document.getElementsByClassName('SlideShowImage');
    disableAll();
    imageIndex = (imageIndex + 1) % slides.length; 
    slides[imageIndex].style.display = 'block';
}
