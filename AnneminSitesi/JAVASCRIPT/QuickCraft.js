function kutu(genislik, yukseklik, margin = {}, parentOptions = {}, id = '') {
    const div = document.createElement('div');
    if (id) div.id = id;
    div.style.width = genislik;
    div.style.height = yukseklik;
    div.style.border = 'solid black 2px';
    if (margin.top) div.style.marginTop = margin.top;
    if (margin.right) div.style.marginRight = margin.right;
    if (margin.bottom) div.style.marginBottom = margin.bottom;
    if (margin.left) div.style.marginLeft = margin.left;

    if (parentOptions.parent) parentOptions.parent.appendChild(div);
    else document.body.appendChild(div);
}

function login(genislik, yukseklik, inputOptions = {}, buttonOptions = {}, parentOptions = {}) {
    const div = document.createElement('div');
    div.style.width = genislik;
    div.style.height = yukseklik;
    div.style.border = 'solid 2px black';
    div.style.display = 'flex';
    div.style.flexDirection = 'column';
    div.style.justifyContent = 'center';
    div.style.alignItems = 'center';
    div.style.padding = '20px';
    
    const input = document.createElement('input');
    input.type = inputOptions.type || 'text';
    input.placeholder = inputOptions.placeholder || 'Username';


    const button = document.createElement('button');
    button.textContent = buttonOptions.text || 'Login';
    button.onclick = buttonOptions.onClick || (() => alert('Login clicked'));

    div.appendChild(input);
    div.appendChild(button);

    if (parentOptions.parent) parentOptions.parent.appendChild(div);
    else document.body.appendChild(div);
}

function container(genislik, yukseklik, border = {}, layoutOptions = {}, parentOptions = {}) {
    const div = document.createElement('div');
    div.style.width = genislik;
    div.style.height = yukseklik;
    if (border.border) div.style.border = 'solid black 2px';
    if (layoutOptions.yanyana) div.style.display = 'flex';
    if (layoutOptions.ortaladikey) div.style.justifyContent = 'center';
    if (layoutOptions.ortalayatay) div.style.alignItems = 'center';

    if (parentOptions.parent) parentOptions.parent.appendChild(div);
    else document.body.appendChild(div);
}

function resim(src, alt = '', styleOptions = {}, parentOptions = {}) {
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    if (styleOptions.width) img.style.width = styleOptions.width;
    if (styleOptions.height) img.style.height = styleOptions.height;
    if (styleOptions.borderRadius) img.style.borderRadius = styleOptions.borderRadius;
    if (styleOptions.margin) img.style.margin = styleOptions.margin;

    if (parentOptions.parent) parentOptions.parent.appendChild(img);
    else document.body.appendChild(img);
}

function liste(items, ordered = false, styleOptions = {}, parentOptions = {}) {
    const list = ordered ? document.createElement('ol') : document.createElement('ul');
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        list.appendChild(li);
    });

    if (styleOptions.color) list.style.color = styleOptions.color;
    if (styleOptions.fontSize) list.style.fontSize = styleOptions.fontSize;
    if (styleOptions.margin) list.style.margin = styleOptions.margin;

    if (parentOptions.parent) parentOptions.parent.appendChild(list);
    else document.body.appendChild(list);
}

//NE OLUŞTURDUKLARINI GÖRMEK İÇİN KULLANIM ÖRNEĞİ YAZAN YERİN ALTINDAKİ FONKSİYONLARIN // İŞARETİNİ KALDIRIN OLUŞTURUR
//UĞRAŞTIM O KADAR ANANIZI SİKERİM DOĞRU DÜZGÜN KULLANIN
//PARENT YAZAN ŞEY HANGİ KUTUNUN İÇİNDE OLMASI GEREKTİĞİ. EĞER PARENT KUTUNUZUN İD Sİ ORNEK123 İSE {parent: document.getElementById('ORNEK123')} ŞEKLİNDE KULLANIN

// login fonksiyonu:
// inputOptions: { placeholder: 'value', type: 'text' | 'password' }
// buttonOptions: { text: 'value', onClick: function }
// parentOptions: { parent: DOMElement }
// Kullanım Örneği:
//login('300px', '200px', { placeholder: 'Username', type: 'text' }, { text: 'Login', onClick: () => alert('Logging in!') }, { parent: document.getElementById('loginContainer') });

// kutu fonksiyonu:
// margin: { top: 'value', right: 'value', bottom: 'value', left: 'value' }
// parentOptions: { parent: DOMElement }
// Kullanım Örneği:
//kutu('300px', '150px', { top: '20px', right: '10px', bottom: '20px', left: '10px' }, { parent: document.body });

// container fonksiyonu:
// border: { border: true | false }
// layoutOptions: { yanyana: true, ortaladikey: true, ortalayatay: true }
// parentOptions: { parent: DOMElement }
// Kullanım Örneği:
//container('400px', '300px', 'solid 2px black', { yanyana: true, ortaladikey: true }, { parent: document.body });

// resim fonksiyonu:
// styleOptions: { width: 'value', height: 'value', borderRadius: 'value', margin: 'value' }
// parentOptions: { parent: DOMElement }
// Kullanım Örneği:
//resim('image.jpg', 'An image description', { width: '300px', height: '200px', borderRadius: '8px', margin: '10px' }, { parent: document.body });

// liste fonksiyonu:
// styleOptions: { color: 'value', fontSize: 'value', margin: 'value' }
// parentOptions: { parent: DOMElement }
// Kullanım Örneği:
//liste(['Item 1', 'Item 2', 'Item 3'], false, { color: 'blue', fontSize: '16px', margin: '10px' }, { parent: document.body });

//made by arda
