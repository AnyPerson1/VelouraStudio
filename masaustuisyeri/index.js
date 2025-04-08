const Database = require("better-sqlite3");
const db = new Database("data.sqlite");
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleButton');
    const historyDiv = document.getElementById('historyDiv');
    let isOpen = false;

    toggleButton.addEventListener('click', () => {
        if (isOpen) {
            toggleButton.innerHTML = ">";
            historyDiv.style.left = '-350px';
        } else {
            toggleButton.innerHTML = "<";
            historyDiv.style.left = '0';
        }
        isOpen = !isOpen;
    });

    tabloyuGuncelle(); 
});

async function tabloyuGuncelle() {
    const veriler = await window.api.veriCek();
    const tbody = document.querySelector(".mainTable tbody");

    tbody.innerHTML = ""; // Önce tabloyu temizle

    veriler.forEach((veri) => {
        const satir = document.createElement("tr");

        satir.innerHTML = `
            <td>${veri.isim}</td>
            <td>${veri.tarih}</td>
            <td>${veri.ucret + " TL"}</td>
            <td>${veri.islem}</td>
        `;

        tbody.appendChild(satir);
    });
}


document.addEventListener('DOMContentLoaded', () => {
    const table = document.querySelector('.mainTable');

    table.addEventListener('click', (e) => {
        const target = e.target;

        if (target.tagName === 'TD') {
            const currentValue = target.textContent;
            const input = document.createElement('input');

            input.type = 'text';
            input.value = currentValue;
            input.style.width = '100%';
            input.style.boxSizing = 'border-box';

            target.textContent = '';
            target.appendChild(input);
            input.focus();

            input.addEventListener('blur', () => {
                target.textContent = input.value || currentValue;
            });

            input.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    target.textContent = input.value || currentValue;
                }
            });
        }
    });
});
